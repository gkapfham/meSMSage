"""Extract contents from a Pandas dataframe."""

import logging

import pandas

from mesmsage import constants


def extract_individual_names(
    volunteers_dataframe: pandas.DataFrame,
) -> pandas.core.series.Series:
    """Extract the names of individuals from the data frame."""
    logger = logging.getLogger(constants.logging.Rich)
    individuals = volunteers_dataframe.loc[:, constants.sheets.Name]
    logger.debug(individuals)
    return individuals
