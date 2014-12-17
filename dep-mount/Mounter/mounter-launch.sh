#!/bin/bash
#: Title    : mounter-launch.sh
#: Author   : "John Lehr" <slo.sleuth@gmail.com>
#: Date     : 09/28/2012
#: Version  : 0.2.2
#: Desc     : mount device(s) selected by user
#: Options  : none

R="<span foreground='red'>"
G="<span foreground='dark green'>"
E="</span>"

# Launch Mounter
sudo mounter &

# Provide Instructions
TEXT="<b>Mounter</b> is a disk mounting application that runs in the system tray.

<u>General Information:</u>

A ${G}green${E} disk icon means the system is ${G}SAFE${E} and will mount devices ${G}READ-ONLY${E}.
A ${R}red${E} disk icon means ${R}WARNING${E}, mounted devices will be ${R}WRITEABLE${E}.

<u>Instructions:</u>

<i>Left-click</i> the disk icon to mount a device.
<i>Right-click</i> the disk icon to change the system mount policy.
<i>Middle-click</i> will close the mounter application.  Relaunch from the menu.

<b><i>Currenly mounted devices will not be affected by mount policy changes.
Only subsequent mounting operations will be affected.</i></b>"

yad --title=Mounter --window-icon=gtk-harddisk --image=gtk-harddisk \
    --text="$TEXT" --button=gtk-ok
