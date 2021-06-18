#!/bin/sh
free -t | gawk 'NR == 2 {printf "%.1f%%\n", $3/$2*100}'
