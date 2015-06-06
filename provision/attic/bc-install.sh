#!/bin/bash

# BitCurator Install Scripts
#
# BitCurator is free and open source. You can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3. 
#
# You should have received a copy of the GNU General Public License.
# If not, see <http://www.gnu.org/licenses/>.

# @package BitCurator 
# @author KW
# @version svn: $Id$

user_home=$HOME
curr_dir=`pwd`
cd `dirname $0`

echo "Ok, let's get started!"
echo ""
echo "It looks like your current working directory is ${curr_dir}."
echo "We'll be installing some software in ${user_home}."

# -----------
# BASIC SETUP
# -----------

# Check for next available UID
uid_avail=`awk -F: '{uid[$3]=1}END{for(x=1000; x<=1100; x++) {if(uid[x] != ""){}else{print x; exit;}}}' /etc/passwd`
echo "Next UID available: ${uid_avail}"
echo ""

# Need to add nopasswdlogin here
seq="create the default BitCurator user (bcadmin)"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
echo "Going to ${seq} ..."
        #echo "sudo adduser --uid ${uid_avail} --group --system --home /home/bcadmin bcadmin"
        #echo "sudo gpasswd -a $USER bcadmin"
        sudo adduser --uid ${uid_avail} --group --system --home /home/bcadmin bcadmin
        sudo gpasswd -a $USER bcadmin
        echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq_a="install BitCurator dependencies (this may take some time)"
seq_b="install BitCurator dependencies"
echo -n " -- Would you like to ${seq_a}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
echo "Going to ${seq_b} ..."
        #echo "sudo apt-get install bitcurator-dep_0.5.6_all.deb -y"
        sudo dpkg -i ${curr_dir}/debs/bc-meta/bitcurator-deps_0.6.4_all.deb
        sudo apt-get -f install -y
        echo ""
else
echo "Skipping: ${seq_b}"
echo ""
fi

# ----------------------
# EXTERNAL REPOSITORIES
# ----------------------

seq="add the Guymager repository and install the latest version"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	sudo wget -nH -rP /etc/apt/sources.list.d/ http://deb.pinguin.lu/pinguin.lu.list        
	wget -q http://deb.pinguin.lu/debsign_public.key -O- | sudo apt-key add -
	sudo apt-get update
	sudo apt-get install guymager-beta
        echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

# DEPRECATED
#seq="add the YaD PPA repository and install YaD"
#echo -n " -- Would you like to ${seq}? -- (y/N) "
#read a
#if [[ $a == "Y" || $a == "y" ]]; then
#        sudo apt-get install python-software-properties -y
#        sudo apt-add-repository ppa:webupd8team/y-ppa-manager
#        sudo apt-get update
#        sudo apt-get install yad
#	echo ""
#else
#echo "Skipping: ${seq}"
#echo ""
#fi

# -------------------------
# ENVIRONMENT CUSTOMIZATION
# -------------------------

seq="copy BitCurator folders and shortcuts to the desktop"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	cp -r ${curr_dir}/env/desktop-folders/* ${user_home}/Desktop
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="set the desktop background to the BitCurator logo"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	gsettings set org.gnome.desktop.background picture-uri ${curr_dir}/env/images/bc400px-1280full.png
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

# ----------------------
# SOFTWARE INSTALLATIONS
# ----------------------

seq="install Apache Thrift"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	wget archive.apache.org/dist/thrift/0.9.1/thrift-0.9.1.tar.gz -O /tmp/thrift-0.9.1.tar.gz
	tar zxvf /tmp/thrift-0.9.1.tar.gz -C /tmp
	cd /tmp/thrift-0.9.1
	make
	sudo make install
	cd ~
	# UPDATE FOR FINAL INSTALL
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="install libewf"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	wget https://googledrive.com/host/0B3fBvzttpiiSMTdoaVExWWNsRjg/libewf-20130416.tar.gz -O /tmp/libewf-20130416.tar.gz
	tar zxvf /tmp/libewf-20130416.tar.gz -C /tmp
	# UPDATE FOR FINAL INSTALL
	cd /tmp/libewf-20130416
	./configure
	make
	sudo make install
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="install AFFLIB"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	git clone https://github.com/simsong/AFFLIBv3 /tmp/AFFLIBv3
	# UPDATE FOR FINAL INSTALL
	cd /tmp/AFFLIBv3
	./configure
	make
	sudo make install
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="install ZeroMQ"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	git clone --recursive https://github.com/zeromq/zeromq3-x.git /tmp/zeromq
	# UPDATE FOR FINAL INSTALL
	cd /tmp/zeromq
	./autogen.sh
	./configure
	make
	sudo make install
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="install bulk_extractor"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	git clone --recursive https://github.com/simsong/bulk_extractor /tmp/bulk_extractor
	# UPDATE FOR FINAL INSTALL
	cd /tmp/bulk_extractor
	./configure
	make
	sudo make install
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="install matplotlib from the latest sources"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	git clone --recursive https://github.com/matplotlib/matplotlib /tmp/matplotlib
	# UPDATE FOR FINAL INSTALL
	cd /tmp/matplotlib
	python3 setup.py build
	sudo python3 setup.py install
	sudo ldconfig
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="install The Sleuth Kit from the latest sources"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	git clone --recursive https://github.com/sleuthkit/sleuthkit /tmp/sleuthkit
	# UPDATE FOR FINAL INSTALL
	cd /tmp/sleuthkit
	./bootstrap
        ./configure
        make
        sudo make install
	sudo ldconfig
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

#seq="install py3fpdf"
#echo -n " -- Would you like to ${seq}? -- (y/N) "
#read a
#if [[ $a == "Y" || $a == "y" ]]; then
#	git clone --recursive https://github.com/kamwoods/py3fpdf /tmp/py3fpdf
#	# UPDATE FOR FINAL INSTALL
#	cd /tmp/py3fpdf
#	python3 setup.py build
#	sudo python3 setup.py install
#	sudo ldconfig
#	echo ""
#else
#echo "Skipping: ${seq}"
#echo ""
#fi

# ----------------------
# MORE ENVIRONMENT SETUP
# ----------------------

seq="copy the disk mounting scripts to /usr/local/bin and /usr/sbin"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	sudo cp -r ${curr_dir}/env/usr/local/bin/* /usr/local/bin
	sudo cp -r ${curr_dir}/env/usr/sbin/* /usr/sbin
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="copy support items to /usr/share"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
	sudo cp -r env/share/pixmaps/* /usr/share/pixmaps
	echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

# ----------------------
# DESKTOP
# ----------------------

# ADD BACKGROUND
# ADD LAUNCHERS
# ADD SUPPORT FOR SDHASH GUI
# ADD OTHER PY INSTALLS

exit

