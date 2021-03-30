"""Define the command-line interface for the meSMSage program."""

import gspread
import pandas
import typer


def main(
    sheet: str = typer.Option(...),
):
    """Access the command-line argument(s) and then perform actions."""
    # display the debugging output for the program's command-line arguments
    typer.echo("")
    typer.echo(f"The chosen Google Sheet is {sheet}!")
    typer.echo("")
    # create a connection to the specified Google Sheet
    google_client = gspread.service_account("credentials.json")
    worksheet = google_client.open(sheet).sheet1
    # create a Pandas dataframe from the spreadsheet's worksheet
    dataframe = pandas.DataFrame(worksheet.get_all_records())
    print(dataframe)
    print()


if __name__ == "__main__":
    typer.run(main)
