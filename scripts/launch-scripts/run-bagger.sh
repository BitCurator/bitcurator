#!/usr/bin/expect -f

spawn -noecho bash
expect "$ "
send "cd $env(HOME)/.bagger/bagger-2.1.3\n"
send "./bagger.sh -h\n"
interact

