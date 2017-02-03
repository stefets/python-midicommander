#/bin/bash

# Need SOX
# Play filename on a specific audio harware
# ADJUST AUDIODEV to your needs

filename=$1
if [ -e $filename ]
then
	AUDIODEV=hw:1,0 play $1
fi
