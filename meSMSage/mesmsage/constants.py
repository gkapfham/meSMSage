"""Define constants for use in meSMSage."""

import collections
import itertools


def create_constants(name, *args, **kwargs):
    """Create a namedtuple of constants."""
    # the constants are created such that:
    # the name is the name of the namedtuple
    # for *args with "Constant_Name" or **kwargs with Constant_Name = "AnyConstantName"
    # note that this creates a constant that will
    # throw an AttributeError when attempting to redefine
    new_constants = collections.namedtuple(name, itertools.chain(args, kwargs.keys()))
    return new_constants(*itertools.chain(args, kwargs.values()))


# define the markers for files and output
markers = create_constants(
    "markers",
    Empty=b"",
    Indent="  ",
    In_A_File="in a file",
    Newline="\n",
    Nothing="",
    Space=" ",
)

# define the terminology used for spreadsheets
sheets = create_constants(
    "sheets",
    DEFAULT="Sheet1",
)
