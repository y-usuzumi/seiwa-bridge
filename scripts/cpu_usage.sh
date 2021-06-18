#!/bin/sh
top -bn 2 -d 0.01 | grep '^%Cpu' | tail -n 1 | gawk '{printf "%.1f%%\n", $2+$4+$6}'
