#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd /home/bcadmin/Tools/bagit-4.9.0/bin\n"
send "./bag\n"
interact

