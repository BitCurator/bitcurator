#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd $HOME/.fits/fits\n"
send "./fits.sh -h\n"
interact

