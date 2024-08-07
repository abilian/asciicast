import nox

PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]
DEFAULT_PYTHON_VERSION = PYTHON_VERSIONS[-1]
nox.options.sessions = ["lint", "pytest"]


@nox.session(python=DEFAULT_PYTHON_VERSION)
def lint(session: nox.Session) -> None:
    session.install("-e", ".[dev]")
    session.run("pip", "check")
    session.run("make", "lint", external=True)


@nox.session(python=PYTHON_VERSIONS)
def pytest(session: nox.Session) -> None:
    session.install("-e", ".")
    session.install("pytest")
    session.run("pip", "check")
    session.run("pytest", "src")
