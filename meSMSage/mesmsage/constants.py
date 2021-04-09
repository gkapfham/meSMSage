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


# define the environment constants
environment = create_constants(
    "environment",
    Twilio_Phone_Number="TWILIO_PHONE_NUMBER",
)

# define the files constants
files = create_constants(
    "file",
    Env=".env",
)

# define the locales constants
locales = create_constants(
    "locales",
    Us="US",
)

# The defined logging levels, in order of increasing severity, are as follows:
#
# DEBUG
# INFO
# WARNING
# ERROR
# CRITICAL

# define the logging constants
logging = create_constants(
    "logging",
    Debug="DEBUG",
    Info="INFO",
    Warning="WARNING",
    Error="ERROR",
    Critical="CRITICAL",
    Default_Logging_Level="ERROR",
    Format="%(message)s",
    Rich="Rich",
)

# define the markers for files and output
markers = create_constants(
    "markers",
    All_Individuals="All Individuals",
    Empty=b"",
    Indent="  ",
    In_A_File="in a file",
    Newline="\n",
    Nothing="",
    Space=" ",
)

# define the terminology for using pandas
dataframes = create_constants(
    "dataframes",
    Index="index",
    List="list",
)

# define constants for the progress bars
progress = create_constants("progress", Small_Step=0.2, Medium_Step=0.4, Large_Step=0.6)

# define constants for the various sizes
sizes = create_constants("size", First=0, Singleton=1, Tab=4)

# define the terminology used for spreadsheets
sheets = create_constants(
    "sheets",
    Default="Sheet1",
    Name="Individual Name",
    Name_Prompt="individual's name",
    Number="Individual Phone Number",
)
