#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd ~/\n"
send "python3 /home/bcadmin/Tools/bulk_extractor/python/identify_filenames.py -h\n"
interact

