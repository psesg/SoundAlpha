import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
# next line for UHD display scaling
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

import sys
from SoundForm import Ui_MainWindow

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_1.clicked.connect(self.btnClicked1)
        self.ui.pushButton_2.clicked.connect(self.btnClicked2)
        self.ui.pushButton_3.clicked.connect(self.btnClicked3)
        self.ui.pushButton_2.setEnabled(False)
        for file in os.listdir(os.curdir):
            if file.endswith(".mp3"):
                self.ui.comboBox.addItem(file)
                #print(file)
        if self.ui.comboBox.count() > 0:
            self.ui.pushButton_1.setEnabled(True)
        else:
            self.ui.pushButton_1.setEnabled(False)
        self.ui.comboBox.setCurrentText(file)
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setSingleStep(10)
        self.ui.horizontalSlider.setValue(85)
        self.ui.horizontalSlider.valueChanged.connect(self.SliderChanged)
        self.stoped=True
        self.ui.comboBox.currentTextChanged.connect(self.comboBoxTextChanged)
        pygame.init()

    def btnClicked1(self):
        pygame.mixer.music.load(self.ui.comboBox.currentText())
        pygame.mixer.music.play(-1)
        self.stoped = False
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton_2.setText("Пауза")
        pygame.mixer.music.unpause()
        self.stoped = False
        self.ui.pushButton_1.setEnabled(False)

    def btnClicked2(self):
        if not self.stoped:
            self.ui.pushButton_2.setText("Продолжить")
            pygame.mixer.music.pause()
            self.stoped = True
        else:
            self.ui.pushButton_2.setText("Пауза")
            pygame.mixer.music.unpause()
            self.stoped = False

    def SliderChanged(self,value):
        if not self.stoped:
            pygame.mixer.music.set_volume(value/100)
            #print(value)

    def comboBoxTextChanged(self,choose_str):
        if self.stoped == False:
            pygame.mixer.music.stop()
            self.stoped = True
        self.ui.pushButton_2.setText("Пауза")
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_1.setEnabled(True)
        #print(choose_str)

    def btnClicked3(self):
        app.instance().quit()
        pygame.quit()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())

