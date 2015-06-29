#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd ~/\n"
send "python3 /usr/share/dfxml/python/identify_filenames.py -h\n"
interact

