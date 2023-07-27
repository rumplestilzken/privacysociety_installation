#!/usr/bin/env python3

import os


def download_mtkclient():
    print("Downloading mtkclient")
    if not os.path.exists("downloads/mtkclient"):
        os.system("cd downloads; git clone https://github.com/rumplestilzken/mtkclient.git")


def install_mtkclient():
    os.system("cd downloads/mtkclient; sudo pip3 install -r requirements; sudo python3 setup.py build; sudo python "
              "setup.py install")
    os.system("cd downloads/mtkclient; sudo usermod -a -G plugdev $USER; sudo usermod -a -G dialout $USER; sudo cp "
              "Setup/Linux/*.rules /etc/udev/rules.d; sudo udevadm control -R")


def download_mksuper():
    print("Downloading mksuper")
    if not os.path.exists("downloads/mksuper"):
        os.system("cd downloads; git clone https://github.com/rumplestilzken/mksuper.git")


def main():
    print("Installing dependencies...")

    os.system("sudo apt install git wget python3 libusb-1.0-0 python3-pip")

    os.system("mkdir -p downloads")
    download_mtkclient()
    install_mtkclient()
    download_mksuper()

    print("Reboot your computer now.")
    return


if __name__ == '__main__':
    main()
