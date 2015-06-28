#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd $env(HOME)/.fits/fits\n"
send "./fits.sh -h\n"
interact

