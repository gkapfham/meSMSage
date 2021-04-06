"""Configuration file for the test suite."""

import os
import sys

GO_BACK_A_DIRECTORY = "/../"

PROJECT_DIRECTORY = "meSMSage"

# set the system path to contain the previous directory
# Example: /home/gkapfham/working/source/meSMSage/meSMSage/tests/../
PREVIOUS_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PREVIOUS_DIRECTORY + GO_BACK_A_DIRECTORY)

# set the system path to contain the project directory
# /home/gkapfham/working/source/meSMSage/meSMSage/tests/../meSMSage
sys.path.insert(0, PREVIOUS_DIRECTORY + GO_BACK_A_DIRECTORY + PROJECT_DIRECTORY)
print(sys.path)

from mesmsage import configure  # noqa: E402
from mesmsage import constants  # noqa: E402

configure.configure_tracebacks()
_ = configure.configure_logging(constants.logging.Error)
