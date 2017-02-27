#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pyglet
#import wave
from devices.midi import mdb

#Model : Edirol SD-90
# From python-rtmidi
#[0] Midi Through:Midi Through Port-0 14:0
#[1] SD-90:SD-90 Part A 20:0
#[2] SD-90:SD-90 Part B 20:1
#[3] SD-90:SD-90 MIDI 1 20:2 *****
#[4] SD-90:SD-90 MIDI 2 20:3 *****
class SD90(mdb.MidiDeviceBase):
    def __init__(self):
        super(SD90, self).__init__('Roland Edirol SD-90 StudioCanvas')
        self.midi_in_1 = self.midi_out_1 = 3
        self.midi_in_2 = self.midi_out_2 = 4

        pyglet.options['audio'] = ('pulse', 'silent')
        self.media_player = pyglet.media.Player()

    def open_midi_in_2(self):
        return mdb.MidiPort(self.midi_in_2, "input")

    def open_midi_out_2(self):
        return mdb.MidiPort(self.midi_out_2, "output")

    def execute(self, args):
        if args[0] == "bankselect":
            self.bank_select(int(args[1]),int(args[2]),int(args[3]),int(args[4]))
        elif args[0] == "loadstream":
            self.loadstream(args[1])
        elif args[0] == "play":
            self.play()
        elif args[0] == "pause":
            self.pause()
        else:
            return

    def loadstream(self,_filename, _start=False):
        self.media_player.queue(pyglet.media.load(_filename, streaming=False))

    def play(self):
        self.media_player.play()

    def pause(self):
        self.media_player.pause()

    def close(self):
        if self.media_player is None:
            return
        if self.media_player.playing:
            self.pause()
        self.media_player.delete()
