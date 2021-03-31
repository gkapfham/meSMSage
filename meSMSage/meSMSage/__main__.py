"""Define the command-line interface for the meSMSage program."""

import demonstrate
import sheets

from rich.traceback import install

import pandas
import typer


def main(
    googlesheet_id: str = typer.Option(...),
):
    """Access the command-line argument(s) and then perform actions."""
    # setup rich-based tracebacks to enable better debugging on program crash
    install()
    # display the debugging output for the program's command-line arguments
    typer.echo("")
    typer.echo(f"The chosen Google Sheet is {googlesheet_id}!")
    typer.echo("")
    # connect the specified Google Sheet using the default internal sheet of "Sheet1"
    sheet = sheets.connect_to_sheet(googlesheet_id)
    data_range = sheet.get_data_range()
    values = data_range.get_values()
    print(f"All values: {values}")
    sheetfu_volunteers_dataframe = pandas.DataFrame(values[1:len(values)], columns=values[0])
    print(sheetfu_volunteers_dataframe)
    demonstrate.demonstrate_pandas_analysis(sheetfu_volunteers_dataframe)


if __name__ == "__main__":
    typer.run(main)
