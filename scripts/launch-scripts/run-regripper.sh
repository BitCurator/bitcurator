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
send "cd /usr/share/regripper\n"
send "perl rip.pl\n"
interact
exit
