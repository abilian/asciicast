# Asciicast: generate asciicasts from Python code

[![image](https://img.shields.io/pypi/v/asciicast.svg)](https://pypi.python.org/pypi/asciicast)

[![image](https://img.shields.io/travis/sfermigier/asciicast.svg)](https://travis-ci.com/sfermigier/asciicast)

[![Documentation Status](https://readthedocs.org/projects/asciicast/badge/?version=latest)](https://asciicast.readthedocs.io/en/latest/?version=latest)

This package provides a Python API to generate
[asciicasts](https://asciinema.org/docs/asciicast-v2) from Python code.

## Installation

```bash
    pip install asciicast
```

## Demo

[![asciicast](https://asciinema.org/a/wlIj0hTLZVWnjGdIsiB730KT2.svg)](https://asciinema.org/a/wlIj0hTLZVWnjGdIsiB730KT2)

## Usage

The `asciicast` module provides a `Asciicast` class that can be used to record
asciicasts from Python code.

Example:

```python
from asciicast.cast import Cast

cast = Cast(typing_delay=0.03)

cast.echo("# How to use asciicast?")
cast.wait(0.5)

cast.type("cat -n examples/demo1.py")
cast.wait(0.2)

cast.run()
```
