#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# testmodule.py
#
"""Simple TestModeule"""

#import argparse
import logging
#import shlex
#import subprocess
import os
import sys
#import time

from os.path import exists

#import yaml

#import rtmidi
#from rtmidi.midiutil import open_midiport
#from rtmidi.midiconstants import *

device = "./mdb.py"
sys.path.append(os.path.abspath(device))
from device import *

log = logging.getLogger('test')

def main(args=None):

    logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s", level=logging.DEBUG)

    try:
        sd = SD90()
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    try:
        log.debug(sd.name)
        sd.bank_select(1,99,6,126)
        sd.play_note(1, 64,100,1)
        #sd.all_note_off()
    except KeyboardInterrupt:
        print('')
    finally:
        sd.dispose()
        del sd

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
