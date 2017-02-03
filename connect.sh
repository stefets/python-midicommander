#!/bin/bash

# Connect SD-90 MIDI-IN 1 TO SD-90 PART A and SD-90 MIDI-IN 2 TO SD-90 PART B

aconnect -x
aconnect 20:2 20:0
aconnect 20:3 20:1
aconnect -l
