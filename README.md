BitCurator: Tools for Digital Forensics Methods and Workflows in Real-World Collecting Institutions
---------------------------------------------------------------------------------------------------
<http://wiki.bitcurator.net>

# Getting started

BitCurator is a research and development effort designed to bring digital forensics tools and techniques to archives, libraries, and other collecting institutions. The simplest way to get up and running with tools developed by the BitCurator team (and 3rd party tools packaged by us) is to download either our virtual machine or our live-boot and installation ISO.

The most current BitCurator virtual machine and ISO images can be downloaded from

  http://wiki.bitcurator.net/

The default username and password for the virtual machine are as follows:

* Username: `bcadmin`
* Password: `bcadmin`

# Installation and Dependencies

The core BitCurator tools have been tested in Ubuntu 14.04.3LTS and Ubuntu 16.04LTS. You should not clone this repository directly unless you wish to modify the included tools. The BitCurator environment (VM and Live CD) can be downloaded from the wiki noted above.

If you wish to install the BitCurator tools and dependencies in a clean Ubuntu 14.04LTS environment, you may do so using the bitcurator-bootstrap repository (instructions on how to do so are included in the README):

* git clone https://github.com/bitcurator/bitcurator-bootstrap

The bc-bootstrap.sh script will install required dependencies, the BitCurator Python tools, and other supporting software.

# BitCurator Documentation, Help, and other Information

The latest technical and user documentation is available at
[http://wiki.bitcurator.net/](http://wiki.bitcurator.net/).

# License(s)

The BitCurator logo, BitCurator project documentation, and other non-software products of the BitCurator team are subject to the the Creative Commons Attribution 4.0 Generic license (CC By 4.0).

Unless otherwise indicated, software items in this repository are distributed under the terms of the GNU General Public License, Version 3. See the text file "COPYING" for further details about the terms of this license.

In addition to software produced by the BitCurator team, BitCurator packages and modifies open source software produced by other developers. Licenses and attributions are retained here where applicable.

Notes and acknowledgements:

Files in "/scripts/bash_scripts" and "/scripts/nautilus_scripts" are based on original code developed by their respective authors and distributed under respective versions of the GNU General Public License.

The py3fpdf code is a local fork of J. Rivera's Python 3 port of the fpdf library distributed under the LGPL.

See http://wiki.bitcurator.net/ for up-to-date project information.


# Credits

BitCurator is a product of the BitCurator team housed at the School of 
Information and Library Science at the University of North Carolina at 
Chapel Hill. Funding between 2011 and 2014 was provided by the Andrew
W. Mellon Foundation.

Ongoing support for the BitCurator environment and related tools is provided
by the BitCurator Consortium. Find out more at:

http://www.bitcuratorconsortium.net/

