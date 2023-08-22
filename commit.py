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

if os.name == 'nt':
    SETUP_GPTCOMMIT="cmd /C setup_gptcommit.cmd"
else:
    SETUP_GPTCOMMIT="bash setup_gptcommit.sh"

# setup timezone as Shanghai
