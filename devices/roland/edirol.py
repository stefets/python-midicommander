#!/usr/bin/env python
# -*- coding: utf-8 -*-

from devices.generic import mdb

#Model : Edirol SD-90
class SD90(mdb.MidiDeviceBase):
#
# From python-rtmidi
#[0] Midi Through:Midi Through Port-0 14:0
#[1] SD-90:SD-90 Part A 20:0
#[2] SD-90:SD-90 Part B 20:1
#[3] SD-90:SD-90 MIDI 1 20:2 *****
#[4] SD-90:SD-90 MIDI 2 20:3 *****

    def __init__(self):
        super(SD90, self).__init__('Roland Edirol SD-90 StudioCanvas')
        self.midi_in_1 = self.midi_out_1 = 3
        self.midi_in_2 = self.midi_out_2 = 4

    def open_midi_in_2(self):
        return mdb.MidiPort(self.midi_in_2, "input")

    def open_midi_out_2(self):
        return mdb.MidiPort(self.midi_out_2, "output")

class TD20(mdb.MidiDeviceBase):

    def __init__(self):
        super(TD20, self).__init__('Roland TD-20')
