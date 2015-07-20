#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd /usr/share/regripper\n"
send "perl rip.pl\n"
interact

