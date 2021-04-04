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


# define the file constants
file = create_constants(
    "file",
    Env=".env",
)

# The defined levels, in order of increasing severity, are as follows:
#
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL

# define the logging constants
logging = create_constants(
    "logging",
    Default_Logging_Level="ERROR",
    Format="%(message)s",
    Rich="Rich",
)

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

# define constants for the progress bars
progress = create_constants("progress", Small_Step=0.2, Medium_Step=0.4, Large_Step=0.6)

# define constants for the various sizes
size = create_constants("size", Tab=4)

# define the terminology used for spreadsheets
sheets = create_constants(
    "sheets",
    Default="Sheet1",
    Name="Individual Name",
    Name_Prompt="individual's name",
    Number="Individual Phone Number",
)
