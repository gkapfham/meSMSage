"""Run tasks that support easy testing across multiple Python versions."""

import inspect

from invoke import task

from rich.console import Console

console = Console()

displayed_python_verison = False


def display_internal_python_version(c):
    """Display the version of Python."""
    global displayed_python_verison
    # display diagnostic information about new version of Python
    if not displayed_python_verison:
        c.run("python --version")
        displayed_python_verison = True


@task
def test(c, noexternal=False):
    """Run the test suite."""
    display_internal_python_version(c)
    console.print(f"[bold red]:zap:Begin {inspect.currentframe().f_code.co_name} [/bold red]")
    # run the test suite
    if noexternal:
        c.run("poetry run pytest -x -s -m 'not googlesheets and not twilio'")
    else:
        c.run("poetry run pytest -x -s")
    console.print(f"[bold red]:zap:End {inspect.currentframe().f_code.co_name} [/bold red]")


@task
def debugtest(c, noexternal=False):
    """Run the test suite."""
    display_internal_python_version(c)
    console.print(f"[bold red]:zap:Begin {inspect.currentframe().f_code.co_name} [/bold red]")
    # run the test suite
    if noexternal:
        c.run(
            "poetry run pytest -x -s --log-cli-level=DEBUG -m 'not googlesheets and not twilio'"
        )
    else:
        c.run("poetry run pytest -x -s --log-cli-level=DEBUG")
    console.print(f"[bold red]:zap:End {inspect.currentframe().f_code.co_name} [/bold red]")


@task
def cover(c):
    """Run the test suite and collect coverage information."""
    display_internal_python_version(c)
    console.print(f"[bold red]:zap:Begin {inspect.currentframe().f_code.co_name} [/bold red]")
    # run the test suite and collect coverage information
    # note that this does not run the test cases marked with the @twilio
    # marker so as to not incur service costs when testing. While this
    # will still run the test cases that use mocks, it may still result
    # in the tests having lower coverage than would otherwise be the case
    c.run(
        "poetry run pytest -s --cov-config .coveragerc --cov-report term-missing --cov=mesmsage --cov-branch -m 'not twilio'"
    )
    console.print(f"[bold red]:zap:Begin {inspect.currentframe().f_code.co_name} [/bold red]")


@task
def black(c):
    """Run black code format check."""
    display_internal_python_version(c)
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite and collect coverage information
    c.run("poetry run black mesmsage tests --check")
    print("---> End " + inspect.currentframe().f_code.co_name)


@task
def flake8(c):
    """Run the test suite."""
    display_internal_python_version(c)
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite and collect coverage information
    c.run("poetry run flake8 -v mesmsage tests")
    print("---> End " + inspect.currentframe().f_code.co_name)


@task
def mypy(c):
    """Run mypy."""
    display_internal_python_version(c)
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite and collect coverage information
    c.run("poetry run mypy mesmsage")
    print("---> End " + inspect.currentframe().f_code.co_name)


@task
def pydocstyle(c):
    """Run pydocstyle."""
    display_internal_python_version(c)
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite and collect coverage information
    c.run("poetry run pydocstyle -v mesmsage tests")
    print("---> End " + inspect.currentframe().f_code.co_name)


@task
def pylint(c):
    """Run pylint."""
    display_internal_python_version(c)
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite and collect coverage information
    c.run("poetry run pylint mesmsage tests")
    print("---> End " + inspect.currentframe().f_code.co_name)


@task(black, flake8, mypy, pydocstyle, pylint)
# pylint: disable=unused-argument
def linters(c):
    """Run all of the tasks."""


@task(cover, linters)
# pylint: disable=unused-argument
def all(c):
    """Run all of the tasks."""
