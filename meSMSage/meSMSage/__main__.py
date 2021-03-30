"""Define the command-line interface for the meSMSage program."""

import typer


def main(
    sheet: str = typer.Option(...),
):
    """Access the command-line argument(s) and then perform actions."""
    # display the debugging output for the program's command-line arguments
    typer.echo("")
    typer.echo(f"The chosen Google Sheet is {sheet}!")
    typer.echo("")


if __name__ == "__main__":
    typer.run(main)
