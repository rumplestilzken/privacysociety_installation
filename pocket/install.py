#!/usr/bin/env python3

import os
import subprocess
from enum import Enum
from argparse import ArgumentParser, RawDescriptionHelpFormatter, Action

region = ""
filename = ""


class DeviceRegion(Enum):
    NotSet = ""
    TEE = "tee"
    EEA = "eea"


class EnumAction(Action):
    """Argparse action for handling Enums"""

    def __init__(self, **kwargs):
        enum_type = kwargs.pop("type", None)
        if enum_type is None:
            raise ValueError("Type must be assigned an Enum when using EnumAction")

        if not issubclass(enum_type, Enum):
            raise TypeError("Type must be an Enum when using EnumAction")

        kwargs.setdefault("choices", tuple(e.value for e in enum_type))

        super(EnumAction, self).__init__(**kwargs)
        self._enum = enum_type

    def __call__(self, parser, namespace, values, option_string=None):
        value = self._enum(values)
        setattr(namespace, self.dest, value)


def download_resources():
    here = os.path.dirname(os.path.realpath(__file__))

    global region
    global filename

    if region == DeviceRegion.TEE:
        filename = "2023010520_g66v71c2k_dfl_tee.tar.xz"
    elif region == DeviceRegion.EEA:
        filename = "2023010416_g66v71c2k_dfl_eea.tar.xz"

    if not os.path.exists(here + "/" + filename):
        print("Downloading Stock Rom")
        os.system("cd pocket; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                  "/rom_resources/" + filename)

    if not os.path.exists(here + "/" + filename.strip(".tar.xz")):
        print("Extracting Stock Rom")
        os.system("cd pocket; xz -kd " + filename)
        os.system("cd pocket; tar -xf " + filename.strip(".xz"))
        os.system("cd pocket; rm " + filename.strip(".xz"))

    img_filename = "privacysociety_pocket.img.xz"
    if not os.path.exists(here + "/" + img_filename):
        print("Downloading PrivacySociety GSI")
        os.system("cd pocket; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                  "/rom_resources/" + img_filename)
        print("Extracting PrivacySociety GSI")
        os.system("cd pocket; xz -kd " + img_filename)


def flash_stock():
    print("Flashing Stock Rom")
    global filename
    answer = input("Keep device connected. Press enter and reboot the device.")
    command = "cd pocket/" + filename.strip(".tar.xz") + "; mtk w preloader, recovery, vbmeta, vbmeta_system, " \
                                                         "vbmeta_vendor, md1img, spmfw, scp1, scp2, sspm_1, sspm_2, " \
                                                         "cam_vpu1, cam_vpu2, cam_vpu3, gz1, gz2, lk, lk2, boot, logo, " \
                                                         "dtbo, tee1, tee2, super, cache, userdata "

    command += "preloader_g66v71c2k_dfl_tee.bin, recovery.img, vbmeta.img, vbmeta_system.img, vbmeta_vendor.img, " \
               "md1img-verified.img, spmfw-verified.img, scp-verified.img, scp-verified.img, sspm-verified.img, " \
               "sspm-verified.img, cam_vpu1-verified.img, cam_vpu2-verified.img, cam_vpu3-verified.img, " \
               "gz-verified.img, gz-verified.img, lk-verified.img, lk-verified.img, boot.img, logo-verifiee.bin, " \
               "dtbo-verified.img, tee-verified.img, tee-verified.img, super.img, cache.img, userdata.img"

    os.system(command)

def mksuper():
    here = os.path.dirname(os.path.realpath(__file__))
    print("mksuper process running")

    if not os.path.exists(here + "/super.ext4.img"):
        subprocess.run(["python", here + "/../downloads/mksuper.py", " -dev pocket -gsi " + here + "/privacysociety_pocket.img -out " + here + "/super.ext4.img"])


def flash_lineage():
    print("Preparing to flash PrivacySociety GSI")
    here = os.path.dirname(os.path.realpath(__file__))

    answer = input("Disconnect the device from the computer. Plug back in and manually process according to README. "
                   "Press Enter to continue.")
    os.system("adb reboot bootloader")
    answer = input("Press Volume Up on the device when prompted...Press enter to continue")
    os.system("fastboot flashing unlock")
    os.system("fastboot flash boot " + here + "/" + filename + "/boot.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta " + here + "/" + filename + "/vbmeta.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_vendor " + here + "/" + filename + "/vbmeta_vendor.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_system " + here + "/" + filename + "/vbmeta_system.img")
    os.system("fastboot flash super " + here + "/super.ext4.img")
    print("The device will now reboot into PrivacySociety GSI")
    os.system("fastboot reboot")


def usage():
    print("""install.py
    -region: tee or eea""")


def parse_arguments():
    parser = ArgumentParser(formatter_class=RawDescriptionHelpFormatter, epilog=usage())
    parser.add_argument("-region", required=True, type=DeviceRegion, action=EnumAction, default=DeviceRegion.NotSet)
    return parser.parse_args()


def main():
    args = parse_arguments()

    global region
    region = args.region

    download_resources()
    mksuper()
    # flash_stock()
    # flash_lineage()

    return


if __name__ == '__main__':
    main()
