# bitcurator-distro-main

[![GitHub issues](https://img.shields.io/github/issues/bitcurator/bitcurator-distro-main.svg)](https://github.com/bitcurator/bitcurator-distro-main/issues)
[![GitHub forks](https://img.shields.io/github/forks/bitcurator/bitcurator-distro-main.svg)](https://github.com/bitcurator/bitcurator-distro-main/network)

## DEPRECATION NOTICE:

This repository has been deprecated, and is no longer actively maintained. Future releases of BitCurator will be created and maintained using SaltStack (https://saltstack.com/). You can find additional information in the current main repository (https://github.com/bitcurator/bitcurator-distro) and the Salt-based build tool repository (https://github.com/bitcurator/bitcurator-distro-salt).

## Overview

This repository contains scripts, tools and assets required to build the BitCurator ISO for distribution. It is intended solely for use by developers and maintainers working on the BitCurator environment. 

Looking for the latest release? You can find it packaged as live-boot and installation ISO and as a VirtualBox virtual machine at https://github.com/BitCurator/bitcurator-distro/wiki/Releases

## Introduction to building the BitCurator distro (for developers)

The BitCurator environment is a customized respin of Ubuntu 16.04. Aside from the initial Ubuntu install, a small number of manual tweaks, and executing the respin tool, the process is fully automated by a script found in the bitcurator-distro-bootstrap repository. To get started building and testing a new release, you will need the following:

- The latest Ubuntu 16.04.1 ISO (https://www.ubuntu.com/download/desktop)
- bitcurator-distro-bootstrap (https://github.com/bitcurator/bitcurator-distro-bootstrap)

The bootstrap script found in bitcurator-distro-bootstrap will (among other tasks) automatically clone out two support repositories, bitcurator-distro-main (the repo you're looking at right now) and bitcurator-distro-tools (which includes a small set of disk image management and analysis tools with their own Python installer). You do not need to clone these repositories unless you intend to patch, modify, or maintain them.

- bitcurator-distro-main (https://github.com/bitcurator/bitcurator-distro-main)
- bitcurator-distro-tools (https://github.com/bitcurator/bitcurator-distro-tools)

## Building (for developers)

The BitCurator environment is currently tested and maintained using Ubuntu 16.04.1LTS. Instructions on how the environment is currently prepared follow. Note: Some of these procedures could probably be automated. Automation modifications should be pushed to https://github.com/bitcurator/bitcurator-distro-bootstrap.

Download a copy of this Ubuntu ISO from http://releases.ubuntu.com/16.04.1/ubuntu-16.04.1-desktop-amd64.iso and install on a host machine or VirtualBox VM. Do not install guest additions if using a VM.
- During the install, do not install updates or 3rd party extensions
- During the install, set the host name to __BitCurator__, the user to __bcadmin__, the password to __bcadmin__, and __enable auto-login__ (using the appropriate checkbox).

Reboot the system at the prompt.

Once rebooted to the desktop, click on the Unity launcher and type __Terminal__. Drag the terminal icon to the Unity bar on the left for convenient access. Open a terminal and update the system using the following commands:

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

__This process may take 20-30 minutes.__ Once the upgrade has completed, close the terminal.

Open the Ubuntu "System Settings" dialog (by clicking on the gear icon in the top right menu bar), and click on "Displays". Set the resolution to __1024x768__. 

Return to the main window by clicking on __All Settings__, click on the __Theme__ dropdown, and select __Radiance__. Set the Launcher Icon Size to 44. Click on the __Behavior__ tab and select __Enable Workspaces__. Select __In the window's title bar__ from __Show the menus for a window__. 

Return to the main window by clicking on __All Settings__, click on __Brightness and Lock__, and select __Never__ for __Turn screen off when inactive for__. Disable __Lock__, and disable the password requirement for returning from lock.

Open __Firefox__ and set the homepage to __https://wiki.bitcurator.net/__.

In a terminal, install dkms to ensure any kernel extensions installed in the remaining tasks are automatically transferred to new kernels:

```shell
sudo apt-get install dkms
```

In a terminal, install __git__ and clone out the bootstrap repo:

```shell
sudo apt-get install git
git clone https://github.com/bitcurator/bitcurator-distro-bootstrap
```

The bc-bootstrap.sh script is used to install required dependencies, the BitCurator Python tools, and other supporting software. In the same terminal, run the following commands:

```shell
cd bitcurator-distro-bootstrap
sudo ./bc-bootstrap.sh -s -i -y
```

__This process may take an hour or longer to complete__. When the bootstrap script has completed, you will be prompted to reboot. Run the following commenad:

```shell
sudo reboot
```

The bootstrap script places installation log info in __/home/bcadmin/bitcurator-boostrap.log__. You may wish to scan this file manually, or refer to it if any of the installed tools fail in additional testing. (If you are building the BitCurator environment in a VM, this may be a good time to shut down, create a clone, and test each tool individually to verify operation. Some tools create additional user data that may be copied when generating the installation ISO - as the __bcadmin__ user is copied over verbatim - so this testing should not be performed in the release-preparation copy.

Move the icons on the Desktop into the appropriate locations. The standard BitCurator release places __home__ in the top left, followed vertically by __Imaging Tools__, __Forensics Tools__, __Accession Tools__, __Additional Tools__, and __Shared Folders and Media__. __Documentation and Help__ and __Network Servers__ are placed in the top right.

Once the system has been rebooted, click on the Unity launch icon and type __Users and Groups__. Click __Advanced Settings__, and select the __User Privileges__ tab. Select __Use floppy drives__ and click __OK__.

If you are building the release in a VM, now is a good time to shut down, create a clone, and perform the __respin__ (next section) using that clone.

## Respin

BitCurator uses Bodhibuilder (a fork and update of the Remastersys tool) to repin the environment as a Live / Installable CD. Bodhibuilder is installed automatically by the __bitcurator-distro-bootstrap__ bootstrap script.

Click the Unity launcher and type __Bodhibuilder__. Click the Bodhibuilder icon and select the __Settings__ tab. Enter __bcadmin__ for Username, __BitCurator-X.X.X__ (where X.X.X is the release number) for CD Label, __BitCurator-X.X.X.iso__ for ISO Filename, "BitCurator-X-X-X" for GRUB Name, and "http://wiki.bitcurator.net/" for URL for ISO.

Click on the __Actions__ tab and click __Select__ next to __Boot menu picture for the Live CD__. Select the image at __/usr/share/bitcurator/resources/images/BitCuratorEnv3Logo300px-invert.png__. Click __Open__. Click __OK__ in the popup dialog.

Click __Select__ next to __Boot menu picture for the installed environment__. Select the image at __/usr/share/bitcurator/resources/images/BitCuratorEnv3Logo300px-invert.png.__ Click __Open__. Click __OK__ in the popup dialog. GRUB setting will update.

Click __Select__ next to __User, whose current settings will be used as default__ and select __bcadmin__. Click __OK__. Files will copy.

Click __Select__ next to __Plymouth theme__ and select __BitCurator Logo__. Click __OK__. The initramfs will update.

In the main window, click __Backup__, and then click __OK__. The file __BitCurator-X.X.X.iso__ (along wth MD5 and SHA256 sum files) will be created in /home/bodhibuilder/bodhibuilder. __This process may take up to an hour to complete__.

The resulting ISO can be used to prepare a VirtualBox virtual machine, or copied to a USB drive for installation on another host (see https://www.ubuntu.com/download/desktop/create-a-usb-stick-on-ubuntu for instructions on how to perform this transfer).

## Preparation of the Virtual Machine

Create a new VirtualBox VM with 2048MB RAM and 2 processors assigned. Set the video memory to 128MB, enable bidirectional transfer for copy/paste and file drag-and-drop, enable USB 3.0 (XHCI) support, and create a new USB device filter called "All USB Devices". Boot the VM and select the BitCurator ISO as the installation medium. Click through the default options and allow the installation to complete. Reboot. Make any final adjustments to the look and feel of the user desktop (as required) and shut down the VM. Delete the "Logs" and ".vbox-prev" files from the VM directory. Tar and gzip the directory for distribution.

## BitCurator documentation, help, and other information

User documentation and additional resources are available at
[http://wiki.bitcurator.net/](http://wiki.bitcurator.net/).

Questions and comments can also be directed to the bitcurator-users list.

[https://groups.google.com/d/forum/bitcurator-users](https://groups.google.com/d/forum/bitcurator-users)

## License(s)

The BitCurator logo, BitCurator project documentation, and other non-software products of the BitCurator team are subject to the the Creative Commons Attribution 4.0 Generic license (CC By 4.0).

Unless otherwise indicated, software items in this repository are distributed under the terms of the GNU General Public License, Version 3. See the text file "COPYING" for further details about the terms of this license.

In addition to software produced by the BitCurator team, BitCurator packages and modifies open source software produced by other developers. Licenses and attributions are retained here where applicable.

## Acknowledgements

Files in "/scripts/bash_scripts" and "/scripts/nautilus_scripts" are based on original code developed by their respective authors and distributed under respective versions of the GNU General Public License.

The py3fpdf code is a local fork of J. Rivera's Python 3 port of the fpdf library distributed under the LGPL.

See http://bitcurator.net/ for up-to-date project information.


## Development Team and Support

The BitCurator environment is a product of the BitCurator team housed at the School of Information and Library Science at the University of North Carolina at Chapel Hill. Funding between 2011 and 2014 was provided by the Andrew W. Mellon Foundation.

Ongoing support for the BitCurator environment and related tools is provided by the BitCurator Consortium. Find out more at:

http://www.bitcuratorconsortium.net/

