"""Run tasks that support easy testing across multiple Python versions."""

import inspect

from invoke import task

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
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite
    if noexternal:
        c.run("poetry run pytest -x -s -m 'not googlesheets and not twilio'")
    else:
        c.run("poetry run pytest -x -s")
    print("---> End " + inspect.currentframe().f_code.co_name)


@task
def debugtest(c, noexternal=False):
    """Run the test suite."""
    display_internal_python_version(c)
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite
    if noexternal:
        c.run(
            "poetry run pytest -x -s --log-cli-level=DEBUG -m 'not googlesheets and not twilio'"
        )
    else:
        c.run("poetry run pytest -x -s --log-cli-level=DEBUG")
    print("---> End " + inspect.currentframe().f_code.co_name)


@task
def cover(c):
    """Run the test suite and collect coverage information."""
    display_internal_python_version(c)
    print("Begin " + inspect.currentframe().f_code.co_name + " --->")
    # run the test suite and collect coverage information
    c.run(
        "poetry run pytest -s --cov-config .coveragerc --cov-report term-missing --cov=mesmsage --cov-branch -m 'not twilio'"
    )
    print("---> End " + inspect.currentframe().f_code.co_name)


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
