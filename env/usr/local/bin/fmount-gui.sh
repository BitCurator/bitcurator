#!/bin/bash
#:fmount-gui
# by John Lehr - slo.sleuth@gmail.com - http://linuxsleuthing.blogspot.com 
# touched by Nanni Bassetti - http://www.nannibassetti.com - digitfor@gmail.com
# version 1.00 

check_cancel()
{
	if [ $? -gt 0 ]; then
		exit 1
	fi
}

if [ "$(id -ru)" != "0" ];then
	gksu -k -S -m "Enter root password to continue" -D "fmount-gui requires root user priveleges to mount disk images." echo
fi

image_files="$(yad --file-selection \
	--multiple \
	--height 400 \
	--width 600 \
	--title "fmount: Disk Image Selection" \
	--text " If image is split, select all image segments (shift-click).\n")"
check_cancel



image_files="$(echo $image_files | tr "|" " ")"



sudo bash fmount.sh $image_files 

if [ $? = 0 ]; then
	yad  --width 600 \--title "fmount" --text "Operation succeeded!\n\nYour disk is mounted"
else
	yad --width 600 --title "fmount" --text "fmount encountered errors.\n\nPlease check your settings and try again"
fi
