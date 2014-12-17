#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd /home/bcadmin/Tools/fits\n"
send "./fits.sh -h\n"
interact

