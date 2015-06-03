BitCurator Environment Build Procedure (Current: Trusty Tahr / BC v1.1.0)

This document contains many sequential dependencies, not all of which are strict. Please add comments if you find errors or see an obvious cleanup.

Note! Checking available versions of software in apt-cache: If there’s a question about what the current build of a support library is, you can check with “apt-cache policy [package-name]”

Getting Started

1. Make sure your VirtualBox install is up to date, then download the latest Oracle VM VirtualBox Extension Pack image, and install it by double-clicking on it in the host.
https://www.virtualbox.org/wiki/Downloads

2. Download Ubuntu 14.04LTS 64-bit image from Canonical
http://www.ubuntu.com/download/desktop

3. Set up a new virtual disk image. Use “dynamically resizing” and set to to 256GB. Set BitCurator release name (generally, BitCurator-X.X.X for version, subversion, and subsubversion).

5. Release VM should have memory set to 1575MB, and processors to 1. Set the video memory to 64MB. This is for compatibility purposes, not for optimization. Note: While building the environment, it’s faster to keep memory at 4,096+ and processors to two or more.

6. Install Ubuntu: When prompted, select “Install Ubuntu” rather than “Try Ubuntu”. Select “Download updates while installing”, but not “Select this third party software”. Continue through the remain defaults until login info:
Your name: BitCurator
Computer’s name: bcadmin-VirtualBox
Username: bcadmin
Password: bcadmin
Select “log in automatically”
If you miss this step, later you’ll need to enable auto-login: sudo vim /etc/lightdm/lightdm.conf and add:
autologin-user=<username>
autologin-user-timeout=0
Continue.
Wait. Once finished, click “Restart Now”.

7. Run “sudo apt-get install dkms”, and update manager
7.1 Once restarted, run “Update Manager”.
7.2 Install VirtualBox guest additions by selecting “Install guest additions” under “Devices” menu (if not automatically prompted to do so).
   1. Reboot.

7.3 Fix SMBUS error:
This error can be easily fixed by adding the extra line to the bottom of /etc/modprobe.d/blacklist.conf:
blacklist i2c_piix4

7.5 Open Software Center. Under “Edit” select software sources, and under Other Software check both “Canonical Partners” items.

7.6 In “System Settings”, click on “Appearance” and set the theme to “Radiance”. (This will improve readability of GTK-based GUIs)

Building the Dependencies File (MUST do this after installing guest additions)

8. Start up an older version of the VM. Update the BitCurator dependencies metadata package as necessary using the “equivs” package. Make the necessary additions to the file by adding the name of new packages to the “Depends” line (comma delimited). Then run “equivs-build bitcurator-dep-X.X.X” (where X.X.X is the current build number).

CURRENT 14.04 dependencies list (post-0.9.0)
g++, ant, libcrypto++9, libssl-dev, expat, libexpat1-dev, libfuse-dev, libncurses5-dev, libcurl4-openssl-dev, libreadline-dev, libmagic-dev, flex, gawk, libpthread-stubs0-dev, libcppunit-1.13-0, libcppunit-dev, libtool, automake, openjdk-7-jdk, expect, ghex, gnome-system-tools, gnome-panel, gnome-search-tool, hfsutils, hfsutils-tcltk, hfsplus, hfsprogs, dconf-tools, libgtk2.0-dev, xmount, mercurial-common, python-sphinx, vim, git, equivs, python3, python3-setuptools, python3-dev, python3-numpy, uuid-dev, libncursesw5-dev, libbz2-dev, clamav, clamav-daemon, clamtk, dkms, sharutils, smartmontools, hdparm, fdutils, smbfs, winbind, subversion, libarchive-dev, nautilus-actions, libxml2-dev, libboost-dev, libboost-test-dev, libboost-program-options-dev, libboost-system-dev, libboost-filesystem-dev, bison, apache2, libapache2-mod-python, python3-pyqt4, libqt4-dev, qt4-dev-tools, python-qt4-dev, pyqt4-dev-tools, python3-sip-dev, mysql-client, libmyodbc, unixodbc, unixodbc-dev, libmysqlclient-dev, libexif-dev, readpst, recoll, cdrdao, dcfldd, bchunk, libimage-exiftool-perl, python-tk, python3-tk, python-pyside, python-compizconfig, udisks, libappindicator1, unity-tweak-tool, gnome-tweak-tool, compizconfig-setting-manager, python2.7-config, gtkhash, nautilus-scripts-manager, fslint, 
libgnomeui-0, libgnomeui-dev, cmake, swig, python-magic, libtre-dev, libtre5, libudev-dev, gddrescue, gnome-sushi, vlc, autopoint

[* libboost-dev libboost-test-dev libboost-program-options-dev libevent-dev automake libtool flex bison pkg-config g++ libssl-dev *]

[[libzmq1, libzmq-dev]]

[Non-current additions for building AIR: dc3dd, sharutils, perl-tk]
[Note: For qt4 building of test gui: qt4-qmake, libqt4-dev, qt4-designer, python3-pyside 
Convert GUI file: pyuic4 -x bc_genrep_gui.ui -o bc_genrep_gui.py

8.1: To install QT4 deps:
sudo apt-get install python3-dev libqt4-dev g++ python-qt4 qt4-dev-tools python-qt4-dev pyqt4-dev-tools, python3-sip-dev
apt-get source python-qt4
cd into python-qt4 directory that was just downloaded and unpacked 
(it should definitely be there - if it is not, something went wrong)

python3 configure.py
make
sudo make install

8.2: For future dev:
Need to compile python to *nix executable? Use Freeze (maybe not Py3????)
File dialog: http://stackoverflow.com/questions/3196353/pyqt4-file-select-widget

9. Unmount CD-ROM from guest. Power down the guest. Check that the CD-ROM image is not attached in the host settings.

10. Reboot the VM.

11. Under Settings -> Ports in the host menu, enable USB 2.0 passthrough and set up an *empty* filter to capture all USB devices.

Useful extras

Do some of the things here: http://scienceblogs.com/gregladen/2014/04/24/10-or-20-things-to-do-after-installing-ubuntu-14-04-trusty-tahr/

Configuring the Environment

12. Restart the VM, login, and add Terminal to launcher. Then right-click on Ubuntu One and unlock from launcher.

13. Edit Terminal profile preferences, set font point to 10, scrollback to 2048, and custom size 80x42 rows.

14. Set background image to bc400px-1280full.png (pull from previous release). Pick middle blue color and set image to “Fill”.

15. Add “Imaging Tools”, “Forensics Tools”, “Metadata Tools”, and “Documentation and Help” folders to Desktop.
      1. Add a “Bulk Extractor Viewer” directory to “Documentation and Help”, and place BEVeiwer help PDF in it.
      2. Add a “Nautilus Scripts” directory to the “Documentation and Help”, and place the README from the previous VM in it.
      3. Add the DFXML tag library in a “DFXML Guides” directory (current version).
      4. Add the “BitCurator Reporting Guide” in a “BitCurator Guides” directory.

16. Make a “Tools” Directory in the home directory.

17. Copy dep file to the new VM and install by double clicking. Place the deb file in an “archives” folder in “Tools”.

18. Download latest versions of AFFLIB, Bulk Extractor, SDHash, fiwalk, pytsk, TSK, AIR imager, and the DFXML tools (see below for links if you don’t have them).

19. Compile and install in the following order: 

apache thrift http://thrift.apache.org/download/
./configure
make
sudo make install

libewf http://code.google.com/p/libewf/downloads/detail?name=libewf-20130303.tar.gz
./bootstrap
./configure --enable-v1-api
make
sudo make install

AFFLib https://github.com/simsong/AFFLIBv3 - git clone, external packaging not available
[./bootstrap.sh, if needed]
./configure
make
sudo make install
sudo ldconfig

TSK http://www.sleuthkit.org/sleuthkit/download.php - use the current master source
git clone --recursive
./bootstrap
./configure
make
sudo make install
sudo ldconfig

PyTSK http://code.google.com/p/pytsk/ - use current source
[ADD BUILD INSTRUCTIONS HERE, NOT CURRENTLY WORKING]

Guymager:
Add the pinguin server and its public key by executing the following commands:
   sudo wget -nH -rP /etc/apt/sources.list.d/ http://deb.pinguin.lu/pinguin.lu.list
    wget -q http://deb.pinguin.lu/debsign_public.key -O- | sudo apt-key add -
sudo apt-get update
sudo apt-get install guymager-beta

ZeroMQ https://github.com/zeromq/zeromq3-x.git - download
git clone --recursive
./autogen.sh
./configure
make
sudo make install

HashDB https://github.com/simsong/hashdb - (or download from digitalcorpora)
git clone --recursive
chmod 755 bootstrap.sh
./configure --with-boost-libdir=/usr/lib/x86_64-linux-gnu
make
sudo make install

bulk extractor https://github.com/simsong/bulk_extractor - download links at bottom
Note: Need boost libraries. Installing libboost-{system,filesystem,chrono,program-options,thread,test}1.54{-dev,.0} manually seems to work.

git clone --recursive
chmod 755 bootstrap.sh
export PATH to /usr/lib/x86_64-linux-gnu in .bashrc, source .bashrc, and

./configure --with-boost-libdir=/usr/lib/x86_64-linux-gnu
make
sudo make install

SDHash http://roussev.net/sdhash/sdhash.html - use current version
[No configure!]
make
sudo make install

HFS Utilities http://www.mars.org/home/rob/proj/hfs/ - use “current” version
./configure
make 
sudo make install

DFXML https://github.com/simsong/dfxml - git clone the current master (no compile needed)

POCO get latest poco source
[should compile fine in 14.04 as of 1.4.6

log2timeline get latest log2timeline source
[note that we don’t necessarily need this right now]

XlsxWriter get latest xlsxwriter source
sudo python3 setup.py install

pyExifToolGUI get latest pyExifToolGUI source
https://github.com/hvdwolf/pyExifToolGUI/releases
run “sudo ./install_remove.py install”
[[ubuntu-tweak get app from http://ubuntu-tweak.com/ - already installed via sources]]

[[[20. Pull the OpenPyXL source from: https://bitbucket.org/ericgazoni/openpyxl/src
(use Mercurial via HG command-line, included as of 0.1.8
hg clone https://bitbucket.org/ericgazoni/openpyxl
sudo python3 setup.py install]]]

21. VERY IMPORTANT: run “sudo ldconfig”

Setting up the Nautilus, Bash, and DFXML Scripts

22. DISABLE AUTOMOUNTING (IMPORTANT):
To enable or disable automount open a terminal and type dconf-editor followed by the [Enter] key. Browse to org.gnome.desktop.media-handling.
Disable the automount key.
Disable the org.gnome.desktop.media-handling.automount-open key. This controls automatically opening a folder for automounted media. This only applies to media where no known x-content/* type was detected; otherwise the user configurable action will be taken.

[[DEPRECATED: already in previously copied files 25. Symlink in DFXML to desktop: ln -s -T /home/bcadmin/Tools/dfxml ~/Desktop/Metadata\ Tools/DFXML\ Scripts]]

23. sudo chmod +x *.desktop in Imaging Tools

24. Check all shortcuts in Imaging Tools, Forensics Tools, verify that they work.

25. Download, update if necessary, test, and install the Nautilus scripts:
To install the Nautilus scripts, first download the following files by clicking on the links below and selecting "Save File" when prompted by Firefox:
BC Nautilus Scripts
BC Bash Scripts
Open a terminal and type “cd ./Downloads” to change to your download directory
Type “tar -C ~/.gnome2/nautilus-scripts -xvf ./bc_nautilus_scripts.tar” to extract the scripts to your nautilus directory
Type “sudo tar -C /usr/local/bin -xvf ./bc_bash_scripts.tar” to install two additional support scripts
Install Yad (required for the safe mount script) by typing the following commands:
sudo apt-add-repository ppa:webupd8team/y-ppa-manager
sudo apt-get update
sudo apt-get install yad
Type “nautilus -q” to restart Nautilus
Open Nautilus by clicking on the icon in the top left of your desktop
Right click anywhere in the Nautilus window and navigate to the “scripts” menu.

26. Now is a good time to reboot and make a snapshot. Save VM to backup drive for reference.

Setting up Support Programs for the Reporting Tools

Note: Error in current matplotlib. Must create setup.cfg, change gtk3agg to “False”, and put the check in the setupext.py, the file that reads it
  if self.get_config() is False:
       raise CheckFailed(“skipping due to configuration”)
in function BackendGtk3Agg

      1. Make a “Support” directory in Tools
      2. cd Tools/Support
      3. git clone https://github.com/matplotlib/matplotlib
      4. cd matplotlib
      5. python3 setup.py build
      6. sudo python3 setup.py install
      7. sudo ldconfig

27. IMPORTANT. Install generate report dependencies - py3fpdf. 
      1. Original source: https://bitbucket.org/cyraxjoe/py3fpdf
      2. Download source tarball, untar. 
      3. python3 setup.py build
      4. sudo python3 setup.py install
      5. You should *not* need to modify $PYTHONPATH or copy the py3fpdf lib into any other directories. If you run the report generation tests later and they fail, something has gone wrong.

28. Run sudo ldconfig *again*

29. Make a “bitcurator” directory in Tools, and a directory in Metadata Tools on the Desktop called “BitCurator Reporting Tools”
          1. Copy over current generate_reports.py and the report configuration file into bitcurator directory [NOTE: CONFIG FILE GOES INTO DIR MENTIONED LATER - FIX THIS].
2. Now create a desktop launcher for the BitCurator report (if not already pulled in from previous VM.

30. Setup sdhash run script:
      1. Make “scripts” directory in /home/bcadmin/Tools
      2. vim run-sdhash.sh
      3. Add following lines:
          #!/usr/bin/expect -f
          spawn -noecho bash
          expect “$ “
          send “cd ~\n”
          send “sdhash\n”
          interact

31. Setup the bitcurator reporting run script:
      1. vim run-bcreport.sh
      2. Add following lines:
          #!/usr/bin/expect -f
          spawn -noecho bash
          expect “$ “
          send “cd ~\n”
          send “python3 /home/bcadmin/Tools/bitcurator/generate_report.py -h\n”
          interact

32. Setup the identify filenames run script:
      1. vim run-identfile.sh
      2. Add following lines:
          #!/usr/bin/expect -f
          spawn -noecho bash
          expect “$ “
          send “cd ~\n”
          send “python3 /home/bcadmin/Tools/bulk_extractor/python/identify_filenames.py -h\n”
          interact

33. Setup the fiwalk run script:
      1. vim run-fiwalk.sh
      2. Add following lines:
          #!/usr/bin/expect -f
          spawn -noecho bash
          expect “$ “
          send “cd ~\n”
          send “fiwalk\n”
          interact

34. Create the appropriate Desktop launchers for all of the scripts in the past several steps (or copy over from previous version of VM).

34.5 Set up /usr/share/icons/bitcurator directory, and copy in icons for launchers

35. Copy FinalBitCuratorLogo-NoText.png to Pictures folder (for report generation).

36. Add the remaining desktop icons:
gsettings set org.gnome.desktop.background show-desktop-icons true
Now you need to restart your ubuntu system before running the following commands.
For Computer Icon
gsettings set org.gnome.nautilus.desktop computer-icon-visible true
For Home icon
gsettings set org.gnome.nautilus.desktop home-icon-visible true
For Network icon
gsettings set org.gnome.nautilus.desktop network-icon-visible true
For Trash icon
gsettings set org.gnome.nautilus.desktop trash-icon-visible true
For Mounted Volumes
gsettings set org.gnome.nautilus.desktop volumes-visible true

37. Set the applet launcher to ‘all’: (was: [‘JavaEmbeddedFrame’, ‘Wine’, ‘Update-notifier’])
In dconf-editor, got to desktop->unity->panel and change systray-whitelist to “all” ((also add mounter to com.canonical.Unity-2d.Panel)????)

IN 14.04: NEED TO REENABLE WHITELIST!
sudo apt-add-repository ppa:gurqn/systray-trusty
sudo apt-get update
sudo apt-get upgrade
(see http://ubuntuforums.org/showthread.php?t=2217458 for original posts)
(also see timekiller’s version: https://launchpad.net/~timekiller/+archive/unity-systrayfix)

Then, restart Unity by pressing ALT + F2 and entering "unity" or by logging out. Then open Dconf Editor, navigate to com > canonical > unity > panel and the "systray-whitelist" should be displayed there so you can enable some apps to be able to use the systray.


38. Enabling the Mounter
1. Move pixmaps to /usr/share/pixmaps/mounter, chmod and chgrp to root (also the two remastersys files)
2. Move fstab.rules to /etc/udev/rules.d/ (and check permissions)
# Force fstab options for devices
RUN+=”/usr/sbin/rbfstab”
3. Double check that rbfstab is in /usr/sbin
4. move mounter, mounteralert.sh, and mouter-launch.sh and rbfstabGUI.sh to /usr/local/bin

In home directory, cd .config, mkdir “autostart”, and copy mounter.desktop to here!!!

39. Add to /usr/sbin rbfstab, rebuildfstab*, and scanpartitions (pulled from CAINE)

40. IMPORTANT: Run updatedb!!!

41. Sudoers file (/etc/sudoers) should include the following after cmnd alias line:
# Cmnd alias specification

# User privilege specification
root    ALL=(ALL:ALL) ALL

# Members of the admin group may gain root privileges
%admin ALL=(ALL) ALL
%admin ALL=(ALL:ALL) NOPASSWD: /usr/local/bin/mounter

# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL
%sudo   ALL=NOPASSWD: ALL

# See sudoers(5) for more information on "#include" directives:

#includedir /etc/sudoers.d
bcadmin ALL=(ALL) NOPASSWD: ALL

42. Enabling floppy access
    1. Allow yourself to use the floppy by going to System->Administration->Users and Groups->Advanced Settings->User Privileges and click on "Use floppy drives"
    1.5 ALSO ADD MOUNT USERSPACE FILE SYSTEMS (FUSE)
    2. Follow these instructions http://askubuntu.com/questions/168597/how-do-i-use-a-floppy-drive-in-ubuntu
Also check here:
http://ubuntuforums.org/showthread.php?t=2060100
Most importantly, here:
http://www.securitybeacon.com/?p=1110

It appears that floppy support might be well broken:
http://ubuntu.5.n6.nabble.com/Upgrade-to-Udisks-2-0-to-get-a-working-floppy-drive-td4994366.html

Recent questions:
https://answers.launchpad.net/ubuntu/+question/244735

43. Support files:
    0. [EVENTUALLY we’ll have an installer to handle this]
    1. Make a /usr/share/pixmaps/bitcurator directory, and copy FinalBitcuratorLogo-NoText to it.
    2. Make an /etc/bitcurator directory and copy bc_report_config.txt into it

44. Update menus
In “Settings”->”Appearance”->”Behavior” select “In the window’s title bar” for menus

45. Fix “rapl domains” message:
http://askubuntu.com/questions/449574/intel-rapl-no-valid-rapl-domains-message-upon-boot

46. Important! Apply some of these fixes!
https://sites.google.com/site/easylinuxtipsproject/first

47. Improve swappiness
sudo vim /etc/sysctrl.conf
Add following lines to bottom of file:
# Decrease swap usage to a workable level
vm.swappiness=10
# Improve cache management
vm.vfs_cache_pressure=50

48. Enable Aff in Guymager
AffEnabled=TRUE

49. Update Plymouth Theme
http://theurbanpenguin.com/wp/?p=3285
END OF LINE
----------------------------------------------------------------------------------------------------------------------------

Creating the BitCurator ISO Image

1. Shut down the VM, and create a snapshot. This will serve as the core image for any further subrevisions (and retain the state of the VM prior to installing the ISO creation packages).

2. Boot the VM snapshot, and follow the directions below (duplicated from Porter’s original ISO creation guide):

Navigate to website for Remastersys base (currently 3.0.4-1) and the Remastersys gtk gui  
Open the Ubuntu Software Center and select Edit -> Software Sources
                 a. Add deb http://www.remastersys.com/ubuntu precise main
sudo apt-get update
Install remastersys and remastersys-gui with “sudo apt-get install remastersys” and “sudo apt-get install remastersys-gui”
Launch the Remastersys GUI from the Dash menu
Click “Customize”
Download the 640x480 Grub background here http://dl.dropbox.com/u/10897132/bitcurator/bitcurator-grub.png
Set the Grub image and Splash image the the image above.
Click User Settings, select bcadmin, then click Select
Click Configure
Change the Live CD Label to “BitCurator Live CD”
Change the Custom ISO to bitcurator-0.2.0.iso, then click Save
Change the user to “bcadmin”
Click Main to return to the main window
Click “Backup” to begin the remaster process. Choosing the backup option will allow us to keep the custom desktop configuration used in the VM .

Edit “/lib/udev/rules.d/80-udisks.rules” and search for the lines
——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-–
# PC floppy drives
#
KERNEL==”fd*”, ENV{ID_DRIVE_FLOPPY}=”1″
# USB floppy drives
#
SUBSYSTEMS==”usb”, ATTRS{bInterfaceClass}==”08″, ATTRS{bInterfaceSubClass}==”04″, ENV{ID_DRIVE_FLOPPY}=”1″
——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-——-–
Replace those “1″ (ones) with “0″ (zeros). That’s all the magic.
Now restart the udev daemon by typing “invoke-rc.d udev restart”
You’re done. It should work now.

And instead, do:
sudo service udev restart

The reverse: how to disable floppies in 14.04
http://askubuntu.com/questions/457970/how-to-completely-disable-floppy-in-ubuntu-14-04

Installing OpenJDK7
---------------------------
In software center, install openjdk-7
This will install openjdk-7-jre and others
Now install openjdk-7-jre

update-java-alternatives -l
(note output)

install icedtea-7-plugin

Now, sudo update-java-alternatives -s java-1.7.0-openjdk-amd64

Apache prep
-----------------
1. Install libapache2-mod-python from Ubuntu Software Center
     sudo apt-get install apache2 libapache2-mod-python

2. Restart apache2: 
     sudo /etc/init.d/apache2 restart

3. Read about mod_python http://modpython.org/python10/

4. You can tell if the module has been installed and turned on by going to /etc/apache2/mods-enabled
   and looking for the correct mod.

xx. ADD MORE HERE and ADD INSTRUCTIONS ON index.cgi
finally keep a log of all remaining installation options

TO DO:
- Add mediainfo
- Add ffmpeg

Install PIP and configobj:
$ sudo apt-get install python-pip python-dev build-essential 
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv 


#sudo pip install configobj

# Install six first, it’s a dep:
https://pypi.python.org/pypi/six

# No - this only installs for Python 2.7. instead, download from:
https://pypi.python.org/pypi/configobj/5.0.2

Then tar zxvf the file and run “sudo python3 setup.py install” from inside the directory


FOR FUTURE VERSIONS:

http://hints.macworld.com/article.php?story=20080623213342356

New tools to install:
creepy http://ilektrojohn.github.io/creepy/

PYTSK in PYTHON3:
Check out conversion (relevant): https://bitbucket.org/andrewgodwin/south/pull-request/89/limit-the-use-of-iostringio-to-python3-use/diff

grub settings:

GRUB_DEFAULT=0
GRUB_DEFAULT=saved
GRUB_SAVEDEFAULT=true
#GRUB_HIDDEN_TIMEOUT=0
GRUB_HIDDEN_TIMEOUT_QUIET=false
GRUB_TIMEOUT=1
GRUB_DISTRIBUTOR=`lsb_release -i -s 2> /dev/null || echo Debian`
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""

Then run “sudo update-grub”

Plymouth / Customizing the Ubuntu Boot Logo:
http://askubuntu.com/questions/143330/how-can-i-customize-the-ubuntu-boot-up-logo
better:
http://ubuntuhandbook.org/index.php/2013/07/install-change-boot-screen-theme-ubuntu-13-04/
Best???
http://theurbanpenguin.com/wp/?p=3285

