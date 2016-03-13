#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "bagit.py --help\n"
interact

