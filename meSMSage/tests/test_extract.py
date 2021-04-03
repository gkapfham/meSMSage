"""Test the functions in the extract module."""

import pandas

from mesmsage import extract


def test_extract_individual_names():
    """Ensure that it is possible to extract the names of individuals."""
    dataframe = pandas.DataFrame(
        {
            "Volunteer Name": ["Gregory", "Jessica", "Madelyn"],
            "Volunteer Phone Number": ["888-111-5555", "888-222-5555", "888-333-5555"],
        }
    )
    individual_names = extract.extract_individual_names(dataframe)
    assert individual_names is not None
    individual_names_list = individual_names.values.tolist()
    assert individual_names_list is not None
    assert len(individual_names_list) == 3
