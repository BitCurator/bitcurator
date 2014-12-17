#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd ~/\n"
send "python3 /home/bcadmin/Tools/bitcurator/python/bc_reports_tab.py -h\n"
interact

