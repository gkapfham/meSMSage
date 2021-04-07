"""Extract contents from a Pandas dataframe."""

import itertools
import logging

from typing import Dict
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
    phone_numbers_dictionary = {}
    for (index, row) in phone_numbers.iterrows():
        logger.debug(index)
        logger.debug(row)
        phone_numbers_dictionary[row["Individual Name"]] = row["Individual Phone Number"]
    return phone_numbers_dictionary


def get_individual_activities(
    individuals_dataframe: pandas.DataFrame, chosen_individuals_list: List[str]
) -> Dict[str, str]:
    """Get the activities for each of the specified individuals."""
    logger = logging.getLogger(constants.logging.Rich)
    individuals_have_shifts = individuals_dataframe[individuals_dataframe.any(1)]
    specific_individuals_have_shifts = individuals_have_shifts.loc[
        individuals_have_shifts["Individual Name"].isin(chosen_individuals_list)
    ]
    logger.debug(specific_individuals_have_shifts)
    specific_individuals_specific_shifts = specific_individuals_have_shifts.loc[
        :, (specific_individuals_have_shifts != 0).any(axis=0)
    ]
    logger.debug(specific_individuals_specific_shifts)
    specific_individuals_specific_shifts_dict = (
        specific_individuals_specific_shifts.to_dict("list")
    )
    specific_individuals_specific_shifts_tall = pandas.DataFrame.from_dict(
        specific_individuals_specific_shifts_dict, orient="index"
    )
    name_activities_dictionary = {}
    for (
        column_name,
        column_contents,
    ) in specific_individuals_specific_shifts_tall.iteritems():
        logger.debug(list(column_contents))
        logger.debug(list(column_contents.index.values))
        current_name = None
        for (data, metadata) in zip(
            list(column_contents), list(column_contents.index.values)
        ):
            logger.debug(f"Data: {data}")
            logger.debug(f"Metadata: {metadata}")
            if metadata == "Individual Name":
                current_name = data
            if data is True:
                if current_name in name_activities_dictionary:
                    metadata_list = name_activities_dictionary[current_name]
                    metadata_list.append(metadata)
                else:
                    name_activities_dictionary[current_name] = [metadata]
        current_name = None
    return name_activities_dictionary


def convert_series_to_list(series: pandas.core.series.Series) -> List:
    """Convert a pandas series to a standard list."""
    series_list = series.values.tolist()
    return series_list
