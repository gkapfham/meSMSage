"""Demonstrate examples associated with using pandas on the dataframe."""

import numpy
import pandas


def demonstrate_pandas_analysis(volunteers_dataframe: pandas.DataFrame):
    """Demonstrate the use of different functions for the analysis of a pandas data frame."""
    print(volunteers_dataframe)
    print()
    print("General Debugging information about volunteers_dataframe")
    print(volunteers_dataframe.columns)
    print(volunteers_dataframe.columns[0])
    print(volunteers_dataframe.dtypes)
    print()
    print("Debugging information about volunteers_dataframe's size")
    print(volunteers_dataframe.ndim)
    print(volunteers_dataframe.shape)
    print(volunteers_dataframe.size)
    print(volunteers_dataframe.memory_usage())
    print()
    # display the shifts for a specified person
    greg_shifts = volunteers_dataframe[volunteers_dataframe['Volunteer Name'] == "Gregory Kapfhammer"]
    print()
    print(greg_shifts)
    print()
    greg_shifts_list = []
    for column_name, column_contents in greg_shifts.iteritems():
        print(f"Column Name:  {column_name}")
        print(f"Column Contents:  {column_contents.values}")
        print(f"Column Contents Type:  {type(column_contents.values)}")
        print(f"Column Contents array index:  {column_contents.values[0]}")
        print(f"Column Contents array index type:  {type(column_contents.values[0])}")
        if column_contents.values[0] is numpy.bool_(True):
            print("Working the shift!")
            greg_shifts_list.append(column_name)
    print(greg_shifts_list)
    print()
