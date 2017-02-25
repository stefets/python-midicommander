#!/usr/bin/env python
# -*- coding: utf-8 -*-

from devices.midi import mdb

class GT10Base(mdb.MidiDeviceBase):
	def __init__(self):

class GT10(GT10Base):
    def __init__(self):
        super(GT10, self).__init__('Boss GT10 Multi Effects')

class GT10B(GT10Base):
    def __init__(self):
        super(GT10B, self).__init__('Boss GT10B Multi Effects')

class GT100(mdb.MidiDeviceBase):
    def __init__(self):
        super(GT100, self).__init__('Boss GT100 Multi Effects')
