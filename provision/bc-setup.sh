#!/bin/bash

# BitCurator Install Scripts
# Last updated: December 15, 2013
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

echo "@@@@@     @@    C      @@@@@"
echo "@@  @@@    @   @@     @@@  @                          @@"
echo "@@   @@        @@     @@                              @@"
echo "@@    @   @@   @@@@  @@       @@   @@   @@@@@ @@@@@   @@@@@     llll     @@@@"
echo "@@   @@   @@   @@    @@       @@   @@   @@       @@   @@      lllllll   ,@"
echo "@@@@@@    @@   @@    @@       @@   @@   @@        @@  @@      llllllll  ,@"
echo "@@@@@@@   @@   @@    @@       @@   @@   @@        @@  @@    ;llll,lllll ,@"
echo "@@    @@  @@   @@    @@       @@   @@   @@    @@@@@@  @@     tltt,:tttt ,@"
echo "@@    @@  @@   @@    @@       @@   @@   @@   @@   @@  @@     tftfl:LLLf ,@"
echo "@@    @@  @@   @@    @@       @@   @@   @@   @@   @@  @@     fLLCGGGGC  ,@"
echo "@@   @@@  @@   @@     @@      @@   @@   @@   @@   @@   @      LCGGGGGG  ,@"
echo "@@@@@@@   @@    @@@    @@@@@@  @@@@@@   @@    @@@@@@   @@@@    CGGGGG   ,@"

echo "Welcome to the BitCurator Installer!"

echo "Ok, let's get started!"
echo ""
echo "It looks like your current working directory is ${curr_dir}."
echo "We'll be installing some software in ${user_home}."

seq="install git, in order to download BitCurator"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
echo "Going to ${seq} ..."
        #echo "sudo apt-get install git -y"
        sudo apt-get install git -y
        echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

seq="pull down the current BitCurator source, tools, and supporting scripts"
echo -n " -- Would you like to ${seq}? -- (y/N) "
read a
if [[ $a == "Y" || $a == "y" ]]; then
echo "Going to ${seq} ..."
        #echo "sudo apt-get install git -y"
        git clone https://github.com/bitcurator/bitcurator
        echo ""
else
echo "Skipping: ${seq}"
echo ""
fi

exit

