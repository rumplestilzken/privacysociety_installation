#!/usr/bin/env python3

from enum import Enum
import subprocess


class DeviceType(Enum):
    NotSet = ""
    Pocket = "pocket"
    Jelly2E = "jelly2e"
    AtomL = "atoml"


class DeviceRegion(Enum):
    NotSet = ""
    TEE = "tee"
    EEA = "eea"


def main():
    dev = DeviceType.NotSet
    region = DeviceRegion.NotSet

    answer = input("Which device would you like to flash?\n1)Titan Pocket\n2)Jelly 2E\n3)Atom L\nSelection:")
    match answer:
        case "1":
            dev = DeviceType.Pocket
        case "2":
            dev = DeviceType.Jelly2E
        case "3":
            dev = DeviceType.AtomL
        case _:
            print("Invalid Selection.")
            quit()

    answer = input("Which region is your device?\n1)TEE\n2)EEA\nSelection:")
    match answer:
        case "1":
            region = DeviceRegion.TEE
        case "2":
            region = DeviceRegion.EEA
        case _:
            print("Invalid Selection.")
            quit()

    print("Device Type: '" + dev.name + "' Region: '" + region.name + "'")
    answer = input("Have you read and understood the flashing instructions for this device? Press enter.")
    answer = input("Connect the device to the computer. Press Enter.")

    script = ""

    match dev:
        case DeviceType.Pocket:
            script = "pocket/install.py"
        case DeviceType.Jelly2E:
            script = "jelly2e/install.py"
        case DeviceType.AtomL:
            script = "atoml/install.py"
        case _:
            print("Device type '" + dev.name + "' not supported.")

    subprocess.check_call(['python', script, '-region', region.value])

    print("Flashing Complete.")

    return


if __name__ == '__main__':
    main()
