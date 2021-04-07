"""Demonstrate examples associated with using pandas on the dataframe."""

import logging

import numpy
import pandas

from mesmsage import constants


def demonstrate_pandas_analysis(volunteers_dataframe: pandas.DataFrame) -> None:
    """Demonstrate the use of different functions for the analysis of a pandas data frame."""
    logger = logging.getLogger(constants.logging.Rich)
    logger.debug(volunteers_dataframe)
    logger.debug("General Debugging information about volunteers_dataframe")
    logger.debug(volunteers_dataframe.columns)
    logger.debug(volunteers_dataframe.columns[0])
    logger.debug(volunteers_dataframe.dtypes)
    logger.debug("Debugging information about volunteers_dataframe's size")
    logger.debug(volunteers_dataframe.ndim)
    logger.debug(volunteers_dataframe.shape)
    logger.debug(volunteers_dataframe.size)
    logger.debug(volunteers_dataframe.memory_usage())
    # display the details about all of the people
    individuals = volunteers_dataframe.loc[:, "Individual Name"]
    logger.debug(type(individuals))
    logger.debug(individuals)
    # display the shifts for a specified person
    greg_shifts = volunteers_dataframe[
        volunteers_dataframe["Individual Name"] == "Gregory Kapfhammer"
    ]
    logger.debug(greg_shifts)
    greg_shifts_list = []
    for column_name, column_contents in greg_shifts.iteritems():
        logger.debug(f"Column Name:  {column_name}")
        logger.debug(f"Column Contents:  {column_contents.values}")
        logger.debug(f"Column Contents Type:  {type(column_contents.values)}")
        logger.debug(f"Column Contents array index:  {column_contents.values[0]}")
        logger.debug(
            f"Column Contents array index type:  {type(column_contents.values[0])}"
        )
        if column_contents.values[0] is numpy.bool_(True):
            logger.debug("Working the shift!")
            greg_shifts_list.append(column_name)
    logger.debug(greg_shifts_list)
    data = volunteers_dataframe
    names = ["Gregory Kapfhammer", "Jessica Kapfhammer", "Jennifer Dingeldine"]
    phone_numbers = data.loc[data["Individual Name"].isin(names)]
    logger.debug(phone_numbers)
    logger.debug(type(phone_numbers))
    output = phone_numbers[phone_numbers.eq(True).any(axis=1)]
    logger.debug(output.head())
    matching = phone_numbers.loc[:, (phone_numbers == True).any()]
    again = output.loc[(output["Individual Name"].isin(names)) | (output == True).any()]
    logger.debug(again)
    logger.debug(matching)
    has_shift = data[data.any(1)]  # GOOD
    has_shift_specific = has_shift.loc[has_shift["Individual Name"].isin(names)]  # GOOD
    logger.debug(has_shift_specific)
    hsss = has_shift_specific.loc[:, (has_shift_specific != 0).any(axis=0)]  # GOOD
    logger.debug(hsss)
    for column_name, column_contents in hsss.iteritems():
        if column_name == "Individual Name":
            logger.debug(f"The name is {column_contents.values}")
    for index, row in hsss.iterrows():
        logger.debug(row["Individual Name"])
        logger.debug(row["Individual Phone Number"])
    dictionary = hsss.to_dict("list")
    logger.debug(dictionary)
    tryit_long = pandas.DataFrame.from_dict(dictionary)
    logger.debug(tryit_long)
    tryit_tall = pandas.DataFrame.from_dict(dictionary, orient="index")  # GOOD
    logger.debug(tryit_tall)  # GOOD
    for column_name, column_contents in tryit_tall.iteritems():
        logger.debug(list(column_contents))
        logger.debug(list(column_contents.index.values))
