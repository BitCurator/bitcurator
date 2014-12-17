#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd ~/\n"
send "ddrescue --help\n"
interact

