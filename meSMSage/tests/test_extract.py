"""Test the functions in the extract module."""

import pandas

import pytest

from mesmsage import extract


def test_convert_series_to_list():
    """Ensure that the conversion from a pandas series to a list works correctly."""
    series = pandas.Series([0, 1, 2])
    series_list = extract.convert_series_to_list(series)
    assert series_list is not None
    assert len(series_list) == 3


def test_extract_individual_names_column_exists():
    """Ensure that it is possible to extract the names of individuals."""
    dataframe = pandas.DataFrame(
        {
            "Individual Name": ["Gregory", "Jessica", "Madelyn"],
            "Individual Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    individual_names = extract.get_individual_names(dataframe)
    assert individual_names is not None
    individual_names_list = individual_names.values.tolist()
    assert individual_names_list is not None
    assert len(individual_names_list) == 3


def test_extract_individual_names_column_does_not_exists():
    """Ensure that extract the names of individuals crashes for malformed data frame with incorrect name column."""
    dataframe = pandas.DataFrame(
        {
            "Person's Name": ["Gregory", "Jessica", "Madelyn"],
            "Individual Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    with pytest.raises(extract.IndividualNotFoundError):
        _ = extract.get_individual_names(dataframe)


def test_extract_get_phone_numbers_single_person():
    """Ensure that it is possible to get a single person's telephone number from the data frame."""
    dataframe = pandas.DataFrame(
        {
            "Individual Name": ["Gregory", "Jessica", "Madelyn"],
            "Individual Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    individual_names_list = ["Madelyn"]
    phone_numbers = extract.get_individual_numbers(dataframe, individual_names_list)
    assert phone_numbers is not None
    assert phone_numbers.ndim == 2
    assert phone_numbers.size == 2


def test_extract_get_phone_numbers_multiple_person():
    """Ensure that it is possible to get multiple people's telephone number from the data frame."""
    dataframe = pandas.DataFrame(
        {
            "Individual Name": ["Gregory", "Jessica", "Madelyn"],
            "Individual Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    individual_names_list = ["Madelyn", "Gregory"]
    phone_numbers = extract.get_individual_numbers(dataframe, individual_names_list)
    assert phone_numbers is not None
    assert phone_numbers.ndim == 2
    assert phone_numbers.size == 4


def test_extract_get_phone_numbers_no_matching_person():
    """Ensure that it is possible to get no matching person's telephone number from the data frame."""
    dataframe = pandas.DataFrame(
        {
            "Individual Name": ["Gregory", "Jessica", "Madelyn"],
            "Individual Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    individual_names_list = ["Incorrect Name"]
    phone_numbers = extract.get_individual_numbers(dataframe, individual_names_list)
    assert phone_numbers is not None
    assert phone_numbers.ndim == 2
    assert phone_numbers.size == 0


def test_extract_get_phone_numbers_no_matching_person_empty_list():
    """Ensure that it is possible to get no matching person's telephone number from the data frame."""
    dataframe = pandas.DataFrame(
        {
            "Individual Name": ["Gregory", "Jessica", "Madelyn"],
            "Individual Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    individual_names_list = []
    phone_numbers = extract.get_individual_numbers(dataframe, individual_names_list)
    assert phone_numbers is not None
    assert phone_numbers.ndim == 2
    assert phone_numbers.size == 0
