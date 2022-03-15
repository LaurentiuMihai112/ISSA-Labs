from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import threading
import sys
import time

HOST = 'localhost'
PORT = 5005
client = 0
DIAG = False

led0_flag = False
led1_flag = False
led2_flag = False
led3_flag = False


class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(658, 500)
        main_window.setMinimumSize(QtCore.QSize(658, 500))
        main_window.setMaximumSize(QtCore.QSize(658, 500))
        self.logo_img = QtGui.QPixmap('./rsz_conti.png')
        self.centralwidget = QtWidgets.QWidget(main_window)
        main_window.setWindowTitle('Client')
        self.centralwidget.setObjectName("centralwidget")
        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(150, 20, 400, 100))
        self.logo.setObjectName("logo")
        self.connected_msg = QtWidgets.QLabel(self.centralwidget)
        self.connected_msg.setGeometry(QtCore.QRect(292, 175, 85, 30))
        self.connected_msg.setObjectName("connected_msg")
        self.connected_msg.setStyleSheet("font: bold; color: green")
        self.not_diag_mode = QtWidgets.QLabel(self.centralwidget)
        self.not_diag_mode.setGeometry(QtCore.QRect(272, 187, 120, 30))
        self.not_diag_mode.setObjectName("not_diag_mode")
        self.not_diag_mode.setStyleSheet("font: bold; color: red")
        self.not_diag_mode.setVisible(False)
        self.diagMode = QtWidgets.QPushButton(self.centralwidget)
        self.diagMode.setGeometry(QtCore.QRect(185, 210, 131, 41))
        self.diagMode.setObjectName("diagMode")
        self.diagMode.clicked.connect(self.diag)
        self.diagMode.setEnabled(False)
        self.diagMode_off = QtWidgets.QPushButton(self.centralwidget)
        self.diagMode_off.setGeometry(QtCore.QRect(325, 210, 131, 41))
        self.diagMode_off.setObjectName("diagMode")
        self.diagMode_off.setEnabled(False)
        self.diagMode_off.clicked.connect(self.stop_diag)

        self.set_led0 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led0.setGeometry(QtCore.QRect(30, 310, 81, 31))
        self.set_led0.clicked.connect(self.set_led0_flags)

        self.set_led1 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led1.setGeometry(QtCore.QRect(30, 350, 81, 31))
        self.set_led1.clicked.connect(self.set_led1_flags)

        self.set_led2 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led2.setGeometry(QtCore.QRect(30, 390, 81, 31))
        self.set_led2.clicked.connect(self.set_led2_flags)

        self.set_led3 = QtWidgets.QPushButton(self.centralwidget)
        self.set_led3.setGeometry(QtCore.QRect(30, 430, 81, 31))
        self.set_led3.clicked.connect(self.set_led3_flags)

        self.led0_state = QtWidgets.QLabel(self.centralwidget)
        self.led0_state.setGeometry(QtCore.QRect(140, 313, 25, 25))
        self.led0_state.setVisible(False)

        self.led1_state = QtWidgets.QLabel(self.centralwidget)
        self.led1_state.setGeometry(QtCore.QRect(140, 353, 25, 25))
        self.led1_state.setVisible(False)

        self.led2_state = QtWidgets.QLabel(self.centralwidget)
        self.led2_state.setGeometry(QtCore.QRect(140, 393, 25, 25))
        self.led2_state.setVisible(False)

        self.led3_state = QtWidgets.QLabel(self.centralwidget)
        self.led3_state.setGeometry(QtCore.QRect(140, 433, 25, 25))
        self.led3_state.setVisible(False)

        self.set_led_title = QtWidgets.QLabel(self.centralwidget)
        self.set_led_title.setGeometry(QtCore.QRect(75, 270, 92, 21))
        self.set_led_title.setObjectName("set_led_title")
        self.set_led_title.setStyleSheet("font:bold; font-size:11px;")
        self.read_dtc_title = QtWidgets.QLabel(self.centralwidget)
        self.read_dtc_title.setGeometry(QtCore.QRect(470, 270, 101, 20))
        self.read_dtc_title.setObjectName("read_dtc_title")
        self.read_dtc_title.setStyleSheet("font:bold; font-size:11px;")

        self.dtc1 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc1.setGeometry(QtCore.QRect(460, 310, 81, 31))
        self.dtc1.clicked.connect(lambda: self.get_dtc_state('01'))

        self.dtc2 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc2.setGeometry(QtCore.QRect(460, 350, 81, 31))
        self.dtc2.clicked.connect(lambda: self.get_dtc_state('02'))

        self.dtc3 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc3.setGeometry(QtCore.QRect(460, 390, 81, 31))
        self.dtc3.clicked.connect(lambda: self.get_dtc_state('03'))

        self.dtc4 = QtWidgets.QPushButton(self.centralwidget)
        self.dtc4.setGeometry(QtCore.QRect(460, 430, 81, 31))
        self.dtc4.clicked.connect(lambda: self.get_dtc_state('04'))

        self.dtc1_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc1_state.setGeometry(QtCore.QRect(570, 315, 65, 20))
        self.dtc1_state.setText('Unknown')
        self.dtc1_state.setStyleSheet('font:bold; color: blue')

        self.dtc2_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc2_state.setGeometry(QtCore.QRect(570, 355, 65, 20))
        self.dtc2_state.setText('Unknown')
        self.dtc2_state.setStyleSheet('font:bold; color: blue')

        self.dtc3_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc3_state.setGeometry(QtCore.QRect(570, 395, 65, 20))
        self.dtc3_state.setText('Unknown')
        self.dtc3_state.setStyleSheet('font:bold; color: blue')

        self.dtc4_state = QtWidgets.QLabel(self.centralwidget)
        self.dtc4_state.setGeometry(QtCore.QRect(570, 435, 65, 20))
        self.dtc4_state.setText('Unknown')
        self.dtc4_state.setStyleSheet('font:bold; color: blue')

        self.connect = QtWidgets.QPushButton(self.centralwidget)
        self.connect.setGeometry(QtCore.QRect(260, 130, 131, 51))
        self.connect.setObjectName("connect")
        self.connect.clicked.connect(self.start_client)
        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 658, 21))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo.setPixmap(self.logo_img)
        self.connected_msg.setText(_translate("MainWindow", ""))
        self.not_diag_mode.setText(_translate("MainWindow", "NOT IN DIAG MODE"))
        self.diagMode.setText(_translate("MainWindow", "Enter Diag Mode"))
        self.diagMode_off.setText(_translate("MainWindow", "Stop Diag Mode"))
        self.set_led0.setText(_translate("MainWindow", "Set LED0"))
        self.set_led1.setText(_translate("MainWindow", "Set LED1"))
        self.set_led2.setText(_translate("MainWindow", "Set LED2"))
        self.set_led3.setText(_translate("MainWindow", "Set LED3"))

        self.set_led_title.setText(_translate("MainWindow", "SET LED STATES"))
        self.read_dtc_title.setText(_translate("MainWindow", "READ DTC STATES"))
        self.dtc3.setText(_translate("MainWindow", "Read DTC3"))
        self.dtc2.setText(_translate("MainWindow", "Read DTC2"))
        self.dtc1.setText(_translate("MainWindow", "Read DTC1"))
        self.dtc4.setText(_translate("MainWindow", "Read DTC4"))
        self.led0_state.setText(_translate("MainWindow", ""))
        self.led1_state.setText(_translate("MainWindow", ""))
        self.led2_state.setText(_translate("MainWindow", ""))
        self.led3_state.setText(_translate("MainWindow", ""))
        self.connect.setText(_translate("MainWindow", "CONNECT"))

    # ############################## EXERCISE 0 ###############################
    def start_client(self):
        self.diagMode.setEnabled(True)
        self.diagMode_off.setEnabled(False)

        self.dtc1.setEnabled(True)
        self.dtc2.setEnabled(True)
        self.dtc3.setEnabled(True)
        self.dtc4.setEnabled(True)

        self.set_led0.setText('Set LED0')
        self.set_led1.setText('Set LED1')
        self.set_led2.setText('Set LED1')
        self.set_led3.setText('Set LED3')

        self.dtc1_state.setText('Unknown')
        self.dtc1_state.setStyleSheet('font:bold; color: blue;')
        self.dtc2_state.setText('Unknown')
        self.dtc2_state.setStyleSheet('font:bold; color: blue;')
        self.dtc3_state.setText('Unknown')
        self.dtc3_state.setStyleSheet('font:bold; color: blue;')
        self.dtc4_state.setText('Unknown')
        self.dtc4_state.setStyleSheet('font:bold; color: blue;')

        self.set_led0.setText('Set LED0')
        self.set_led1.setText('Set LED1')
        self.set_led2.setText('Set LED2')
        self.set_led3.setText('Set LED3')

        self.led0_state.setVisible(False)
        self.led1_state.setVisible(False)
        self.led2_state.setVisible(False)
        self.led3_state.setVisible(False)

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((HOST, PORT))
        self.connected_msg.setText('Connected')
        self.recv_messages()

    # ############################## EXERCISE 1 ###############################
    def recv_handler(self, stop_event):
        global DIAG
        while True:
            message = self.connection.recv(1024).decode()
            print(f"Message received:{message}")
            if DIAG:
                if message == 'Ox3E00':
                    DIAG = False
                if message.startswith('0x6E'):
                    led_number = int(message[-2])
                    data = int(message[-1])
                    if led_number == 0:
                        self.set_led0_label(data)
                    if led_number == 1:
                        self.set_led1_label(data)
                    if led_number == 2:
                        self.set_led2_label(data)
                    if led_number == 3:
                        self.set_led3_label(data)
                if message.startswith('0x62'):
                    dtc_number = int(message[5])
                    data = message[-5:]
                    print(data)
                    if dtc_number == 1:
                        self.set_dtc1_state(data)
                    if dtc_number == 2:
                        self.set_dtc2_state(data)
                    if dtc_number == 3:
                        self.set_dtc3_state(data)
                    if dtc_number == 4:
                        self.set_dtc4_state(data)

            elif message == 'Ox3E01':
                DIAG = True

    def recv_messages(self):
        self.stop_event = threading.Event()
        self.c_thread = threading.Thread(target=self.recv_handler, args=(self.stop_event,))
        self.c_thread.start()

    def diag(self):
        global DIAG
        DIAG = True
        self.diagMode.setEnabled(False)
        self.diagMode_off.setEnabled(True)
        self.connection.send('0x3E01'.encode())

    def stop_diag(self):
        global DIAG
        DIAG = False
        self.diagMode.setEnabled(True)
        self.diagMode_off.setEnabled(False)
        self.connection.send('0x3E00'.encode())

    # ############################## EXERCISE 3 ###############################
    # READ DTC's
    def get_dtc_state(self, dtc_string):
        self.connection.send('0x2201'.encode())

    # SET DTC1 State
    def set_dtc1_state(self, data_recv):
        if data_recv == '02550':
            self.dtc1_state.setStyleSheet('font:bold; color: green;')
            self.dtc1_state.setText("Active")
        elif data_recv == '25500':
            self.dtc1_state.setStyleSheet('font:bold; color: red;')
            self.dtc1_state.setText("Inactive")
        else:
            self.dtc1_state.setStyleSheet('font:bold; color: blue;')
            self.dtc1_state.setText("Unknown")

    # SET DTC2 State
    def set_dtc2_state(self, data_recv):
        pass

    # SET DTC3 State
    def set_dtc3_state(self, data_recv):
        pass

    # SET DTC4 State
    def set_dtc4_state(self, data_recv):
        pass

    # ############################## EXERCISE 4 ###############################

    # SET LED0
    def set_led0_label(self, data_recv):
        if data_recv:
            self.led0_state.setStyleSheet('background-color:green;')
        else:
            self.led0_state.setStyleSheet('background-color:red;')

    def set_led0_flags(self):
        global led0_flag
        if DIAG:
            if led0_flag:
                led0_flag = False
                self.connection.send('0x2E001'.encode())
            else:
                led0_flag = True
                self.connection.send('0x2E000'.encode())

    # SET LED1
    def set_led1_label(self, data_recv):
        if data_recv:
            self.led1_state.setStyleSheet('background-color:green;')
        else:
            self.led1_state.setStyleSheet('background-color:red;')

    def set_led1_flags(self):
        global led1_flag
        if DIAG:
            if led1_flag:
                led1_flag = False
                self.connection.send('0x2E011'.encode())
            else:
                led1_flag = True
                self.connection.send('0x2E010'.encode())

    # SET LED2
    def set_led2_label(self, data_recv):
        if data_recv:
            self.led2_state.setStyleSheet('background-color:green;')
        else:
            self.led2_state.setStyleSheet('background-color:red;')

    def set_led2_flags(self):
        global led2_flag
        if DIAG:
            if led2_flag:
                led2_flag = False
                self.connection.send('0x2E021'.encode())
            else:
                led2_flag = True
                self.connection.send('0x2E020'.encode())

    # SET LED3
    def set_led3_label(self, data_recv):
        if data_recv:
            self.led3_state.setStyleSheet('background-color:green;')
        else:
            self.led3_state.setStyleSheet('background-color:red;')

    def set_led3_flags(self):
        global led3_flag
        if DIAG:
            if led3_flag:
                led3_flag = False
                self.connection.send('0x2E031'.encode())
            else:
                led3_flag = True
                self.connection.send('0x2E030'.encode())

    # #########################################################################


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
