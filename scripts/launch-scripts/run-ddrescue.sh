#!/usr/bin/expect -f

#trap sigwinch and pass it to the child we spawned
#this allows the gnome-terminal window to be resized
trap {
 set rows [stty rows]
 set cols [stty columns]
 stty rows $rows columns $cols < $spawn_out(slave,name)
} WINCH

set arg1 [lindex $argv 0]

spawn -noecho bash
expect "$ "
send "cd ~/\n"
send "ddrescue --help\n"
interact
exit
