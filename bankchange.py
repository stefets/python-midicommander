#!usr/bin/env python
#
# bankchange.py
# Stephane Gagnon
# Shows how to send bank select cc0, cc32, pc and optionally send a note, velocity and variation
#

import argparse
import logging
import sys
import time

import rtmidi
from rtmidi.midiutil import open_midiport
from rtmidi.midiconstants import *

log = logging.getLogger('bankchange')

# Message Container
class MidiMessage(object):
    def __init__(self, channel=None):

        self.Channel = channel-1

    def AllNoteOff(self):
        self.AllNoteOff=[CONTROLLER_CHANGE+self.Channel, 120, 0] 
        MidiOut.send_message(self.AllNoteOff)
        
    def BankSelect(self, msb=None, lsb=None, program=None):
        bank = BankSelect(self.Channel, msb, lsb, program)  
        bank.Send()
        del bank

    def SendNote(self, note=None, velocity=100, duration=1):
        _note = Note(self.Channel, note,velocity, duration)
        _note.Play()
        del _note

# Note object
class Note(object):
    def __init__(self, channel=None, note=None, velocity=100, duration=1):

        if duration is None: 
            self.Duration=1
        else:
            self.Duration=duration

        if velocity is None: 
            velocity=100

        self.Note_On = [NOTE_ON+channel, note, velocity]
        self.Note_Off = [NOTE_OFF+channel, note, 0]

    # Play the note
    def Play(self):
        MidiOut.send_message(self.Note_On)
        time.sleep(self.Duration) # note length
        MidiOut.send_message(self.Note_Off)

# Bank Select object
class BankSelect(object):
    def __init__(self, channel=None, msb=None, lsb=None, program=None):

        self.Channel=channel
        self.ProgramNumber=program-1
        self.MSB=msb
        self.LSB=lsb

        self.CC0=[CONTROLLER_CHANGE+self.Channel, BANK_SELECT, self.MSB] 
        self.CC32=[CONTROLLER_CHANGE+self.Channel, BANK_SELECT_LSB,self.LSB] 
        self.ProgramChange=[PROGRAM_CHANGE+self.Channel, self.ProgramNumber]

    # Send a bank change
    def Send(self):
        MidiOut.send_message(self.CC0)
        MidiOut.send_message(self.CC32)
        MidiOut.send_message(self.ProgramChange)
        time.sleep(0.1)  # give time for the MIDI device to process the bank change

def main(args=None):
#
#    Main program function.
#

    parser = argparse.ArgumentParser(description='BankChange Script')
    parser.add_argument('-p',  '--port', dest='port',
        help='MIDI output port name or number (default: open virtual input)')
    parser.add_argument('-v',  '--verbose', action="store_true",
        help='verbose output')
    parser.add_argument('-c',  '--channel', dest='channel', type=int,
        help='Channel number 1-16')
    parser.add_argument('-m',  '--msb', dest='msb', type=int,
        help='MSB Value')
    parser.add_argument('-l',  '--lsb', dest='lsb', type=int,
        help='LSB Value')
    parser.add_argument('-pc',  '--program', dest='program', type=int,
        help='Program Change')
    parser.add_argument('-n',  '--note', dest='note', type=int,
        help='Note Value')
    parser.add_argument('-vel',  '--velocity', dest='velocity', type=int,
        help='Note velocity, default=100')
    parser.add_argument('-d',  '--duration', dest='duration', type=int,
        help='Note duration, default=1')

    args = parser.parse_args(args if args is not None else sys.argv[1:])
    print(args)

    logging.basicConfig(format="%(name)s: %(levelname)s - %(message)s",
        level=logging.DEBUG if args.verbose else logging.WARNING)

    try:
        global MidiOut 
	MidiOut, port_name = open_midiport(args.port, "output")
    except (EOFError, KeyboardInterrupt):
        sys.exit()

    #log.info("Sending message out...")

    try:
        message = MidiMessage(args.channel)
        message.AllNoteOff()
        message.BankSelect(args.msb, args.lsb, args.program) 
        if args.note is not None:
            message.SendNote(args.note, args.velocity, args.duration)
        del message
    except:
        print "Unexpected error:", sys.exc_info()[0]
    finally:
        print('Done')
        MidiOut.close_port()
        del MidiOut

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
