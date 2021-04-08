"""Extract contents from a Pandas dataframe."""

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
) -> Dict[str, str]:
    """Get the phone numbers for each of the specified individuals in a complete data frame with names."""
    logger = logging.getLogger(constants.logging.Rich)
    # extract the phone numbers of the chosen individuals
    phone_numbers = individuals_dataframe.loc[
        individuals_dataframe[constants.sheets.Name].isin(chosen_individuals_list),
        [constants.sheets.Name, constants.sheets.Number],
    ]
    logger.debug(f"Phone numbers: {phone_numbers}")
    # create an empty dictionary that will store mappings of the form:
    # <Name of a Person> --> <Phone Number of a Person>
    phone_numbers_dictionary = {}
    # iterate through each row in the data frame and create a dictionary
    # entry out of the name of a person and their phone number
    for (index, row) in phone_numbers.iterrows():
        phone_numbers_dictionary[row["Individual Name"]] = row[
            "Individual Phone Number"
        ]
    return phone_numbers_dictionary


def get_individual_activities(
    individuals_dataframe: pandas.DataFrame, chosen_individuals_list: List[str]
) -> Dict[str, List[str]]:
    """Get the activities for each of the specified individuals."""
    logger = logging.getLogger(constants.logging.Rich)
    # remove columns in the data frame for which no individual has an activity
    individuals_have_activities = individuals_dataframe
    logger.debug(individuals_have_activities)
    # only consider the individuals who were chosen
    specific_individuals_have_activities = individuals_have_activities.loc[
        individuals_have_activities["Individual Name"].isin(chosen_individuals_list)
    ]
    logger.debug(specific_individuals_have_activities)
    # only consider the activities for which one of these individuals is active, meaning
    # that this step removes activities for which all of the entries are False
    specific_individuals_specific_activities = specific_individuals_have_activities.loc[
        :, (specific_individuals_have_activities != 0).any(axis=0)
    ]
    logger.debug(specific_individuals_specific_activities)
    # reshape the data frame by converting it to a list and then back to a data frame
    # ultimately producing a "tall" data frame where each column is an individual,
    # their contact information, and the activities that they are going to need
    specific_individuals_specific_activities_dict = (
        specific_individuals_specific_activities.to_dict("list")
    )
    logger.debug(specific_individuals_specific_activities_dict)
    specific_individuals_specific_activities_tall = pandas.DataFrame.from_dict(
        specific_individuals_specific_activities_dict, orient="index"
    )
    logger.debug(specific_individuals_specific_activities_tall)
    # iterate through each of the columns in the tall data frame and create
    # a dictionary that maps an individual to a list of their activities
    name_activities_dictionary: Dict[str, List[str]] = {}
    for (
        column_name,
        column_contents,
    ) in specific_individuals_specific_activities_tall.iteritems():
        current_name = None
        # iterate through the metadata (i.e., headers of original data frame)
        # and the data (i.e., the contents of the original data frame)
        for (data, metadata) in zip(
            list(column_contents), list(column_contents.index.values)
        ):
            # store the name of the current individual since this will
            # serve as the key in the name_activities_dictionary
            if metadata == "Individual Name":
                current_name = data
            # indicate that the person is going to work a shift since
            # there is a "checkmark" (i.e., a True value) for the specific
            # data entry associated with this activity
            if data is True:
                # this individual already has an entry in the dictionary
                # and so the function must extract the existing list of
                # activities and append to it the current description of
                # the activity (i.e., the metadata originally stored in
                # the header of the data frame)
                if current_name in name_activities_dictionary:
                    metadata_list = name_activities_dictionary[current_name]
                    metadata_list.append(metadata)
                # this individual does not already have an entry in the
                # dictionary and so the function must create a new list
                # of activity descriptions and then create the mapping
                else:
                    new_metadata_list: List[str] = [metadata]
                    name_activities_dictionary[current_name] = new_metadata_list  # type: ignore
        # support the movement to a new name
        current_name = None
    logger.debug(name_activities_dictionary)
    return name_activities_dictionary


def convert_series_to_list(series: pandas.core.series.Series) -> List:
    """Convert a pandas series to a standard list."""
    series_list = series.values.tolist()
    return series_list
