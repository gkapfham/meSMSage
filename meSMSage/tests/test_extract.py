"""Test the functions in the extract module."""

import pandas

from mesmsage import extract


def test_convert_series_to_list():
    """Ensure that the conversion from a pandas series to a list works correctly."""
    series = pandas.Series([0, 1, 2])
    series_list = extract.convert_series_to_list(series)
    assert series_list is not None
    assert len(series_list) == 3


def test_extract_individual_names():
    """Ensure that it is possible to extract the names of individuals."""
    dataframe = pandas.DataFrame(
        {
            "Individual Name": ["Gregory", "Jessica", "Madelyn"],
            "Individual Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    individual_names = extract.extract_individual_names(dataframe)
    assert individual_names is not None
    individual_names_list = individual_names.values.tolist()
    assert individual_names_list is not None
    assert len(individual_names_list) == 3
