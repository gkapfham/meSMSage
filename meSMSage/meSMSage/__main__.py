"""Define the command-line interface for the meSMSage program."""

import demonstrate
import sheet

import pandas
import typer


def main(
    googlesheet: str = typer.Option(...),
):
    """Access the command-line argument(s) and then perform actions."""
    # display the debugging output for the program's command-line arguments
    typer.echo("")
    typer.echo(f"The chosen Google Sheet is {sheet}!")
    typer.echo("")
    # create a connection to the specified Google Sheet
    worksheet = sheet.connect(googlesheet)
    # create a Pandas volunteers_dataframe from the spreadsheet's worksheet
    volunteers_dataframe = pandas.DataFrame(worksheet.get_all_records())
    demonstrate.demonstrate_pandas_analysis(volunteers_dataframe)


if __name__ == "__main__":
    typer.run(main)
