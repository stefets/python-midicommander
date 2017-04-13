#!/bin/bash

# Connect SD-90 Midi Through to the specified client or default client (0)

# Client 0 = SD-90 Part A
# Client 1 = SD-90 Part B

# Disconnect Thru
aconnect -d 14:0 20:0
aconnect -d 14:0 20:1

client=0	# Default

#if [[ $1 =~ ^[0-1]+$ ]]
#then
#	client=$1
#fi	

aconnect 14:0 20:$client
aconnect -l
