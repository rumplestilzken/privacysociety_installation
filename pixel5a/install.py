#!/usr/bin/env python3

import os
import subprocess

filename = ""
magisk_filename = ""


def download_resources():
    here = os.path.dirname(os.path.realpath(__file__))

    global filename

    filename = "barbet-tq3a.230805.001.tar.xz"

    if not os.path.exists(here + "/" + filename):
        print("Downloading Stock Rom")
        os.system(
            "cd " + here + "; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                           "/rom_resources/" + filename)

    if not os.path.exists(here + "/" + filename.strip(".tar.xz")):
        print("Extracting Stock Rom")
        os.system("cd " + here + "; xz -kd " + filename)
        os.system("cd " + here + "; tar -xf " + filename.strip(".xz"))
        os.system("cd " + here + "; rm " + filename.strip(".xz"))

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
    answer = input("Keep device connected. Press enter and reboot or power on the device.")
    command = "cd " + here + "/" + filename.replace(".tar.xz", "") + "/flash-all.sh"
    os.system(command)


def flash_lineage():
    print("Preparing to flash PrivacySociety GSI")
    here = os.path.dirname(os.path.realpath(__file__))

    answer = input("Let device power on and manually process according to README. Press Enter to continue.")
    os.system("adb kill-server")
    os.system("adb shell; exit")
    os.system("adb reboot fastboot")
    answer = input("Press Volume Up on the device when prompted...Press enter to continue")
    os.system("fastboot flashing unlock")
    output = subprocess.check_output("fastboot flash boot_a " + here + "/" + magisk_filename)
    while "not allowed in locked state" in output:
        input("Unlocking attempt failed. Please try again. Press Volume Up when prompted. Press enter when ready.")
        os.system("fastboot flashing unlock")
        output = subprocess.check_output("fastboot flash boot_a " + here + "/" + magisk_filename)

    os.system("fastboot flash --disable-verity --disable-verification vbmeta_a " + here + "/" + filename.strip(
        ".tar.xz") + "/image-barbet-tq3a.230805.001/vbmeta.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_system_a " + here + "/" + filename.strip(
        ".tar.xz") + "/image-barbet-tq3a.230805.001/vbmeta_system.img")
    os.system("fastboot resize-logical-partition product_a 0x0")
    os.system("fastboot flash system_a " + here + "/" + filename.strip(".tar.xz") + ".img")
    os.system("fastboot reboot")
    print("The device will now reboot into PrivacySociety GSI")


def main():
    download_resources()
    flash_stock()
    flash_lineage()
    return


if __name__ == '__main__':
    main()
