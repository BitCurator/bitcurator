#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd ~/\n"
send "cdrdao\n"
interact

