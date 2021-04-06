"""Extract contents from a Pandas dataframe."""

import logging

from typing import List

import pandas

from mesmsage import constants


class IndividualNotFoundError(Exception):
    """Define error to indicate that there is no row available for an individual."""

    pass


def get_individual_names(
    individuals_dataframe: pandas.DataFrame,
) -> pandas.core.series.Series:
    """Extract the names of individuals from the data frame."""
    logger = logging.getLogger(constants.logging.Rich)
    try:
        individuals = individuals_dataframe.loc[:, constants.sheets.Name]
    except KeyError:
        raise IndividualNotFoundError
    logger.debug(individuals)
    return individuals


def get_individual_numbers(
    individuals_dataframe: pandas.DataFrame, chosen_individuals_list: List[str]
) -> pandas.DataFrame:
    """Get the phone numbers for each of the specified individuals in a complete data frame with names."""
    logger = logging.getLogger(constants.logging.Rich)
    phone_numbers = individuals_dataframe.loc[
        individuals_dataframe["Individual Name"].isin(chosen_individuals_list),
        ["Individual Name", "Individual Phone Number"],
    ]
    logger.debug(f"Phone numbers: {phone_numbers}")
    return phone_numbers


def convert_series_to_list(series: pandas.core.series.Series) -> List:
    """Convert a pandas series to a standard list."""
    series_list = series.values.tolist()
    return series_list
