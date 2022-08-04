import psutil
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
    log.debug("mountpoints: %s", mountpoints)
    for mp in mountpoints:
        log.debug("mp: %s", mp)

        if "gisled" in mp.mountpoint:
            log.debug("gisled mp: %s", mp)
            return mp.mountpoint

    return None