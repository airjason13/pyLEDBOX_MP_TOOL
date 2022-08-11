import platform

gisled_vid = 0x9527
gisled_pid = 0x5678

font_size = 18

file_name_gisled_cpu_serial_number = 'box_cpu_serial_number'
file_name_gisled_eth_mac_number = 'box_eth_mac_number'
file_name_gisled_wlan_mac_number = 'box_wlan_mac_number'
file_name_gisled_box_serial_number = 'box_serial_number'
file_name_gisled_machine_type = 'machine_type'
file_name_gisled_ledclient_version = 'ledclient_version'
file_name_gisled_ledserver_version = 'ledserver_version'
file_name_gisled_ledsystem_version = 'ledsystem_version'

machine_type_client = 'Client'
machine_type_server = 'Server'
machine_type_aio = 'AIO'

MP_FILE_NAME="GIS_LED_MP_LOG.xlsx"

if "Linux" in platform.system():
	print("Linux")
elif "Windows" in platform.system():
	print("Windows")
