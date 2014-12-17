#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd /home/bcadmin/Tools/bagger-2.1.3\n"
send "./bagger.sh -h\n"
interact

