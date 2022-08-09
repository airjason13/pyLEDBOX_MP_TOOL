import psutil
from pathlib import Path
import usb.core
from global_defs import *
import log_utils

log = log_utils.logging_init(__file__)


def find_gisled_machine():
    devs = list(usb.core.find(find_all=True, idVendor=gisled_vid, idProduct=gisled_pid))

    # log.debug("find_pico")
    # was it found?
    if devs is None:
        # raise ValueError('Device not found')
        log.debug("no gisled machine")

    # for dev in devs:
    #    print("dev :", dev.get_active_configuration())
    return devs


def get_gisled_mountpoint():
    mountpoints = psutil.disk_partitions()
    # log.debug("mountpoints: %s", mountpoints)
    for mp in mountpoints:
        # log.debug("mp: %s", mp)
        if "gisled" in mp.mountpoint:
            # log.debug("gisled mp: %s", mp)
            return mp.mountpoint

    return 'NA'


def get_gisled_cpu_serial_number(mount_point):
    try:
        file_uri_gisled_serial_number = mount_point + "/" + file_name_gisled_cpu_serial_number
        f = open(file_uri_gisled_serial_number, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_eth_mac_number(mount_point):
    try:
        file_uri_gisled_eth_mac_number = mount_point + "/" + file_name_gisled_eth_mac_number
        f = open(file_uri_gisled_eth_mac_number, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_box_serial_number(mount_point):
    try:
        file_uri_gisled_box_serial_number = mount_point + "/" + file_name_gisled_box_serial_number
        f = open(file_uri_gisled_box_serial_number, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_box_type(mount_point):
    try:
        file_uri_gisled_box_machine_type = mount_point + "/" + file_name_gisled_machine_type
        f = open(file_uri_gisled_box_machine_type, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'

def get_gisled_wlan_mac_number(mount_point):
    try:
        file_uri_gisled_wlan_mac_number = mount_point + "/" + file_name_gisled_wlan_mac_number
        f = open(file_uri_gisled_wlan_mac_number, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_ledclient_version(mount_point):
    try:
        file_uri_gisled_ledclient_version = mount_point + "/" + file_name_gisled_ledclient_version
        f = open(file_uri_gisled_ledclient_version, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'

def get_gisled_ledserver_version(mount_point):
    try:
        file_uri_gisled_ledserver_version = mount_point + "/" + file_name_gisled_ledserver_version
        f = open(file_uri_gisled_ledserver_version, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'

def get_gisled_ledsystem_version(mount_point):
    try:
        file_uri_gisled_ledsystem_version = mount_point + "/" + file_name_gisled_ledsystem_version
        f = open(file_uri_gisled_ledsystem_version, "r")
        return f.read()
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def set_gisled_box_serial_number(mount_point, box_serial_number):
    try:
        file_uri_gisled_box_serial_number = mount_point + "/" + file_name_gisled_box_serial_number
        file = Path(file_uri_gisled_box_serial_number)
        file.touch(exist_ok=True)
        f = open(file_uri_gisled_box_serial_number, "w")
        f.write(box_serial_number)
        f.flush()
        f.close()
        return True
    except RuntimeError as e:
        log.debug(e)
        return False


def set_gisled_box_type(mount_point, machine_type):
    try:
        file_uri_gisled_box_type = mount_point + "/" + file_name_gisled_machine_type
        file = Path(file_uri_gisled_box_type)
        file.touch(exist_ok=True)
        f = open(file_uri_gisled_box_type, "w")
        f.write(machine_type)
        f.flush()
        f.close()
        return True
    except RuntimeError as e:
        log.debug(e)
        return False
