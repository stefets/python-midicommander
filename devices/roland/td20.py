#!/usr/bin/env python
# -*- coding: utf-8 -*-

from devices.generic import mdb

class TD20(mdb.MidiDeviceBase):

    def __init__(self):
        super(TD20, self).__init__('Roland TD-20')
