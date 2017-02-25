#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

class Player(object):
    def __init__(self):
        print "Initializing mpg123 player in Remote Mode..."
        self._play=subprocess.Popen(['mpg123', '-a', 'hw:1,0', '-q', '-R'], stdin=subprocess.PIPE)
        self._play.stdin.write('silence\n')

    def execute_command(self, value):
        x=get_ms_time()
        self._play.stdin.write(' '.join(value[1:]) + '\n')
        print get_ms_time() - x

    def dispose(self):
        self._play.terminate()
