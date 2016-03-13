#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd $env(HOME)/.bagit/bagit-4.10.0/bin\n"
send "./bag\n"
interact

