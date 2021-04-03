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
