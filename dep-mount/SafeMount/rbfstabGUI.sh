#!/bin/bash
#: Title    : rbfstabGUI
#: Author   : "John Lehr" <slo.sleuth@gmail.com>
#: Date     : 09/18/2012
#: Version  : 0.1.0
#: Desc     : a gui to activate or deactivate rbfstab

get_mount_policy()
{
    if [ -e /etc/udev/rules.d/fstab.rules ]
    then
        ro="<span size='x-large'>System mounting policy: \
    <b><u>READ-ONLY</u></b></span>"
    else 
        ro="<span size='x-large'>System mounting policy: \
    <span foreground='red'><b><u>WRITEABLE</u></b></span></span>"
    fi
}


flash_status()
{
    get_mount_policy
    yad \
        --image=gtk-harddisk \
        --image-on-top \
        --undecorated \
        --text="$ro" \
        --no-buttons \
        --timeout=3
}

make_writeable()
{
    instructions="<span size='x-large' foreground='red'>\
    <b><u>WARNING</u></b></span>\n
    You are about to make devices <span color='red'><b>WRITEABLE</b></span>.\n
    Are you sure you want to continue?"
    
    yad \
        --window-icon=gtk-harddisk \
        --image=gtk-dialog-warning \
        --text="$instructions" \
        --button=gtk-yes:0 \
        --button=gtk-cancel:1

    case $? in
        0) sudo rbfstab -r ;;
        1) flash_status; exit 0 ;;
    esac

    flash_status
}

## MAIN SCRIPT

#Get current policy
get_mount_policy

#Text for main dialog box
instructions="$ro \n
Changing the system mount policy will affect all
subsequent mounts.  Currently mounted devices will
not be affected.\n
Make a selection below:"

#Main dialog box
yad \
    --window-icon=gtk-harddisk \
    --image=gtk-harddisk \
    --title="Change Mount Policy" \
    --text="$instructions" \
    --button="Writeable":2 \
    --button=gtk-cancel:1 \
    --button="Read-Only":0 

case $? in
    0) sudo rbfstab -i; #install rbfstab
        flash_status;;
    1)  flash_status
        exit 0;; #Exit on cancel
    2) make_writeable;; #remove rbfstab
esac
mounter_menuapp
