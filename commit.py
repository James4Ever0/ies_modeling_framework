# this file shall be identical anywhere else.
import pytz
import datetime
import os
import sys
import tkinter
import subprocess
# on windows nt, alert us (using tkinter or native api?) if commit has failed.
# on other platforms, please improvise.

CHECK_GPTCOMMIT_KEYS="gptcommit config keys"

# setup timezone as Shanghai
