# bitcurator-distro-main

This repository contains scripts, tools and assets required to build the BitCurator ISO for distribution. It is intended solely for use by developers and maintainers working on the BitCurator environment. 

Looking for the latest release? You can find it packaged as live-boot and installation ISO and as a VirtualBox virtual machine at:

  http://wiki.bitcurator.net/

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
- During the install, set the host name to "BitCurator", the user to "bcadmin", the password to "bcadmin", and enable auto-login.

Reboot the system at the prompt.

Once rebooted to the desktop, click on the Unity launcher and type "Terminal". Drag the terminal icon to the Unity bar on the left for convenient access. Open a terminal and update the system using the following commands:

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

Open the Ubuntu "System Settings" dialog (by clicking on the gear icon in the top right menu bar), and click on "Displays". Set the resolution to 1024x768. 

Return to the main window by clicking on "All Settings", click on the "Theme" dropdown, and select "Radiance". Set the Launcher Icon Size to 44. Click on the "Behavior" tab and select "Enable Workspaces". Select "In the window's title bar" from "Show the menus for a window". 

Return to the main window by clicking on "All Settings", click on "Brightness and Lock", and select "Never" for "Turn screen off when inactive for". Disable "Lock", and disable the password requirement for returning from lock.

In a terminal, install dkms to ensure any kernel extensions installed in the remaining tasks are automatically transferred to new kernels:

```shell
sudo apt-get install dkms
```

In a terminal, install git and clone out the bootstrap repo:

```shell
sudo apt-get install git
git clone https://github.com/bitcurator/bitcurator-distro-bootstrap
```

The bc-bootstrap.sh script is used to install required dependencies, the BitCurator Python tools, and other supporting software. In the same terminal, run the following commands:

```shell
cd bitcurator-distro-bootstrap
sudo ./bc-bootstrap.sh -s -i -y
```

When the bootstrap script has completed, you will be prompted to reboot. Run the following commenad:

```shell
sudo reboot
```

Move the icons on the Desktop into the appropriate locations. The standard BitCurator release places "home" in the top left, followed vertically by "Imaging Tools", "Forensics Tools", "Accession Tools", "Additional Tools", and "Shared Folders and Media". "Documentation and Help" and "Network Servers" are placed in the top right.

Once the system has been rebooted, click on the Unity launch icon and type "Users and Groups". Click "Advanced Settings", and select the "User Privileges" tab. Select "Use floppy drives" and click "OK".

## Respin

BitCurator uses Bodhibuilder (a fork and update of the Remastersys tool) to repin the environment as a Live / Installable CD. Bodhibuilder is installed automatically using the bitcurator-distro-bootstrap bootstrap script.

Click the Unity launcher and type "Bodhibuilder". Click the Bodhibuilder icon and select the "Settings" tab. Enter "bcadmin" for Username, "BitCurator-X.X.X" (where X.X.X is the release number) for CD Label, "BitCurator-X.X.X.iso" for ISO Filename, "BitCurator-X-X-X" for GRUB Name, and "http://wiki.bitcurator.net/" for URL for ISO.

Click on the "Actions" tab and click "Select" next to "Boot menu picture for the Live CD". Select the image at "/usr/share/bitcurator/resources/images/BitCuratorEnv3Logo300px-invert.png". Click "Open". Click "OK" in the popup dialog.

Click "Select" next to "Boot menu picture for the installed environment". Select the image at "/usr/share/bitcurator/resources/images/BitCuratorEnv3Logo300px-invert.png." Click "Open". Click "OK" in the popup dialog. GRUB setting will update.

Click "Select" next to "User, whose current settings will be used as default" and select "bcadmin". Click "OK". Files will copy.

Click "Select" next to "Plymouth theme" and select "BitCurator Logo". Click "OK". The initramfs will update.

In the main window, click "Backup", and then click "OK". The file "BitCurator-X.X.X.iso" (along wth MD5 and SHA256 sum files) will be created in /home/bodhibuilder/bodhibuilder).

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

See http://wiki.bitcurator.net/ for up-to-date project information.


## Development Team and Support

The BitCurator environment is a product of the BitCurator team housed at the School of Information and Library Science at the University of North Carolina at Chapel Hill. Funding between 2011 and 2014 was provided by the Andrew W. Mellon Foundation.

Ongoing support for the BitCurator environment and related tools is provided by the BitCurator Consortium. Find out more at:

http://www.bitcuratorconsortium.net/

