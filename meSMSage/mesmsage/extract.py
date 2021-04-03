"""Extract contents from a Pandas dataframe."""

import logging

from typing import List

import pandas

from mesmsage import constants


def get_individual_names(
    individuals_dataframe: pandas.DataFrame,
) -> pandas.core.series.Series:
    """Extract the names of individuals from the data frame."""
    logger = logging.getLogger(constants.logging.Rich)
    individuals = individuals_dataframe.loc[:, constants.sheets.Name]
    logger.debug(individuals)
    return individuals


def convert_series_to_list(series: pandas.core.series.Series) -> List:
    """Convert a pandas series to a standard list."""
    series_list = series.values.tolist()
    return series_list
