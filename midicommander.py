#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Started from : https://github.com/SpotlightKid/python-rtmidi
# https://github.com/SpotlightKid/python-rtmidi/tree/master/examples/midi2command
#

import argparse
import logging
import shlex
import subprocess
import sys
import uuid
import random
import yaml

from os.path import exists

import rtmidi
from rtmidi.midiutil import open_midiport
from rtmidi.midiconstants import *

from devices import pi_camera
from devices import mpg123
from devices.midi.roland import edirol

import time
get_ms_time = lambda: int(round(time.time() * 1000))

try:
    from functools import lru_cache
except ImportError:
    # Python < 3.2
	lru_cache = lambda : lambda func: func

log = logging.getLogger('midi2command')

STATUS_MAP = {
    'noteon': NOTE_ON,
    'noteoff': NOTE_OFF,
    'controllerchange': CONTROLLER_CHANGE
}
#STATUS_MAP = {
#    'noteon': NOTE_ON,
#    'noteoff': NOTE_OFF,
#    'programchange': PROGRAM_CHANGE,
#    'controllerchange': CONTROLLER_CHANGE,
#    'pitchbend': PITCH_BEND,
#    'polypressure': POLY_PRESSURE,
#    'channelpressure': CHANNEL_PRESSURE
#}

class InternalCommand(object):
    def __init__(self, args=None, data1=None, data2=None):
        #TODO    
        for arg in args:
            print arg
        print data1
        print data2

class Command(object):
    def __init__(self, name='', description='', status=0xB0, channel=None, data=None, command=None):
        self.name = name
        self.description = description
        self.status = status
        self.channel = channel
        self.command = command

        if data is None or isinstance(data, int):
            self.data = data
        elif hasattr(data, 'split'):
            self.data = map(int, data.split())
        else:
            raise TypeError("Could not parse 'data' field.")

class MidiInputHandler(object):
    def __init__(self, port, config, _camera, _player, _daw):
        self.port = port
        self.commands = dict()
        self.load_config(config)
        if _player is not None:
            self.player = _player
        if _camera is not None:
            self.camera = _camera
        if _daw is not None:
            self.daw = _daw

    def __call__(self, _event, data=None):
        x=get_ms_time()
        event, deltatime = _event

        if event[0] < 0xF0:
            channel = (event[0] & 0xF) + 1
            status = event[0] & 0xF0
        else:
            status = event[0]
            channel = None

        data1 = data2 = None
        num_bytes = len(event)

        if num_bytes >= 2:
            data1 = event[1]
        if num_bytes >= 3:
            data2 = event[2]

        # Look for matching command definitions
        print "Before lookup : " + str(get_ms_time() - x)
        cmd = self.lookup_command(status, channel, data1, data2)
        print "After lookup : " + str(get_ms_time() - x)

        if cmd:
            cmdline = cmd.command % dict(
                channel=channel,
                data1=data1,
                data2=data2,
                status=status)
            self.execute_command(cmdline, data1, data2)
            print get_ms_time() - x

        # For optimisation, display info after execution
        #log.debug("[%s] %r", self.port, event)

    @lru_cache()
    def lookup_command(self, status, channel, data1, data2):
        for cmd in self.commands.get(status, []):
            if channel is not None and cmd.channel != channel:
                continue

            if (data1 is None and data2 is None) or cmd.data is None:
                return cmd
            elif isinstance(cmd.data, int) and cmd.data == data1:
                return cmd
            elif (isinstance(cmd.data, (list, tuple)) and cmd.data[0] == data1 and cmd.data[1] == data2):
                return cmd

    # Execute command set in config file
    def execute_command(self, cmdline, data1, data2):
        try:
            args = shlex.split(cmdline)
            log.info("Calling command: %s", cmdline)
            if args[0] == "external":
                subprocess.Popen(args[1:])
            elif args[0] == "internal":
                self.execute_internal_command(args, data1, data2)
            elif args[0] == "mpg123" and self.player is not None:
                self.player.execute_command(args)
            elif args[0] == "bankselect" and self.daw is not None:
                self.daw.bank_select(int(args[1]),int(args[2]),int(args[3]),int(args[4]))
            elif args[0] == "camera" and self.camera is not None:
                self.camera.execute(data1, data2)
            else:
                subprocess.Popen(args)
        except:
            log.exception("Error calling method execute_command.")

    def execute_internal_command(self, args, data1, data2):
        return

    def load_config(self, filename):
        if not exists(filename):
            raise IOError("Config file not found: %s" % filename)

        with open(filename) as patch:
            data = yaml.load(patch)

        for cmdspec in data:
            print(cmdspec)
            try:
                if isinstance(cmdspec, dict) and 'command' in cmdspec:
                    cmd = Command(**cmdspec)
                elif len(cmdspec) >= 2:
                    cmd = Command(*cmdspec)
            except (TypeError, ValueError) as exc:
                log.debug(cmdspec)
                raise IOError("Invalid command specification: %s" % exc)
            else:
                status = STATUS_MAP.get(cmd.status.strip().lower())

                if status is None:
                    try:
                        int(cmd.status)
                    except:
                        log.error("Unknown status '%s'. Ignoring command",
                            cmd.status)

                log.debug("Config: %s\n%s\n", cmd.name, cmd.description)
                self.commands.setdefault(status, []).append(cmd)

def main(args=None):

    parser = argparse.ArgumentParser(description='midicommander')

    parser.add_argument('-v',  '--verbose', action="store_true",
        help='verbose output')

    parser.add_argument('-m', '--mpg123', action="store_true",
        help='open mpg123 in Remote Mode (-R) and listen stdin for commands')

    parser.add_argument('-c', '--camera', action="store_true",
        help='enable camera')

    parser.add_argument(dest='config', metavar="CONFIG",
        help='Configuration file in YAML syntax.')

    args = parser.parse_args(args if args is not None else sys.argv[1:])

    logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s",
		level=logging.DEBUG if args.verbose else logging.WARNING)

    # PLUGINS 
    play = None
    cam = None

    if args.camera:
        log.info("Starting RPI Camera Module...")
        cam = pi_camera.Camera()

    if args.mpg123:
        log.info("Starting mpg123 process in Remote Mode...")
        play=mpg123.Player()

    # MIDI 
    daw=edirol.SD90()
    log.info(daw.name)
    try:
        midiin1 = daw.open_midi_in_1()
        midiin2 = daw.open_midi_in_2()
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    # MIDI CALLBACK AND PASS PLUGINS POINTER
    log.info("Attaching MIDI input callback handler.")
    midiin1.port.set_callback(MidiInputHandler(midiin1.port_name, args.config, cam, play, daw))
    midiin2.port.set_callback(MidiInputHandler(midiin2.port_name, args.config, cam, play, daw))

    log.info("Entering main loop. Press Ctrl-C to exit")
    try:
        # just wait for keyboard interrupt in main thread
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('')
    finally:
        log.info("Exiting main thread")
        midiin1.close()
        midiin2.close()
        daw.dispose()
        del daw
        del midiin1
        del midiin2
        if cam is not None:
            cam.dispose()
            del cam
        if play is not None:
            play.dispose()
            del play
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
