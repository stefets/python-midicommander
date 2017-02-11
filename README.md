# python-midicommander

# Tested on a Raspberry Pi

# Execute external process or control RPI camera or control a process that can get stdin input when specific MIDI message is received.

Started from : https://github.com/SpotlightKid/python-rtmidi
https://github.com/SpotlightKid/python-rtmidi/tree/master/examples/midi2command

With the script above we can execute external gnu/linux command via a midi message. 
It work with a config file in YAML format and the external command is a Popen call.
Read and understand the script before use mine.

I use the midi2command logic but added few functions for my own needs in music :
  - Can call internal method from a midi message, in my script we can control the camera module
  - TODO : Can control a DAW object (in progress under classes directory)
  - Under classes directory there is a base class for a Midi Device (DAW) and a class for the Edirol SD-90 that inherit the base class)
  - TODO : Send reset sysex to SD-90
