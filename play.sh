#/bin/bash

# Need SOX
# Play filename on a specific audio harware
# ADJUST AUDIODEV for your needs

#export AUDIODEV=hw:1,0
if [ -e $filename ]; then play -q $1; fi
