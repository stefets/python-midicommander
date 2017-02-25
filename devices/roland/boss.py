#!/usr/bin/env python
# -*- coding: utf-8 -*-

from devices.generic import mdb

class GT10(mdb.MidiDeviceBase):
    def __init__(self):
        super(GT10, self).__init__('Boss GT10 Multi Effects')
class GT10B(mdb.MidiDeviceBase):
    def __init__(self):
        super(GT10B, self).__init__('Boss GT10B Multi Effects')
class GT100(mdb.MidiDeviceBase):
    def __init__(self):
        super(GT100, self).__init__('Boss GT100 Multi Effects')
