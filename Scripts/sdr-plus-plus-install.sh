#!/bin/sh
# SDRPlusPlus Installation Script for Raspberry Pi 4B

# Stop on the first sign of failure
set -e

[ $(id -u) = 0 ] && echo "Please do not run this script as root" && exit 100

# Remove the director "SDRPlusPlus" if it exists. If it does not exist, do nothing.
echo "Removing any existing SDRPlusPlus directory..."
[ -d SDRPlusPlus ] && rm -rf SDRPlusPlus

# Uninstall any existing SDRPlusPlus packages
# echo "Uninstalling existing SDRPlusPlus packages..."
# sudo apt purge ^sdrplusplus

echo "Installing dependencies"
sudo apt update
sudo apt install -y build-essential cmake git libfftw3-dev libglfw3-dev libglew-dev libvolk2-dev libzstd-dev libsoapysdr-dev libairspyhf-dev libairspy-dev \
            libiio-dev libad9361-dev librtaudio-dev libhackrf-dev librtlsdr-dev libbladerf-dev liblimesuite-dev p7zip-full wget
            
git clone https://github.com/AlexandreRouma/SDRPlusPlus
cd SDRPlusPlus            

echo "Preparing build"
sudo mkdir -p build
cd build

sudo mkdir -p CMakeFiles
sudo cmake .. -DOPT_BUILD_RTL_SDR_SOURCE=ON

echo "Building"
sudo make

echo "Installing"
sudo make install

# Modded by TekMaker 03/26/2022
# https://www.instructables.com/Building-SDR-From-Source-Code-on-a-Raspberry-PI-4-/
# https://github.com/TekMaker/SDRplus

echo "Installation complete. All tasks were successful!"
echo "Press any key to continue..."
read
