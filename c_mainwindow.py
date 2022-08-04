import time

import qdarkstyle as qdarkstyle
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QLineEdit, QFrame, QWidget, QLabel, QSizePolicy, QPushButton, \
    QGroupBox, QVBoxLayout, QRadioButton
from PyQt5 import QtWidgets
import pyqtgraph as pg

import utils_usb
from pyqt_worker import Worker
import threading
import psutil
import log_utils

log = log_utils.logging_init(__file__)





class MainUi(QMainWindow):

    def __init__(self):
        super().__init__()
        pg.setConfigOptions(antialias=True)

        self.setWindowOpacity(1.0)  # 窗口透明度
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.init_ui()

        self.gisled_machine_connected_status = False
        self.gisled_mount_point = None
        self.find_gisled_machine_mutex = threading.Lock()
        #self.search_gisled = utils_usb.find_gisled_machine()
        self.thread = Worker(method=self.search_gisled)
        self.thread.start()



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
        self.lineedit_gisled_machine_cpu_serial_number = QLabel(self.widget)
        self.lineedit_gisled_machine_cpu_serial_number.setFont(self._font)
        self.lineedit_gisled_machine_cpu_serial_number.setText("NA")

        self.label_gisled_machine_eth_mac = QLabel(self.widget)
        self.label_gisled_machine_eth_mac.setFont(self._font)
        self.label_gisled_machine_eth_mac.setText("GISTLED Machine ETH MAC : ")
        self.lineedit_gisled_machine_eth_mac = QLabel(self.widget)
        self.lineedit_gisled_machine_eth_mac.setFont(self._font)
        self.lineedit_gisled_machine_eth_mac.setText("NA")
        self.label_gisled_machine_wlan_mac = QLabel(self.widget)
        self.label_gisled_machine_wlan_mac.setFont(self._font)
        self.label_gisled_machine_wlan_mac.setText("GISTLED Machine WLAN MAC : ")
        self.lineedit_gisled_machine_wlan_mac = QLabel(self.widget)
        self.lineedit_gisled_machine_wlan_mac.setFont(self._font)
        self.lineedit_gisled_machine_wlan_mac.setText("NA")
        self.label_gisled_machine_serial_number = QLabel(self.widget)
        self.label_gisled_machine_serial_number.setFont(self._font)
        self.label_gisled_machine_serial_number.setText("GISTLED Machine SN : ")
        self.lineedit_gisled_machine_serial_number = QLineEdit(self.widget)
        self.lineedit_gisled_machine_serial_number.setFont(self._font)
        self.lineedit_gisled_machine_serial_number.setText("NA")
        
        self.btn_write_gisled_machine_serial_number = QPushButton(self.widget)
        self.btn_write_gisled_machine_serial_number.setFont(self._font)
        self.btn_write_gisled_machine_serial_number.setText("Write Box SN")

        self.btn_write_gisled_machine_type = QPushButton(self.widget)
        self.btn_write_gisled_machine_type.setFont(self._font)
        self.btn_write_gisled_machine_type.setText("Write Box Type")

        self.btn_write_gisled_mp_file = QPushButton(self.widget)
        self.btn_write_gisled_mp_file.setFont(self._font)
        self.btn_write_gisled_mp_file.setText("Write MP File")

        self.groupbox_led_role = QGroupBox("GISLED Machine Type")
        self.groupbox_led_role.setFont(self._font)

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
        self.gridlayout.addWidget(self.label_gisled_machine_serial_number, 4, 0)
        self.gridlayout.addWidget(self.lineedit_gisled_machine_serial_number, 4, 1)

        self.gridlayout.addWidget(self.btn_write_gisled_machine_serial_number, 4, 3)
        self.gridlayout.addWidget(self.btn_write_gisled_mp_file, 0, 3)
        self.gridlayout.addWidget(self.groupbox_led_role, 5, 0, 2, 3)
        self.gridlayout.addWidget(self.btn_write_gisled_machine_type, 5, 3)


    def search_gisled(self):
        self.find_gisled_machine_mutex.acquire()
        self.gisled_machine_usb_dev = utils_usb.find_gisled_machine()
        if self.gisled_machine_usb_dev is not None:
            self.label_gisled_mount_status.setText("gisled machine connected")
            if self.gisled_machine_connected_status is False:
                log.debug("found gisled machine")
                self.gisled_mount_point = utils_usb.get_gisled_mountpoint()
                log.debug("gisled_mount_point : %s", self.gisled_mount_point)
                self.gisled_machine_connected_status = True

        self.find_gisled_machine_mutex.release()
        time.sleep(2)

