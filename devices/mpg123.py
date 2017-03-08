#!/usr/bin/env python
#-*- coding: utf-8 -*-

import subprocess

class Player(object):
    def __init__(self):
        print "Initializing mpg123 player in Remote Mode..."
        self._play=subprocess.Popen(['mpg123', '-q', '-R'], stdin=subprocess.PIPE)
        self._play.stdin.write('silence\n')

    def execute_command(self, value):
        self._play.stdin.write(' '.join(value[1:]) + '\n')

    def dispose(self):
        self._play.terminate()
