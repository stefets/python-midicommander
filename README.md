# python-midicommander

# Tested on a Raspberry Pi

# Execute external process or control RPI camera or control a process that can get stdin input when specific MIDI message is received.

Started from : https://github.com/SpotlightKid/python-rtmidi
  - https://github.com/SpotlightKid/python-rtmidi/tree/master/examples/midi2command

With the script above we can execute external gnu/linux command via a midi message. 
It work with a config file in YAML format and the external command is a Popen call.
Read and understand the script before use mine.

I use the midi2command logic but added few functions for my own needs in music :
  - Check branch evolution for latest commits
