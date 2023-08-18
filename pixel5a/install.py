#!/usr/bin/env python3

import os
import subprocess

filename = ""
magisk_filename = ""
img_filename = ""


def download_resources():
    here = os.path.dirname(os.path.realpath(__file__))

    global filename

    filename = "barbet-tq3a.230805.001"

    if not os.path.exists(here + "/" + filename):
        print("Downloading Stock Rom")
        os.system(
            "cd " + here + "; wget https://dl.google.com/dl/android/aosp/barbet-tq3a.230805.001-factory-5c469710.zip")

    if not os.path.exists(here + "/" + filename):
        print("Extracting Stock Rom")
        os.system("cd " + here + "; unzip " + filename)
    if not os.path.exists(here + "/" + filename + "/system.img"):
        os.system("cd " + here + "/" + filename + "/; unzip image-barbet-tq3a.230805.001.zip")

    f = open(here + "/" + filename + "/flash-all.sh", "r")
    file_lines = f.read()
    f.close()

    if "skip-reboot" not in file_lines:
        file_lines = file_lines.replace("-w", "-w --skip-reboot")

        f = open(here + "/" + filename + "/flash-all.sh", "w")
        f.write(file_lines)
        f.close()

        print(file_lines)

    global img_filename
    img_filename = "privacysociety_pixel5a.img.xz"
    if not os.path.exists(here + "/" + img_filename):
        print("Downloading PrivacySociety GSI")
        os.system(
            "cd " + here + "; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                           "/rom_resources/" + img_filename)
        print("Extracting PrivacySociety GSI")
        os.system("cd " + here + "; xz -kd " + img_filename)

    global magisk_filename
    magisk_filename = "magisk_patched-26100_GuQtC.img"

    if not os.path.exists(here + "/" + magisk_filename):
        print("Downloading Magisk Boot Image")
        os.system(
            "cd " + here + "; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                           "/rom_resources/" + magisk_filename)


def flash_stock():
    here = os.path.dirname(os.path.realpath(__file__))
    print("Flashing Stock Rom")
    global filename
    answer = input("Plug in the device. Let device power on and manually process according to README. Press Enter to "
                   "continue.")
    os.system("adb kill-server")
    os.system("adb reboot fastboot")
    command = "cd " + here + "/" + filename + ";bash flash-all.sh"

    os.system(command)


def flash_lineage():
    global filename
    global img_filename

    print("Preparing to flash PrivacySociety GSI")
    here = os.path.dirname(os.path.realpath(__file__))
    answer = input("Press Volume Down on the device when prompted and Press the Power button to Unlock the "
                   "bootloader...Press enter to continue")
    os.system("fastboot reboot bootloader")
    os.system("fastboot flashing unlock")
    os.system("fastboot flash boot_a " + here + "/" + magisk_filename)
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_a " + here + "/" + filename + \
              "/vbmeta.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_system_a " + here + "/" + filename + \
              "/vbmeta_system.img")

    os.system("fastboot reboot fastboot")
    os.system("fastboot resize-logical-partition product_a 0x0")
    os.system("fastboot flash system_a " + here + "/" + img_filename.replace(".xz", ""))
    os.system("fastboot erase userdata")
    os.system("fastboot reboot")
    print("The device will now reboot into PrivacySociety GSI")


def main():
    download_resources()
    flash_stock()
    flash_lineage()
    return


if __name__ == '__main__':
    main()
