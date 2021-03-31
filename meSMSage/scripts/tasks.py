"""Run tasks that support easy testing across multiple Python versions."""

from invoke import task


@task
def test(c):
    """Run the test suite."""
    # display diagnostic information about new version of Python
    c.run("python --version")
    # run the test suite
    c.run("poetry run pytest -x -s")
