import time

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap

flag_sweep_thread = False
flag_locked = True
warning_lights_flag = False
right_signal_flag = False
left_signal_flag = False
left_save_flag = False
right_save_flag = False


# ############################## EXERCISE 2 ################################
class MyThreadSweep(QThread):
    sweep_leds_signal = pyqtSignal(int)

    def run(self):
        global flag_sweep_thread
        count = 0

        while flag_sweep_thread:
            self.sweep_leds_signal.emit(count)
            count += 1
            time.sleep(1)
            if count == 4:
                self.sweep_leds_signal.emit(-1)
                flag_sweep_thread = False


# ############################## EXERCISE 6 #################################
class MyThreadWarning(QThread):
    warning_lights_signal = pyqtSignal(int)

    def run(self):
        global warning_lights_flag
        index = 0
        while warning_lights_flag:
            self.warning_lights_signal.emit(index)
            index += 1
            index %= 2
            time.sleep(0.3)
        self.warning_lights_signal.emit(1)


# ############################## EXERCISE 7 #################################
class MyThreadLeft(QThread):
    leftLightsSignal = pyqtSignal(int)

    def run(self):
        global left_signal_flag
        index = 0
        while left_signal_flag:
            self.leftLightsSignal.emit(index)
            index += 1
            index %= 2
            time.sleep(0.3)
        self.leftLightsSignal.emit(1)


# ############################## EXERCISE 8 #################################
class MyThreadRight(QThread):
    rightLightsSignal = pyqtSignal(int)

    def run(self):
        global right_signal_flag
        index = 0
        while right_signal_flag:
            self.rightLightsSignal.emit(index)
            index += 1
            index %= 2
            time.sleep(0.3)
        self.rightLightsSignal.emit(1)


# ############################## EXERCISE 10 ################################
class MyThreadUnlockCar(QThread):
    unlockCarSignal = pyqtSignal(int)

    def run(self):
        for i in range(4):
            self.unlockCarSignal.emit(i)
            time.sleep(0.3)


# ############################## EXERCISE 11 ################################
class MyThreadLockCar(QThread):
    lockCarSignal = pyqtSignal(int)

    def run(self):
        for i in range(3):
            self.lockCarSignal.emit(i)
            time.sleep(0.3)


class UIMainWindow(object):

    def setup_ui(self, my_main_window):
        my_main_window.setObjectName("MainWindow")
        my_main_window.setFixedSize(900, 500)
        my_main_window.setWindowTitle("Laboratory 1 - Interior Lights")
        self.central_widget = QtWidgets.QWidget(my_main_window)
        self.central_widget.setObjectName("centralwidget")

        my_main_window.setCentralWidget(self.central_widget)

        # Set background application color
        self.central_widget.setStyleSheet("background-color: white;")

        # Continental image
        self.label = QtWidgets.QLabel(self.central_widget)
        self.label.setGeometry(QtCore.QRect(5, 350, 350, 120))
        pixmap = QPixmap("conti.png")
        pixmap = pixmap.scaled(350, 120, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)

        # Car image
        self.label_1 = QtWidgets.QLabel(self.central_widget)
        self.label_1.setGeometry(QtCore.QRect(300, 170, 331, 161))
        pixmap1 = QPixmap("car.jpg")
        pixmap1 = pixmap1.scaled(331, 161, QtCore.Qt.KeepAspectRatio)
        self.label_1.setPixmap(pixmap1)

        # Left door button
        self.left_door = QtWidgets.QPushButton(my_main_window)
        self.left_door.setText("Left Door")
        self.left_door.setStyleSheet("font: bold;")
        self.left_door.setGeometry(QtCore.QRect(380, 50, 211, 41))
        self.left_door.clicked.connect(self.open_door_left)

        # Left door slider
        self.left_door_slider = QtWidgets.QSlider(self.central_widget)
        self.left_door_slider.setGeometry(QtCore.QRect(410, 100, 160, 26))
        self.left_door_slider.setOrientation(QtCore.Qt.Horizontal)
        self.left_door_slider.setRange(0, 100)
        self.left_door_slider.setValue(0)
        self.left_door_slider.valueChanged.connect(self.value_change_left_slider)

        # Left door spinbox
        self.spinBox_left = QtWidgets.QSpinBox(my_main_window)
        self.spinBox_left.setGeometry(QtCore.QRect(300, 50, 75, 41))
        self.spinBox_left.setKeyboardTracking(False)
        self.spinBox_left.setRange(0, 100)
        self.spinBox_left.valueChanged.connect(self.value_change)

        # Right door
        self.right_door = QtWidgets.QPushButton(my_main_window)
        self.right_door.setText("Right door")
        self.right_door.setStyleSheet("font: bold;")
        self.right_door.setGeometry(QtCore.QRect(380, 400, 211, 41))
        self.right_door.clicked.connect(self.open_door_right)

        # Right door slider
        self.right_door_slider = QtWidgets.QSlider(self.central_widget)
        self.right_door_slider.setGeometry(QtCore.QRect(410, 360, 160, 26))
        self.right_door_slider.setOrientation(QtCore.Qt.Horizontal)
        self.right_door_slider.setRange(0, 100)
        self.right_door_slider.setValue(0)
        self.right_door_slider.valueChanged.connect(self.value_change_right_slider)

        # Right door spinbox
        self.spinBox_right = QtWidgets.QSpinBox(my_main_window)
        self.spinBox_right.setGeometry(QtCore.QRect(300, 400, 75, 41))
        self.spinBox_right.setKeyboardTracking(False)
        self.spinBox_right.setRange(0, 100)
        self.spinBox_right.valueChanged.connect(self.value_change)

        self.kl_list = ['no_KL', 'KL_s', 'KL_15', 'KL_50', 'KL_75']
        # Current kl label
        self.current_kl_label = QtWidgets.QLabel(self.central_widget)
        self.current_kl_label.setGeometry(QtCore.QRect(685, 80, 151, 31))
        self.current_kl_label.setStyleSheet("font: bold;")
        self.current_kl_label.setText("Current KL: no_KL")

        # Previous kl button
        self.prev_kl = QtWidgets.QPushButton(my_main_window)
        self.prev_kl.setText("Previous KL")
        self.prev_kl.setStyleSheet("font: bold;")
        self.prev_kl.setGeometry(QtCore.QRect(680, 40, 101, 31))
        self.prev_kl.clicked.connect(self.prev_kl_function)
        self.prev_kl.setEnabled(False)

        # Prev kl label
        self.prev_kl_label = QtWidgets.QLabel(self.central_widget)
        self.prev_kl_label.setGeometry(QtCore.QRect(790, 40, 92, 31))
        self.prev_kl_label.setStyleSheet("font: bold;")

        # Next kl button
        self.next_kl = QtWidgets.QPushButton(my_main_window)
        self.next_kl.setText("Next KL")
        self.next_kl.setStyleSheet("font: bold;")
        self.next_kl.setGeometry(QtCore.QRect(680, 120, 101, 31))
        self.next_kl.clicked.connect(self.next_kl_function)

        # Next kl label
        self.next_kl_label = QtWidgets.QLabel(self.central_widget)
        self.next_kl_label.setGeometry(QtCore.QRect(790, 120, 81, 31))
        self.next_kl_label.setStyleSheet("font: bold;")
        self.next_kl_label.setText("KL_s")

        # green led for interior lights
        self.interiorLightsLabel = QtWidgets.QLabel(self.central_widget)
        self.interiorLightsLabel.setGeometry(QtCore.QRect(220, 160, 20, 20))

        # inside carLight Button
        self.carLight1 = QtWidgets.QPushButton(my_main_window)
        self.carLight1.setText("Car Light")
        self.carLight1.setStyleSheet("font: bold;")
        self.carLight1.setGeometry(QtCore.QRect(680, 280, 120, 30))
        self.carLight1.clicked.connect(self.car_light_set)

        # inside carLight
        self.carLight = QtWidgets.QLabel(self.central_widget)
        self.carLight.setGeometry(QtCore.QRect(450, 240, 20, 20))

        # warning Lights Button
        self.warning = QtWidgets.QPushButton(my_main_window)
        self.warning.setText("Warning Lights")
        self.warning.setStyleSheet("font: bold;")
        self.warning.setGeometry(QtCore.QRect(50, 100, 160, 41))
        self.warning.clicked.connect(self.warning_lights_button)

        # left signaling Button
        self.warningLeft = QtWidgets.QPushButton(my_main_window)
        self.warningLeft.setText("Left Signaling")
        self.warningLeft.setStyleSheet("font:bold;")
        self.warningLeft.setGeometry(QtCore.QRect(680, 370, 120, 30))
        self.warningLeft.clicked.connect(self.left_signaling)

        # right signaling Button
        self.warningRight = QtWidgets.QPushButton(my_main_window)
        self.warningRight.setText("Right Signaling")
        self.warningRight.setStyleSheet("font:bold;")
        self.warningRight.setGeometry(QtCore.QRect(680, 400, 120, 30))
        self.warningRight.clicked.connect(self.right_signaling)

        # Warning Lights
        self.warningLightLeftRear = QtWidgets.QLabel(self.central_widget)
        self.warningLightLeftRear.setGeometry(QtCore.QRect(260, 190, 20, 20))

        self.warningLightRightRear = QtWidgets.QLabel(self.central_widget)
        self.warningLightRightRear.setGeometry(QtCore.QRect(260, 293, 20, 20))

        self.warningLightLeftFront = QtWidgets.QLabel(self.central_widget)
        self.warningLightLeftFront.setGeometry(QtCore.QRect(650, 190, 20, 20))

        self.warningLightRightFront = QtWidgets.QLabel(self.central_widget)
        self.warningLightRightFront.setGeometry(QtCore.QRect(650, 293, 20, 20))

        # Lock Car
        self.lockCar1 = QtWidgets.QPushButton(my_main_window)
        self.lockCar1.setText("Lock car")
        self.lockCar1.setStyleSheet("font: bold;")
        self.lockCar1.setGeometry(QtCore.QRect(680, 340, 120, 30))
        self.lockCar1.clicked.connect(self.lock_car)

        # Unlock Car
        self.unlockCar1 = QtWidgets.QPushButton(my_main_window)
        self.unlockCar1.setText("Unlock car")
        self.unlockCar1.setStyleSheet("font: bold;")
        self.unlockCar1.setGeometry(QtCore.QRect(680, 310, 120, 30))
        self.unlockCar1.clicked.connect(self.unlock_car)

        # 4 leds for sweep
        self.led1_sweep = QtWidgets.QLabel(self.central_widget)
        self.led1_sweep.setGeometry(QtCore.QRect(220, 210, 20, 20))

        self.led2_sweep = QtWidgets.QLabel(self.central_widget)
        self.led2_sweep.setGeometry(QtCore.QRect(240, 210, 20, 20))

        self.led3_sweep = QtWidgets.QLabel(self.central_widget)
        self.led3_sweep.setGeometry(QtCore.QRect(260, 210, 20, 20))

        self.led4_sweep = QtWidgets.QLabel(self.central_widget)
        self.led4_sweep.setGeometry(QtCore.QRect(280, 210, 20, 20))

        # KL_s led
        self.KL_S = QtWidgets.QLabel(self.central_widget)
        self.KL_S.setGeometry(QtCore.QRect(750, 165, 20, 20))
        # KL_s label
        self.KL_S_label = QtWidgets.QLabel(self.central_widget)
        self.KL_S_label.setGeometry(QtCore.QRect(700, 165, 40, 20))
        self.KL_S_label.setStyleSheet("font: bold;")
        self.KL_S_label.setText("KL_s")

        # KL_15 led
        self.KL_15 = QtWidgets.QLabel(self.central_widget)
        self.KL_15.setGeometry(QtCore.QRect(750, 190, 20, 20))
        # KL_15 label
        self.KL_15_label = QtWidgets.QLabel(self.central_widget)
        self.KL_15_label.setGeometry(QtCore.QRect(700, 190, 40, 20))
        self.KL_15_label.setStyleSheet("font: bold;")
        self.KL_15_label.setText("KL_15")

        # KL_50 led
        self.KL_50 = QtWidgets.QLabel(self.central_widget)
        self.KL_50.setGeometry(QtCore.QRect(750, 215, 20, 20))
        # KL_50 label
        self.KL_50_label = QtWidgets.QLabel(self.central_widget)
        self.KL_50_label.setGeometry(QtCore.QRect(700, 215, 40, 20))
        self.KL_50_label.setStyleSheet("font: bold;")
        self.KL_50_label.setText("KL_50")

        # KL_75 led
        self.KL_75 = QtWidgets.QLabel(self.central_widget)
        self.KL_75.setGeometry(QtCore.QRect(750, 240, 20, 20))
        # KL_75 label
        self.KL_75_label = QtWidgets.QLabel(self.central_widget)
        self.KL_75_label.setGeometry(QtCore.QRect(700, 240, 40, 20))
        self.KL_75_label.setStyleSheet("font: bold;")
        self.KL_75_label.setText("KL_75")

        # Close all leds button
        self.close_all = QtWidgets.QPushButton(my_main_window)
        self.close_all.setText("Close all leds")
        self.close_all.setStyleSheet("font: bold;color: red")
        self.close_all.setGeometry(QtCore.QRect(50, 50, 120, 35))
        self.close_all.clicked.connect(self.close_all_leds)

        # 1 Led inside
        self.interior_lights = QtWidgets.QPushButton(my_main_window)
        self.interior_lights.setText("Interior lights")
        self.interior_lights.setStyleSheet("font: bold;")
        self.interior_lights.setGeometry(QtCore.QRect(50, 150, 160, 41))
        self.interior_lights.clicked.connect(self.set_interior_lights)

        # Led brightness percentage label
        self.percentage_label = QtWidgets.QLabel(self.central_widget)
        self.percentage_label.setGeometry(QtCore.QRect(50, 260, 90, 40))
        self.percentage_label.setStyleSheet("font: bold;")
        self.percentage_label.setText("Percentage")

        # Led brightness progress bar 
        self.progress_bar = QtWidgets.QProgressBar(my_main_window)
        self.progress_bar.setGeometry(50, 310, 200, 21)
        self.progress_bar.setRange(0, 100)

        # Led brightness spinbox
        self.spinBox = QtWidgets.QSpinBox(my_main_window)
        self.spinBox.setGeometry(QtCore.QRect(150, 260, 75, 41))
        self.spinBox.setKeyboardTracking(False)
        self.spinBox.setRange(0, 100)
        self.spinBox.valueChanged.connect(self.value_change)

        # Sweep button
        self.sweep = QtWidgets.QPushButton(my_main_window)
        self.sweep.setText("Sweep")
        self.sweep.setStyleSheet("font: bold;")
        self.sweep.setGeometry(QtCore.QRect(50, 200, 160, 41))
        self.sweep.clicked.connect(self.sweep_threads)

        self.status_bar = QtWidgets.QStatusBar(my_main_window)
        self.status_bar.setObjectName("statusbar")

        my_main_window.setStatusBar(self.status_bar)
        QtCore.QMetaObject.connectSlotsByName(my_main_window)
        my_main_window.show()

    # ############################## EXERCISE 1 ###############################
    # Clear all leds and widgtets when the Close all leds is pressed
    def close_all_leds(self):
        global flag_sweep_thread, warning_lights_flag, left_signal_flag, right_signal_flag
        self.interior_light_led('#FFFFFF')
        self.set4leds('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF')
        self.set_car_light('#FFFFFF')
        self.progress_bar.setValue(0)
        self.left_door_slider.setValue(0)
        self.right_door_slider.setValue(0)
        flag_sweep_thread = False
        warning_lights_flag = False
        left_signal_flag = False
        right_signal_flag = False
        self.set_bg_colors('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF')
        self.prev_kl.setDisabled(True)
        self.prev_kl_label.setText('')
        self.current_kl_label.setText('Current KL: no_KL')
        self.next_kl_label.setText('KL_s')

    # Open one led when interior lights is pressed  
    def interior_light_led(self, b1):
        self.interiorLightsLabel.setStyleSheet("background-color:" + str(b1) + ";border-radius:5px;")

    # Function called from button handler
    def set_interior_lights(self):
        if '#FFF155' in self.interiorLightsLabel.styleSheet():
            self.interior_light_led('#FFFFFF')
        else:
            self.interior_light_led('#FFF155')

    # ############################## EXERCISE 2 ###############################
    # Sweep Leds thread
    def sweep_threads(self):
        global flag_sweep_thread
        flag_sweep_thread = not flag_sweep_thread
        if flag_sweep_thread:
            print("START SWEEP THREAD!")
        else:
            print("STOP SWEEP THREAD!")
        self.thread = MyThreadSweep()
        self.thread.sweep_leds_signal.connect(self.sweep_leds)
        self.thread.start()

    # Sweep Leds function
    def sweep_leds(self, val):
        colors = ['#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF']
        global flag_sweep_thread
        if flag_sweep_thread:
            colors[val] = '#FFF150'
        self.set4leds(colors[0], colors[1], colors[2], colors[3])

    # Sweep Leds
    def set4leds(self, led1, led2, led3, led4):
        self.led1_sweep.setStyleSheet("background-color:" + str(led1) + ";border-radius:5px;")
        self.led2_sweep.setStyleSheet("background-color:" + str(led2) + ";border-radius:5px;")
        self.led3_sweep.setStyleSheet("background-color:" + str(led3) + ";border-radius:5px;")
        self.led4_sweep.setStyleSheet("background-color:" + str(led4) + ";border-radius:5px;")

    # ############################## EXERCISE 3 ###############################
    # Change progress bar value when spinbox value is changed
    def value_change(self):
        if self.progress_bar.value() < self.spinBox.value():
            self.change_pb_down_value(self.spinBox.value())
        else:
            self.change_pb_up_value(self.spinBox.value())

    # Change led brightness down when the spinbox value
    # (representing led brightness percentage) is less than progress bar value
    def change_pb_down_value(self, value):
        start_value = self.progress_bar.value()
        for i in range(start_value, value):
            self.progress_bar.setValue(i + 1)

    # Change led brightness up when the spinbox value
    # (representing led brightness percentage) is bigger than progress bar value
    def change_pb_up_value(self, value):
        start_value = self.progress_bar.value()
        for i in range(start_value, value, -1):
            self.progress_bar.setValue(i - 1)

    # ############################## EXERCISE 4 ###############################
    # Successive KL led turn
    def kl_lights(self, kl):
        if kl == 1:
            self.set_bg_colors('#868686', '#FFFFFF', '#FFFFFF', '#FFFFFF')
        elif kl == 2:
            self.set_bg_colors('#868686', '#23EC15', '#FFFFFF', '#FFFFFF')
        elif kl == 3:
            self.set_bg_colors('#868686', '#23EC15', '#D80E0E', '#FFFFFF')
        elif kl == 4:
            self.set_bg_colors('#868686', '#23EC15', '#D80E0E', '#0E0ED8')
        else:
            self.set_bg_colors('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF')

    # Set previous value for KL when previous KL button is pressed
    def prev_kl_function(self):
        self.next_kl_label.setText(self.current_kl_label.text()[12:])
        self.current_kl_label.setText("Current KL: " + self.prev_kl_label.text())
        if self.current_kl_label.text()[12:] != 'no_KL':
            for i, kl in enumerate(self.kl_list):
                if kl == self.current_kl_label.text()[12:]:
                    self.prev_kl_label.setText(self.kl_list[i - 1])
        else:
            self.prev_kl_label.setText('')
        self.set_enable()

    # Set next value for KL when next KL button is pressed
    def next_kl_function(self):
        self.prev_kl_label.setText(str(self.current_kl_label.text()[12:]))
        self.current_kl_label.setText("Current KL: " + self.next_kl_label.text())
        if self.current_kl_label.text()[12:] != 'KL_75':
            for i, kl in enumerate(self.kl_list):
                if kl == self.current_kl_label.text()[12:]:
                    self.next_kl_label.setText(self.kl_list[i + 1])
        else:
            self.next_kl_label.setText('')
        self.set_enable()

    # Set enable KL buttons
    def set_enable(self):
        print('Prev ' + self.prev_kl_label.text())
        print('Curr ' + self.current_kl_label.text())
        print('Next ' + self.next_kl_label.text())
        if self.current_kl_label.text()[12:] == 'no_KL':
            self.prev_kl.setEnabled(False)
        elif not self.prev_kl.isEnabled():
            self.prev_kl.setEnabled(True)
        if self.current_kl_label.text()[12:] == 'KL_75':
            self.next_kl.setEnabled(False)
        elif not self.next_kl.isEnabled():
            self.next_kl.setEnabled(True)
        self.kl_lights(self.kl_list.index(self.current_kl_label.text()[12:]))

    # Set KL leds colors
    def set_bg_colors(self, l1, l2, l3, l4):
        self.KL_S.setStyleSheet("background-color:" + str(l1) + ";border-radius:5px;")
        self.KL_15.setStyleSheet("background-color:" + str(l2) + ";border-radius:5px;")
        self.KL_50.setStyleSheet("background-color:" + str(l3) + ";border-radius:5px;")
        self.KL_75.setStyleSheet("background-color:" + str(l4) + ";border-radius:5px;")

    # ############################## EXERCISE 5 ##############################
    # ############################### BONUS ################################
    # Open left door until the obstacle is detected
    def open_door_left(self):
        if self.spinBox_left.value() == 0:
            self.left_door_slider.setValue(100)
        else:
            self.left_door_slider.setValue(self.spinBox_left.value())

    # This function will stop the slider to go to values bigger than the obstacle
    def value_change_left_slider(self):
        if self.spinBox_left.value() != 0:
            if self.left_door_slider.value() > self.spinBox_left.value():
                self.left_door_slider.setValue(self.spinBox_left.value())

    # Open right door until the obstacle is detected      
    def open_door_right(self):
        if self.spinBox_right.value() == 0:
            self.right_door_slider.setValue(100)
        else:
            self.right_door_slider.setValue(self.spinBox_right.value())

    # This function will stop the slider to go to values bigger than the obstacle
    def value_change_right_slider(self):
        if self.spinBox_right.value() != 0:
            if self.right_door_slider.value() > self.spinBox_right.value():
                self.right_door_slider.setValue(self.spinBox_right.value())

    # ########################################################################
    # ############################## USED FUNCTION ###########################
    def set_warning_lights(self, warning_light_left_rear, warning_light_right_rear, warning_light_left_front,
                           warning_light_right_front):
        self.warningLightLeftRear.setStyleSheet(
            "background-color:" + str(warning_light_left_rear) + ";border-radius:5px;")
        self.warningLightRightRear.setStyleSheet(
            "background-color:" + str(warning_light_right_rear) + ";border-radius:5px;")
        self.warningLightLeftFront.setStyleSheet(
            "background-color:" + str(warning_light_left_front) + ";border-radius:5px;")
        self.warningLightRightFront.setStyleSheet(
            "background-color:" + str(warning_light_right_front) + ";border-radius:5px;")

    # ########################################################################

    # ############################## EXERCISE 6 ##############################
    # Warning lights thread
    def warning_lights_button(self):
        """ complete with necessary code """
        global warning_lights_flag, left_signal_flag, right_signal_flag, left_save_flag, right_save_flag
        warning_lights_flag = not warning_lights_flag

        if warning_lights_flag:
            print("START WARNING LIGHTS THREAD!")
            left_save_flag = left_signal_flag
            right_save_flag = right_signal_flag
            left_signal_flag = False
            right_signal_flag = False
        else:
            if left_save_flag:
                self.left_signaling()
            elif right_save_flag:
                self.right_signaling()
            print("STOP WARNING LIGHTS THREAD!")
        self.thread_warning = MyThreadWarning()
        self.thread_warning.warning_lights_signal.connect(self.warning_lights)
        self.thread_warning.start()

    # Warning Lights function
    def warning_lights(self, val):
        values = ['#FFA500', '#FFFFFF']
        self.set_warning_lights(values[val], values[val], values[val], values[val])

    # ############################## EXERCISE 7 ##############################
    # Left Signaling Lights
    def left_signaling(self):
        global left_signal_flag, right_signal_flag, warning_lights_flag, left_save_flag
        left_signal_flag = not left_signal_flag

        if left_signal_flag:
            print("START LEFT SIGNAL LIGHTS THREAD!")
            right_signal_flag = False
            left_save_flag = warning_lights_flag
            warning_lights_flag = False
        else:
            print("STOP LEFT SIGNAL LIGHTS THREAD")
            if left_save_flag:
                self.warning_lights_button()
        self.thread_left = MyThreadLeft()
        self.thread_left.leftLightsSignal.connect(self.while_left)
        self.thread_left.start()

    def while_left(self, val):
        values = ['#FFA500', '#FFFFFF']
        self.set_warning_lights(values[val], values[1], values[val], values[1])

    # ############################## EXERCISE 8 ##############################
    # Right Signaling Lights
    def right_signaling(self):
        global right_signal_flag, left_signal_flag, warning_lights_flag, right_save_flag
        right_signal_flag = not right_signal_flag

        if right_signal_flag:
            print("START RIGHT SIGNAL LIGHTS THREAD!")
            left_signal_flag = False
            right_save_flag = warning_lights_flag
            warning_lights_flag = False
        else:
            print("STOP RIGHT SIGNAL LIGHTS THREAD!")
            if right_save_flag:
                self.warning_lights_button()

        self.thread_right = MyThreadRight()
        self.thread_right.rightLightsSignal.connect(self.while_right)
        self.thread_right.start()

    def while_right(self, val):
        values = ['#FFA500', '#FFFFFF']
        self.set_warning_lights(values[1], values[val], values[1], values[val])

    # ######################## Car Light - usefull for next ex ################
    def set_car_light(self, color):
        self.carLight.setStyleSheet("background-color:" + str(color) + ";border-radius:5px;")

    # Open and close the interior light
    def car_light_set(self):
        if '#FFF155' in self.carLight.styleSheet():
            self.set_car_light('#FFFFFF')
        else:
            self.set_car_light('#FFF155')

    # ############################## EXERCISE 9 ##############################
    # Unlock car
    def unlock_car(self):
        global flag_locked
        if flag_locked:
            self.thread_unlockCar = MyThreadUnlockCar()
            self.thread_unlockCar.unlockCarSignal.connect(self.unlock_car_thread)
            self.thread_unlockCar.start()

    def unlock_car_thread(self, val):
        global flag_locked
        if val == 0:
            self.set_car_light('#FFF155')
            self.set_warning_lights('#FFA500', '#FFA500', '#FFA500', '#FFA500')
        elif val == 1:
            self.set_warning_lights('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF')
        elif val == 2:
            self.set_warning_lights('#FFA500', '#FFA500', '#FFA500', '#FFA500')
        elif val == 3:
            self.set_warning_lights('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF')
            self.set_car_light('#FFFFFF')
            flag_locked = False

    # ############################## EXERCISE 10 ##############################
    # Lock the car
    def lock_car(self):
        self.thread_lockCar = MyThreadLockCar()
        self.thread_lockCar.lockCarSignal.connect(self.lock_car_thread)
        self.thread_lockCar.start()

    def lock_car_thread(self, val):
        global flag_locked
        if val == 0:
            self.set_warning_lights('#FFA500', '#FFA500', '#FFA500', '#FFA500')
        elif val == 1:
            self.set_warning_lights('#FFFFFF', '#FFFFFF', '#FFFFFF', '#FFFFFF')
        elif val == 2:
            self.set_car_light('#FFFFFF')
            flag_locked = True


class MyWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(self,
                                                "Confirm Exit",
                                                "Are you sure you want to exit ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if result == QtWidgets.QMessageBox.Yes:
            event.accept()

        elif result == QtWidgets.QMessageBox.No:
            event.ignore()

    def center(self):
        frame_gm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        center_point = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = MyWindow()
    ui = UIMainWindow()
    ui.setup_ui(main_window)

    main_window.center()
    sys.exit(app.exec_())
