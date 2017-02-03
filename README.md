# python-midicommander

# Tested on a Raspberry Pi

Started from : https://github.com/SpotlightKid/python-rtmidi
https://github.com/SpotlightKid/python-rtmidi/tree/master/examples/midi2command

With the script above we can execute external gnu/linux command via a midi message. 
It work with a config file in YAML format and the external command is a Popen call.
Read and understand the script before use mine.

I use the midi2command logic but added few functions for my own needs in music :
  - Can call internal method from a midi message, in my script we can control the camera module
  - TODO : Can control a DAW object in progress under classes directory
