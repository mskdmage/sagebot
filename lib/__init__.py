"""SageBot automation library initialization.

This module provides the main components for browser, GUI, and file automation.
"""

from .bot import SageBot
from .utils import print_banner
from . import browser
from . import gui
from . import files

print_banner()