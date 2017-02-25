#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# device.py
# Stephane Gagnon
# www.pacificweb.ca
"""Represent a hardware DAW or a USB MIDI DEVICE """

#import argparse
import logging
import sys
#import threading
import time

import rtmidi
from rtmidi.midiutil import open_midiport
from rtmidi.midiconstants import *

log = logging.getLogger("device")

#Base class for a midi device
class MidiDeviceBase(object):
    def __init__(self, name='Generic MIDI IN/OUT'):

        self.name = name

        # Internal MIDI Through Port (Check and adjust for your system)
        self.midi_through = self.midi_in_1 = self.midi_out_1 = 0

        self.MIDI_THROUGH = self.open_midi_through()
		
    def reset(self):
        raise NotImplementedError("Abstract method 'reset()'.")

    def open_midi_through(self):
        port, port_name  = open_midiport(self.midi_through, "output")
        return port
        
    def open_midi_in_1(self):
        return open_midiport(self.midi_in_1, "input")

    def open_midi_out_1(self):
        return open_midiport(self.midi_out_1, "output")

    def close_port(self, port):
        port.close_port()
        del port

    def play_note(self, channel=None, note=None, velocity=100, duration=1):
        Note(self.MIDI_THROUGH, channel, note, velocity, duration).play()

    def all_note_off(self):
        for channel in range(1,16):
            self.message=[CONTROLLER_CHANGE + channel, 120, 0]
            self.MIDI_THROUGH.send_message(self.message)

    def bank_select(self, channel, msb=None, lsb=None, program=None):
        BankSelect(self.MIDI_THROUGH, channel, msb, lsb, program).send()
        time.sleep(0.1)  # give time for the MIDI device to process the bank change

    def dispose(self):
        log.debug("Dispose")
        self.close_port(self.MIDI_THROUGH)

#Model : Edirol SD-90
class SD90(MidiDeviceBase):

    def __init__(self):
        super(SD90, self).__init__('Edirol SD-90 StudioCanvas')
        self.midi_in_1 = self.midi_out_1 = 2 # must match aconnect
        self.midi_in_2 = self.midi_out_2 = 3 # must match aconnect

    def open_midi_in_2(self):
        return open_midiport(self.midi_in_1, "input")

    def open_midi_out_2(self):
        return open_midiport(self.midi_out_2, "output")

# Common

# Note object
class Note(object):
    def __init__(self, midiout, channel=None, note=None, velocity=100, duration=1):

        self.midiout = midiout
        channel -= 1
        self.note_on = [NOTE_ON + channel, note, velocity]
        self.note_off = [NOTE_OFF + channel, note, 0]

        if duration is None:
            self.duration = 1
        else:
            self.duration = duration

        if velocity is None:
            velocity = 100

    def play(self):
        """Play the note."""
        self.midiout.send_message(self.note_on)
        time.sleep(self.duration) # note length
        self.midiout.send_message(self.note_off)

# BankSelect object
class BankSelect(object):
    def __init__(self, midiout, channel=None, msb=None, lsb=None, program=None):

        self.midiout = midiout
        channel-=1
        program-=1

        self.cc0=[CONTROLLER_CHANGE+channel, BANK_SELECT, msb]
        self.cc32=[CONTROLLER_CHANGE+channel, BANK_SELECT_LSB,lsb]
        self.programchange=[PROGRAM_CHANGE+channel, program]

    # Send a bank select
    def send(self):
        self.midiout.send_message(self.cc0)
        self.midiout.send_message(self.cc32)
        self.midiout.send_message(self.programchange)
