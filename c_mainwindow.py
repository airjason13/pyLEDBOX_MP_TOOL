import time

import qdarkstyle as qdarkstyle
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLineEdit, QFrame, QWidget, QLabel, QSizePolicy, QPushButton, \
    QGroupBox, QVBoxLayout, QRadioButton
from PyQt5 import QtWidgets
import pyqtgraph as pg
from global_defs import *
import utils_usb
from pyqt_worker import Worker
import threading
import psutil
from utils_xls import XlsMod
import log_utils

log = log_utils.logging_init(__file__)





class MainUi(QMainWindow):

    def __init__(self):
        super().__init__()
        pg.setConfigOptions(antialias=True)

        self.setWindowOpacity(1.0)  # 窗口透明度
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.engineer_mode = False
        self.init_ui()

        self.gisled_machine_connected_status = False
        self.gisled_mount_point = 'NA'
        self.gisled_machine_usb_dev = None
        self.machine_type = machine_type_client
        self.find_gisled_machine_mutex = threading.Lock()

        # self.search_gisled = utils_usb.find_gisled_machine()
        self.thread = Worker(method=self.search_gisled)
        self.thread.start()

        self.xls = XlsMod("/home/venom/" + MP_FILE_NAME, self)


    def init_ui(self):
        self.resize(1280, 720)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self._font = QFont()
        self._fontScale = 1
        self._font.setPixelSize(24 * self._fontScale)
        self.setFont(self._font)
        self.setWindowTitle("GIS TLED MP Tool")
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.gridlayout = QGridLayout(self.widget)
        self.label_gisled_mount_status = QLabel(self.widget)
        self.label_gisled_mount_status.setFont(self._font)
        self.label_gisled_mount_status.setText("GISTLED box does not connected!")

        self.label_gisled_machine_cpu_serial_number = QLabel(self.widget)
        self.label_gisled_machine_cpu_serial_number.setFont(self._font)
        self.label_gisled_machine_cpu_serial_number.setText("GISTLED Machine CPU SN : ")
        self.lineedit_gisled_machine_cpu_serial_number = QLineEdit(self.widget)
        self.lineedit_gisled_machine_cpu_serial_number.setFont(self._font)
        self.lineedit_gisled_machine_cpu_serial_number.setText("NA")
        self.lineedit_gisled_machine_cpu_serial_number.setReadOnly(True)

        self.label_gisled_machine_eth_mac = QLabel(self.widget)
        self.label_gisled_machine_eth_mac.setFont(self._font)
        self.label_gisled_machine_eth_mac.setText("GISTLED Machine ETH MAC : ")
        self.lineedit_gisled_machine_eth_mac = QLineEdit(self.widget)
        self.lineedit_gisled_machine_eth_mac.setFont(self._font)
        self.lineedit_gisled_machine_eth_mac.setText("NA")
        self.lineedit_gisled_machine_eth_mac.setReadOnly(True)

        self.label_gisled_machine_wlan_mac = QLabel(self.widget)
        self.label_gisled_machine_wlan_mac.setFont(self._font)
        self.label_gisled_machine_wlan_mac.setText("GISTLED Machine WLAN MAC : ")
        self.lineedit_gisled_machine_wlan_mac = QLineEdit(self.widget)
        self.lineedit_gisled_machine_wlan_mac.setFont(self._font)
        self.lineedit_gisled_machine_wlan_mac.setText("NA")
        self.lineedit_gisled_machine_wlan_mac.setReadOnly(True)
        self.label_gisled_machine_serial_number = QLabel(self.widget)
        self.label_gisled_machine_serial_number.setFont(self._font)
        self.label_gisled_ledclient_version = QLabel(self.widget)
        self.label_gisled_ledclient_version.setFont(self._font)
        self.label_gisled_ledclient_version.setText("GISTLED Ledclient Version : ")
        self.lineedit_gisled_ledclient_version = QLineEdit(self.widget)
        self.lineedit_gisled_ledclient_version.setFont(self._font)
        self.lineedit_gisled_ledclient_version.setText("NA")
        self.lineedit_gisled_machine_wlan_mac.setReadOnly(True)

        self.label_gisled_ledserver_version = QLabel(self.widget)
        self.label_gisled_ledserver_version.setFont(self._font)
        self.label_gisled_ledserver_version.setText("GISTLED Ledserver Version : ")
        self.lineedit_gisled_ledserver_version = QLineEdit(self.widget)
        self.lineedit_gisled_ledserver_version.setFont(self._font)
        self.lineedit_gisled_ledserver_version.setText("NA")
        self.lineedit_gisled_ledserver_version.setReadOnly(True)

        self.label_gisled_system_version = QLabel(self.widget)
        self.label_gisled_system_version.setFont(self._font)
        self.label_gisled_system_version.setText("GISTLED System Version : ")
        self.lineedit_gisled_system_version = QLineEdit(self.widget)
        self.lineedit_gisled_system_version.setFont(self._font)
        self.lineedit_gisled_system_version.setText("NA")
        self.lineedit_gisled_system_version.setReadOnly(True)

        self.label_gisled_machine_serial_number.setText("GISTLED Machine SN : ")
        self.lineedit_gisled_machine_serial_number = QLineEdit(self.widget)
        self.lineedit_gisled_machine_serial_number.setFont(self._font)
        self.lineedit_gisled_machine_serial_number.setText("NA")
        
        self.btn_write_gisled_machine_serial_number = QPushButton(self.widget)
        self.btn_write_gisled_machine_serial_number.setFont(self._font)
        self.btn_write_gisled_machine_serial_number.setText("Write Box SN")
        self.btn_write_gisled_machine_serial_number.clicked.connect(self.write_gisled_machine_serial_number)

        self.btn_write_gisled_machine_type = QPushButton(self.widget)
        self.btn_write_gisled_machine_type.setFont(self._font)
        self.btn_write_gisled_machine_type.setText("Write Box Type")
        self.btn_write_gisled_machine_type.clicked.connect(self.write_gisled_machine_type)

        self.btn_write_gisled_mp_file = QPushButton(self.widget)
        self.btn_write_gisled_mp_file.setFont(self._font)
        self.btn_write_gisled_mp_file.setText("Write MP File")
        self.btn_write_gisled_mp_file.clicked.connect(self.write_gisled_mp_sheet)

        self.btn_engineer_mode = QPushButton(self.widget)
        self.btn_engineer_mode.setFont(self._font)
        self.btn_engineer_mode.setText("Engineer Mode")
        self.btn_engineer_mode.clicked.connect(self.trigger_engineer_mode)

        if self.engineer_mode is False:
            self.btn_write_gisled_machine_type.setVisible(False)
            self.btn_write_gisled_machine_serial_number.setVisible(False)

        self.groupbox_led_role = QGroupBox("GISLED Machine Type")
        self.groupbox_led_role.setFont(self._font)
        # self.groupbox_led_role.setGeometry(0, 0, 320, 360)

        self.groupbox_led_role_vboxlayout = QVBoxLayout()
        self.groupbox_led_role.setLayout(self.groupbox_led_role_vboxlayout)
        self.radiobutton_ledrole_client = QRadioButton("Client LEDBox")
        self.radiobutton_ledrole_client.setChecked(True)
        self.groupbox_led_role_vboxlayout.addWidget(self.radiobutton_ledrole_client)

        self.radiobutton_ledrole_server = QRadioButton("Server LEDBox")
        self.groupbox_led_role_vboxlayout.addWidget(self.radiobutton_ledrole_server)

        self.radiobutton_ledrole_aio = QRadioButton("AIO LEDBox")
        self.groupbox_led_role_vboxlayout.addWidget(self.radiobutton_ledrole_aio)

        self.gridlayout.addWidget(self.label_gisled_mount_status, 0, 0)
        self.gridlayout.addWidget(self.label_gisled_machine_cpu_serial_number, 1, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_machine_cpu_serial_number, 1, 1)
        self.gridlayout.addWidget(self.label_gisled_machine_eth_mac, 2, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_machine_eth_mac, 2, 1)
        self.gridlayout.addWidget(self.label_gisled_machine_wlan_mac, 3, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_machine_wlan_mac, 3, 1)
        self.gridlayout.addWidget(self.label_gisled_ledclient_version, 4, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_ledclient_version, 4, 1)
        self.gridlayout.addWidget(self.label_gisled_ledserver_version, 5, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_ledserver_version, 5, 1)
        self.gridlayout.addWidget(self.label_gisled_system_version, 6, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_system_version, 6, 1)

        self.gridlayout.addWidget(self.label_gisled_machine_serial_number, 7, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_machine_serial_number, 7, 1)

        self.gridlayout.addWidget(self.btn_write_gisled_machine_serial_number, 7, 3)
        self.gridlayout.addWidget(self.btn_write_gisled_mp_file, 0, 3)
        self.gridlayout.addWidget(self.groupbox_led_role, 8, 0, 3, 3)
        self.gridlayout.addWidget(self.btn_write_gisled_machine_type, 8, 3)
        self.gridlayout.addWidget(self.btn_engineer_mode, 10, 3)



    def search_gisled(self):
        self.find_gisled_machine_mutex.acquire()
        self.gisled_machine_usb_dev = utils_usb.find_gisled_machine()
        if self.gisled_machine_usb_dev is not None:
            self.gisled_mount_point = utils_usb.get_gisled_mountpoint()
            # log.debug("gisled_mount_point : %s", self.gisled_mount_point)
            self.label_gisled_mount_status.setText("gisled machine connected at " + self.gisled_mount_point)
            if self.gisled_machine_connected_status is False:
                # log.debug("found gisled machine")
                # get machine info
                self.lineedit_gisled_machine_cpu_serial_number.setText(
                    utils_usb.get_gisled_cpu_serial_number(self.gisled_mount_point))
                self.lineedit_gisled_machine_eth_mac.setText(
                    utils_usb.get_gisled_eth_mac_number(self.gisled_mount_point))
                self.lineedit_gisled_machine_wlan_mac.setText(
                    utils_usb.get_gisled_wlan_mac_number(self.gisled_mount_point))
                self.lineedit_gisled_ledclient_version.setText(
                    utils_usb.get_gisled_ledclient_version(self.gisled_mount_point))
                self.lineedit_gisled_ledserver_version.setText(
                    utils_usb.get_gisled_ledserver_version(self.gisled_mount_point))
                self.lineedit_gisled_system_version.setText(
                    utils_usb.get_gisled_ledsystem_version(self.gisled_mount_point))

                self.lineedit_gisled_machine_serial_number.setText(
                    utils_usb.get_gisled_box_serial_number(self.gisled_mount_point))


                self.machine_type = utils_usb.get_gisled_box_type(self.gisled_mount_point)


                if machine_type_aio in self.machine_type:
                    self.radiobutton_ledrole_aio.setChecked(True)
                elif machine_type_server in self.machine_type:
                    self.radiobutton_ledrole_server.setChecked(True)
                else:
                    self.radiobutton_ledrole_client.setChecked(True)
                    self.write_gisled_machine_type()
                if utils_usb.get_gisled_cpu_serial_number(self.gisled_mount_point) == 'NA':
                    self.gisled_machine_connected_status = False
                else:
                    self.gisled_machine_connected_status = True

        else:
            self.label_gisled_mount_status.setText("gisled machine disconnected")
            self.gisled_machine_connected_status = False
        self.find_gisled_machine_mutex.release()
        time.sleep(2)

    def write_gisled_machine_serial_number(self):
        log.debug("sn : %s", self.lineedit_gisled_machine_serial_number.text())
        ret = utils_usb.set_gisled_box_serial_number(self.gisled_mount_point,
                                                     self.lineedit_gisled_machine_serial_number.text())
        if ret is False:
            log.fatal("write machine serial number error!")

    def write_gisled_machine_type(self):
        if self.radiobutton_ledrole_client.isChecked():
            self.machine_type = machine_type_client
        elif self.radiobutton_ledrole_server.isChecked():
            self.machine_type = machine_type_server
        elif self.radiobutton_ledrole_aio.isChecked():
            self.machine_type = machine_type_aio
        log.debug("machine_type : %s", self.machine_type)
        ret = utils_usb.set_gisled_box_type(self.gisled_mount_point, self.machine_type)

    def write_gisled_mp_sheet(self):
        self.xls.write_cpu_serial_number(utils_usb.get_gisled_cpu_serial_number(self.gisled_mount_point))
        self.xls.write_box_serial_number(utils_usb.get_gisled_box_serial_number(self.gisled_mount_point))
        self.xls.write_eth_mac_address(utils_usb.get_gisled_eth_mac_number(self.gisled_mount_point))
        self.xls.write_wlan_mac_address(utils_usb.get_gisled_wlan_mac_number(self.gisled_mount_point))
        self.xls.write_ledclient_sw_version(utils_usb.get_gisled_ledclient_version(self.gisled_mount_point))
        self.xls.write_ledserver_sw_version(utils_usb.get_gisled_ledserver_version(self.gisled_mount_point))
        self.xls.write_ledsystem_sw_version(utils_usb.get_gisled_ledsystem_version(self.gisled_mount_point))

        self.xls.save_work_sheet()
        self.xls.increase_working_row()

    def trigger_engineer_mode(self):
        if self.engineer_mode is False:
            self.engineer_mode = True
        else:
            self.engineer_mode = False

        if self.engineer_mode is True:
            self.btn_write_gisled_machine_type.setVisible(True)
            self.btn_write_gisled_machine_serial_number.setVisible(True)
        else:
            self.btn_write_gisled_machine_type.setVisible(False)
            self.btn_write_gisled_machine_serial_number.setVisible(False)
