#!/bin/bash 

# TODO switch
exit 1
sudo umount /mnt/flash
sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt/flash
