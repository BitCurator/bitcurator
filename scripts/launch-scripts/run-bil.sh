#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd $HOME/.bagit/bagit-4.10.0/bin\n"
send "./bag\n"
interact

