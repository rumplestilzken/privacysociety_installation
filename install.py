#!/usr/bin/env python3

import os


def adb_reboot_fastboot_and_flash():
    answer = input("Prepare device for flashing according to README, press Enter when the phone is connected...")
    os.system("adb reboot bootloader")
    answer = input("Press Volume Up on the device when prompted...Press enter to continue")
    os.system("fastboot flashing unlock")
    os.system("fastboot flash boot boot.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta vbmeta.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_vendor vbmeta_vendor.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_system vbmeta_system.img")
    os.system("fastboot flash super super.img")
    print("The phone will now reboot into LineageOS")
    os.system("fastboot reboot")


def main():
    adb_reboot_fastboot_and_flash()
    return


if __name__ == '__main__':
    main()
