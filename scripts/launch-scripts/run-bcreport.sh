#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd ~/\n"
send "python3 /home/bcadmin/Tools/bitcurator/python/generate_report.py -h\n"
interact

