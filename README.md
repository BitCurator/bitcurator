bitcurator-distro-main
----------------------

This repository contains scripts, tools and assets required to build the BitCurator ISO for distribution. It is intended solely for use by developers and maintainers working on the BitCurator environment. 

Looking for the latest release? You can find it packaged as live-boot and installation ISO and as a VirtualBox virtual machine at:

  http://wiki.bitcurator.net/

# Introduction to building the BitCurator distro (for developers)

The BitCurator environment is a customized respin of Ubuntu 16.04. Aside from the initial Ubuntu install, a small number of manual tweaks, and executing the respin tool, the process is fully automated by a script found in the bitcurator-distro-bootstrap repository. To get started building and testing a new release, you will need the following:

- The latest Ubuntu 16.04.1 ISO (https://www.ubuntu.com/download/desktop)
- bitcurator-distro-bootstrap (https://github.com/bitcurator/bitcurator-distro-bootstrap)

The bootstrap script found in bitcurator-distro-bootstrap will (among other tasks) automatically clone out two support repositories, bitcurator-distro-main (the repo you're looking at right now) and bitcurator-distro-tools (which includes a small set of disk image management and analysis tools with their own Python installer). You do not need to clone these repositories unless you intend to patch, modify, or maintain them.

- bitcurator-distro-main (https://github.com/bitcurator/bitcurator-distro-main)
- bitcurator-distro-tools (https://github.com/bitcurator/bitcurator-distro-tools)

# Installation and respin (for developers)

The BitCurator environment is currently tested and maintained using Ubuntu 16.04.1LTS. Instructions on how the environment is currently prepared follow:

- Download a copy of this Ubuntu ISO from http://releases.ubuntu.com/16.04.1/ubuntu-16.04.1-desktop-amd64.iso and install on a host machine or VirtualBox VM. Do not install guest additions if using a VM.
- During the install, do not install updates or 3rd party extensions
- During the install, set the host name to "BitCurator", the user to "bcadmin", the password to "bcadmin", and enable auto-login.
- Reboot the system at the prompt
- Once rebooted to the desktop, open a terminal and update the system:

```shell
sudo apt-get update
sudo apt-get upgrade
sudo apt-get dist-upgrade
```

- In a terminal, install dkms to ensure any kernel extensions installed in the remaining tasks are automatically transferred to new kernels:

```shell
sudo apt-get install dkms
```

- In a terminal, install git and clone out the bootstrap repo:

```shell
sudo apt-get install git
git clone https://github.com/bitcurator/bitcurator-distro-bootstrap
```

- The bc-bootstrap.sh script is used to install required dependencies, the BitCurator Python tools, and other supporting software. In the same terminal, run the following commands:

```shell
cd bitcurator-distro-bootstrap
./bc-bootstrap.sh -s -i -y
```

# BitCurator documentation, help, and other information

User documentation and additional resources are available at
[http://wiki.bitcurator.net/](http://wiki.bitcurator.net/).

Questions and comments can also be directed to the bitcurator-users list.

[https://groups.google.com/d/forum/bitcurator-users](https://groups.google.com/d/forum/bitcurator-users)

# License(s)

The BitCurator logo, BitCurator project documentation, and other non-software products of the BitCurator team are subject to the the Creative Commons Attribution 4.0 Generic license (CC By 4.0).

Unless otherwise indicated, software items in this repository are distributed under the terms of the GNU General Public License, Version 3. See the text file "COPYING" for further details about the terms of this license.

In addition to software produced by the BitCurator team, BitCurator packages and modifies open source software produced by other developers. Licenses and attributions are retained here where applicable.

# Acknowledgements

Files in "/scripts/bash_scripts" and "/scripts/nautilus_scripts" are based on original code developed by their respective authors and distributed under respective versions of the GNU General Public License.

The py3fpdf code is a local fork of J. Rivera's Python 3 port of the fpdf library distributed under the LGPL.

See http://wiki.bitcurator.net/ for up-to-date project information.


# Development Team and Support

The BitCurator environment is a product of the BitCurator team housed at the School of Information and Library Science at the University of North Carolina at Chapel Hill. Funding between 2011 and 2014 was provided by the Andrew W. Mellon Foundation.

Ongoing support for the BitCurator environment and related tools is provided by the BitCurator Consortium. Find out more at:

http://www.bitcuratorconsortium.net/

