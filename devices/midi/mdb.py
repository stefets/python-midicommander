#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time
from os.path import basename
from random import uniform
from random import randint

import rtmidi
from rtmidi.midiutil import open_midiport
from rtmidi.midiconstants import *

log = logging.getLogger("device")

SYSTEM_EXCLUSIVE = b'\xF0'
END_OF_EXCLUSIVE = b'\xF7'

class MidiPort(object):
    def __init__(self, _id=None, _kind=None):

        self.port, self.port_name = open_midiport(_id, _kind)
    
    def close(self):
        self.port.close_port()

#Base class for a midi device
class MidiDeviceBase(object):
    def __init__(self, name='Generic MIDI IN/OUT'):

        self.name = name
        self.midi_in_1 = self.midi_out_1 = 1
        self.midi_thru = self.open_midi_thru()
		
    def send_sysex(self, filename, delay=50):

        bn = basename(filename)
        with open(filename, 'rb') as sysex_file:

            data = sysex_file.read()

            if data.startswith(SYSTEM_EXCLUSIVE):

                sox = 0
                i = 0

                while sox >= 0:
                    sox = data.find(SYSTEM_EXCLUSIVE, sox)
    
                    if sox >= 0:
                        eox = data.find(END_OF_EXCLUSIVE, sox)
    
                        if eox >= 0:
                            sysex_msg = data[sox:eox + 1]
                            # Python 2: convert data into list of integers
                            if isinstance(sysex_msg, str):
                                sysex_msg = [ord(c) for c in sysex_msg]
    
                            log.info("Sending '%s' message #%03i...", bn, i)
                            self.midi_thru.port.send_message(sysex_msg)
                            time.sleep(0.001 * delay)
    
                            i += 1
                        else:
                            break
    
                        sox = eox + 1
            else:
                log.warning("File '%s' does not start with a sysex message.", bn)

    def open_midi_thru(self):
        return MidiPort(0, "output")

    def open_midi_in_1(self):
        return MidiPort(self.midi_in_1, "input")

    def open_midi_out_1(self):
        return MidiPort(self.midi_out_1, "output")

    def play_note(self, channel=None, note=None, velocity=100, duration=1):
        note=Note(self.midi_thru.port, channel, note, velocity, duration)
        note.play()

    def all_note_off(self):
        for channel in range(1,16):
            self.message=[CONTROLLER_CHANGE + channel, 120, 0]
            self.midi_thru.port.send_message(self.message)

    def bank_select(self, channel, msb=None, lsb=None, program=None):
        bs=BankSelect(self.midi_thru.port, channel, msb, lsb, program)
        bs.send()

    def random(self):
        for p in range(1,10):
            v=randint(20,100)
            self.play_note(1,v,100,uniform(0.1,0.5))

    def dispose(self):
        log.debug("Dispose")
        self.midi_thru.close()

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

    def send(self):
        self.midiout.send_message(self.cc0)
        self.midiout.send_message(self.cc32)
        self.midiout.send_message(self.programchange)
        time.sleep(0.1)  # give time for the MIDI device to process the bank change
