from __future__ import annotations

import abc
import json
import os
import shlex
import tempfile
from pathlib import Path
from typing import Any
from uuid import uuid4

import asciinema.asciicast
from attr import define, field, mutable

SHELL = "/bin/sh"
TYPING_DELAY = 0.04


@define
class Cast:
    commands: list[Command] = field(factory=list)
    typing_delay: float = TYPING_DELAY

    def echo(self, line: str) -> None:
        self.commands.append(Echo(line))

    def type(self, line: str) -> None:
        self.commands.append(Type(line))

    def wait(self, seconds: float) -> None:
        self.commands.append(Wait(seconds))

    def run(self):
        script = self._generate_script()

        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_script = Path(tmp_dir) / "script.sh"
            tmp_cast = Path(tmp_dir) / "asciicast.cast"

            tmp_script.write_text(script)

            cmd = [
                "asciinema",
                "rec",
                "-c",
                f"{SHELL} {tmp_script}",
                "--overwrite",
                str(tmp_cast),
            ]
            os.system(shlex.join(cmd))

            cast = tmp_cast.read_bytes()

        # print(cast.decode("utf-8"))
        self._parse(cast)
        self._render()

    # Private methods
    def _generate_script(self) -> str:
        script = ["#!/bin/sh", "clear"]
        for command in self.commands:
            cmd_script = command.script()
            if cmd_script:
                script.append(cmd_script)
        return "\n".join(script)

    def _parse(self, cast: bytes):
        cmd = None
        start_ts = 0.0

        for line in cast.splitlines():
            if not line.startswith(b'['):
                continue
            ts, _, data = json.loads(line)
            if data.startswith("## start "):
                uid = data.split(" ", 2)[2].strip()
                cmd = self._get_cmd_by_uid(uid)
                start_ts = ts
            elif data.startswith("## end "):
                uid = data.split(" ", 2)[2].strip()
                assert cmd.uid == uid
                cmd = None
            else:
                if cmd is not None:
                    cmd.parse(ts-start_ts, data)

    def _get_cmd_by_uid(self, uid: str) -> Command:
        for cmd in self.commands:
            if cmd.uid == uid:
                return cmd
        raise ValueError(f"Command with uid {uid} not found")

    def _render(self):
        with Writer("test.cast") as writer:
            for cmd in self.commands:
                cmd.write(writer)


@mutable
class Writer:
    path: str | Path
    current_ts: float = 0.0
    writer: Any = None

    def __enter__(self):
        self.writer = asciinema.asciicast.v2.writer(self.path, width=80, height=24)
        self.writer.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.writer.__exit__(exc_type, exc_value, traceback)

    def write_event(self, event_type: str, data: str, delay: float):
        assert event_type == "o"
        self.writer.write_stdout(self.current_ts, data)
        self.current_ts += delay

    def wait(self, seconds: float):
        self.current_ts += seconds


class Command(abc.ABC):
    uid: str = field(init=False)

    def __attrs_post_init__(self):
        self.uid = uuid4().hex

    def script(self):
        return ""

    def parse(self, ts: float, data: str):
        pass

    @abc.abstractmethod
    def write(self, writer):
        raise NotImplementedError


@define
class Echo(Command):
    line: str

    def script(self):
        return f'echo "{self.line}"'

    def write(self, writer):
        for c in self.line:
            writer.write_event("o", c, TYPING_DELAY)
        writer.write_event("o", "\n\r", TYPING_DELAY)


@define
class Type(Command):
    line: str
    outputs: list[tuple[float, str]] = field(factory=list)

    def script(self):
        cmds = [
            "sleep 0.1",
            f"echo '## start {self.uid}'",
            "sleep 0.1",
            self.line,
            "sleep 0.1",
            f"echo '## end {self.uid}'",
            "sleep 0.1",
        ]
        return "\n".join(cmds)

    def write(self, writer):
        for c in self.line:
            writer.write_event("o", c, TYPING_DELAY)
        writer.write_event("o", "\n\r", TYPING_DELAY)

        for ts, data in self.outputs:
            writer.write_event("o", data, 0.1)

    def parse(self, ts: float, data: str):
        for line in data.splitlines():
            self.outputs.append((ts, line+"\r\n"))


@define
class Wait(Command):
    seconds: float

    def write(self, writer):
        writer.wait(self.seconds)
