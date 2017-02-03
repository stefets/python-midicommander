#/bin/bash

# Need SOX
# Play filename on a specific audio harware
# ADJUST AUDIODEV for your needs

filename=$1
if [ -e $filename ]
then
	kill -9 $(pgrep play) 2>/dev/null
	AUDIODEV=hw:1,0 play $1
fi
