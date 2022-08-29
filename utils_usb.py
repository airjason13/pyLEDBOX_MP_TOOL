import psutil
from pathlib import Path
import os.path
import usb.core
from global_defs import *
import log_utils
import datetime
import utils_sn_fops

log = log_utils.logging_init(__file__)


def find_gisled_machine():
    devs = list(usb.core.find(find_all=True, idVendor=gisled_vid, idProduct=gisled_pid))

    # log.debug("devs : %s", devs)
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
        if os.path.isfile(file_uri_gisled_serial_number):
            f = open(file_uri_gisled_serial_number, "r")
            return f.read()
        else:
            log.debug("No file")
            return 'NA'
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_eth_mac_number(mount_point):
    try:
        file_uri_gisled_eth_mac_number = mount_point + "/" + file_name_gisled_eth_mac_number
        if os.path.isfile(file_uri_gisled_eth_mac_number):
            f = open(file_uri_gisled_eth_mac_number, "r")
            return f.read()
        else:
            log.debug("No file")
            return 'NA'
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_box_serial_number(mount_point):
    try:
        file_uri_gisled_box_serial_number = mount_point + "/" + file_name_gisled_box_serial_number
        if os.path.isfile(file_uri_gisled_box_serial_number):
            f = open(file_uri_gisled_box_serial_number, "r")
            return f.read()
        else:
            if os.path.exists(mount_point) is False:
                log.debug("No file")
                return 'NA'''
            else:
                box_serial_number = generate_box_serial_number(mount_point)
                file = Path(file_uri_gisled_box_serial_number)
                file.touch(exist_ok=True)
                f = open(file_uri_gisled_box_serial_number, "w")
                f.write(box_serial_number)
                f.flush()
                f.close()
                log.debug("write box serial number")
                return box_serial_number
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_box_type(mount_point):
    try:
        file_uri_gisled_box_machine_type = mount_point + "/" + file_name_gisled_machine_type
        if os.path.isfile(file_uri_gisled_box_machine_type):
            f = open(file_uri_gisled_box_machine_type, "r")
            return f.read()
        else:
            log.debug("No file")
            return 'NA'
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_wlan_mac_number(mount_point):
    try:
        file_uri_gisled_wlan_mac_number = mount_point + "/" + file_name_gisled_wlan_mac_number
        if os.path.isfile(file_uri_gisled_wlan_mac_number):
            f = open(file_uri_gisled_wlan_mac_number, "r")
            return f.read()
        else:
            log.debug("No file")
            return 'NA'
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_ledclient_version(mount_point):
    try:
        file_uri_gisled_ledclient_version = mount_point + "/" + file_name_gisled_ledclient_version
        if os.path.isfile(file_uri_gisled_ledclient_version):
            f = open(file_uri_gisled_ledclient_version, "r")
            return f.read()
        else:
            log.debug("No file")
            return 'NA'
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_ledserver_version(mount_point):
    try:
        file_uri_gisled_ledserver_version = mount_point + "/" + file_name_gisled_ledserver_version
        if os.path.isfile(file_uri_gisled_ledserver_version):
            f = open(file_uri_gisled_ledserver_version, "r")
            return f.read()
        else:
            log.debug("No file")
            return 'NA'
    except RuntimeError as e:
        log.debug(e)
        return 'NA'


def get_gisled_ledsystem_version(mount_point):
    try:
        file_uri_gisled_ledsystem_version = mount_point + "/" + file_name_gisled_ledsystem_version
        if os.path.isfile(file_uri_gisled_ledsystem_version):
            f = open(file_uri_gisled_ledsystem_version, "r")
            return f.read()
        else:
            log.debug("No file")
            return 'NA'
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
    if mount_point == "NA" :
        return False
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


def get_week_number():
    date_today = datetime.date.today()
    year, week_num, day_of_week = date_today.isocalendar()
    return week_num


def get_box_serial_number_prefix():
    return BOX_SERIAL_NUMBER_PREFIX


def generate_box_serial_number(mount_point):
    box_sn_prefix = get_box_serial_number_prefix()
    box_type = get_gisled_box_type(mount_point)[0]
    log.debug("box_type : %s", box_type)
    box_generation = get_gisled_ledclient_version(mount_point).split("_")[1].replace("G", "A")
    log.debug("box_generation : %s", box_generation)
    year = datetime.datetime.now().date().strftime("%Y")[1:]
    log.debug("year : %s", year)
    week_number = str(get_week_number())
    machine_count = utils_sn_fops.get_week_product_sn_from_snfile()
    utils_sn_fops.increase_week_product_sn()
    log.debug("machine_count : %s", str(machine_count))
    serial_number = box_sn_prefix + "_" + box_type + box_generation + year + week_number + machine_count
    log.debug("serial_number = %s", serial_number)
    return serial_number


