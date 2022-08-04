# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from c_mainwindow import MainUi
import sys
from PyQt5.QtWidgets import QApplication

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    qt_app = QApplication(sys.argv)
    gui = MainUi()
    gui.show()

    #qt_app.focusChanged.connect(gui.focus_on_window_changed)

    sys.exit(qt_app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
