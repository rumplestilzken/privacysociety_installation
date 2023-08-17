#!/usr/bin/env python3

import os
from enum import Enum
from argparse import ArgumentParser, RawDescriptionHelpFormatter, Action
import subprocess

region = ""
filename = ""
magisk_filename = ""
sp_flash_tool_filename = ""


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
        os.system("cd " + here + "; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                  "/rom_resources/" + filename)

    if not os.path.exists(here + "/" + filename.strip(".tar.xz")):
        print("Extracting Stock Rom")
        os.system("cd " + here + "; xz -kd " + filename)
        os.system("cd " + here + "; tar -xf " + filename.strip(".xz"))
        os.system("cd " + here + "; rm " + filename.strip(".xz"))


    img_filename = "privacysociety_pocket.img.xz"
    if not os.path.exists(here + "/" + img_filename):
        print("Downloading PrivacySociety GSI")
        os.system("cd " + here + "; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                  "/rom_resources/" + img_filename)
        print("Extracting PrivacySociety GSI")
        os.system("cd " + here + "; xz -kd " + img_filename)

    global magisk_filename
    magisk_filename = ""
    if region == DeviceRegion.TEE:
        magisk_filename = "magisk_patched-25200_H63Lj.img"
    else:
        magisk_filename = "magisk_patched-25200_h3ilq.img"

    if not os.path.exists(here + "/" + magisk_filename):
        print("Downloading Magisk Boot Image")
        os.system("cd " + here + "; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                  "/rom_resources/" + magisk_filename)

    global sp_flash_tool_filename
    sp_flash_tool_filename = "SP_Flash_Tool_v5.2152_Linux.zip"
    if not os.path.exists(here + "/../downloads/" + sp_flash_tool_filename):
        print("Downloading Magisk Boot Image")
        os.system("cd " + here + "/../downloads/; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                  "/rom_resources/" + sp_flash_tool_filename)
        os.system("cd " + here + "/../downloads; unzip " + sp_flash_tool_filename)

    if not os.path.exists(here + "/../downloads/Magisk-v25.2.apk"):
        os.system("cd " + here + "/../downloads/; wget https://github.com/rumplestilzken/privacysociety_installation/releases"
                  "/download/rom_resources/Magisk-v25.2.apk")

    lk_filename = "lk." + filename.strip(".tar.xz")

    if not os.path.exists(here + "/" + lk_filename + ".img"):
        print("Downloading lk Image")
        os.system("cd " + here + "; wget https://github.com/rumplestilzken/privacysociety_installation/releases/download"
                  "/rom_resources/" + lk_filename + ".img")

def flash_stock():
    here = os.path.dirname(os.path.realpath(__file__))
    print("Flashing Stock Rom")
    global filename
    answer = input("Keep device connected. Press enter and reboot or power on the device.")
    os.system("cd downloads/" + sp_flash_tool_filename.strip(".zip") + "; chmod +x flash_tool")
    command = "cd downloads/" + sp_flash_tool_filename.strip(
        ".zip") + "; ./flash_tool -d MTK_AllInOne_DA.bin -s " + here + "/" + filename.strip(
        ".tar.xz") + "/MT6771_Android_scatter.txt -c firmware-upgrade"
    print(command)
    os.system(command)


def mksuper():
    here = os.path.dirname(os.path.realpath(__file__))
    print("mksuper process running")

    if not os.path.exists(here + "/super." + filename.strip(".tar.xz") + ".ext4.img"):
        if not os.path.exists(here + "/../downloads/mksuper/simg2img/simg2img"):
            os.system("cd " + here + "/../downloads/mksuper/; python install-dependencies.py")
        if not os.path.exists(here + "/super_" + filename.strip(".tar.xz")):
            os.system("cd " + here + "/../downloads/mksuper/; python extract.py -stock " + here + "/" \
                      + filename.strip(".tar.xz") + " -out " + here + "/super_" + filename.strip(".tar.xz"))
        os.system("cd " + here + "/../downloads/mksuper/; python mksuper.py -dev pocket -gsi " + here \
                  + "/privacysociety_pocket.img" + " -out " + here + "/super." + filename.strip(
            ".tar.xz") + ".ext4.img -super_path " + here + "/super_" + filename.strip(".tar.xz"))


def flash_lineage():
    print("Preparing to flash PrivacySociety GSI")
    here = os.path.dirname(os.path.realpath(__file__))

    answer = input("Let device power on and manually process according to README. Press Enter to continue.")
    os.system("adb kill-server")
    os.system("adb shell; exit")
    os.system("adb reboot bootloader")
    answer = input("Press Volume Up on the device when prompted...Press enter to continue")
    os.system("fastboot flashing unlock")
    output = subprocess.check_output("fastboot flash boot " + here + "/" + magisk_filename)
    while "not allowed in locked state" in output:
        print("Unlocking attempt failed. Please try again. Press Volume Up when prompted. Press enter when ready.")
        os.system("fastboot flashing unlock")
        output = subprocess.check_output("fastboot flash boot " + here + "/" + magisk_filename)

    os.system("fastboot flash --disable-verity --disable-verification vbmeta " + here + "/" + filename.strip(
        ".tar.xz") + "/vbmeta.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_vendor " + here + "/" + filename.strip(
        ".tar.xz") + "/vbmeta_vendor.img")
    os.system("fastboot flash --disable-verity --disable-verification vbmeta_system " + here + "/" + filename.strip(
        ".tar.xz") + "/vbmeta_system.img")
    os.system("fastboot flash lk " + here + "/lk." + filename.strip(".tar.xz") + ".img")
    os.system("fastboot flash lk2 " + here + "/lk." + filename.strip(".tar.xz") + ".img")
    os.system("fastboot flash super " + here + "/super." + filename.strip(".tar.xz") + ".ext4.img")
    os.system("fastboot reboot")
    print("The device will now reboot into PrivacySociety GSI")


def install_magisk():
    answer = input("Once the phone has booted  into PrivacySociety GSI and been set up, press Enter.")
    here = os.path.dirname(os.path.realpath(__file__))
    print("Installing Magisk")

    os.system("adb install " + here + "/../downloads/Magisk-v25.2.apk")


def apply_kika():
    os.system("adb shell pm enable com.iqqijni.bbkeyboard; adb shell ime enable "
              "com.iqqijni.bbkeyboard/.keyboard_service.view.HDKeyboardService; adb shell ime set "
              "com.iqqijni.bbkeyboard/.keyboard_service.view.HDKeyboardService;")


def open_magisk():
    answer = input("Press Enter and tap Allow and Ok to reboot.")
    os.system("adb shell monkey -p com.topjohnwu.magisk 1")


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
    flash_stock()
    flash_lineage()
    install_magisk()
    apply_kika()
    open_magisk()

    return


if __name__ == '__main__':
    main()
