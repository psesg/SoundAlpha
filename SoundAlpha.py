import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt,QTimer
from mutagen.mp3 import MP3
# next line for UHD display scaling
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

# pyuic5 SoundForm.ui -o SoundForm.py

import sys
from SoundForm import Ui_MainWindow

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_PlaySelected.clicked.connect(self.PlaySelected)
        self.ui.pushButton_PlayAll.clicked.connect(self.PlayAll)
        self.ui.pushButton_PauseCont.clicked.connect(self.PauseCont)
        self.ui.pushButton_Exit.clicked.connect(self.ExitPrg)
        self.ui.pushButton_PauseCont.setEnabled(False)
        for file in os.listdir(os.curdir):
            if file.endswith(".mp3"):
                self.ui.comboBox.addItem(file)
                #print(file)
        if self.ui.comboBox.count() > 0:
            self.ui.pushButton_PlaySelected.setEnabled(True)
            self.song = MP3(self.ui.comboBox.currentText())
            self.songLength = self.song.info.length
            self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))
        else:
            self.ui.pushButton_PlaySelected.setEnabled(False)
        self.ui.comboBox.setCurrentText(file)
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setSingleStep(10)
        self.ui.horizontalSlider.setValue(85)
        self.ui.horizontalSlider.valueChanged.connect(self.SliderChanged)
        self.stoped=True
        self.ui.comboBox.currentTextChanged.connect(self.comboBoxTextChanged)
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTimer)
        self.song = None
        self.songLength = 0.0
        self.ui.horizontalSliderPos.setMaximum(100)
        self.ui.horizontalSliderPos.setMinimum(0)
        self.ui.horizontalSliderPos.setSingleStep(1)
        self.ui.horizontalSliderPos.setEnabled(False)
        self.running = False
        pygame.init()
        pygame.mixer.init()

    def showTimer(self):
        if self.stoped == False:
            #print (pygame.mixer.music.get_pos())
            #print("songLength = {}".format(self.song.info.length))
            curpos = pygame.mixer.music.get_pos()
            lensong = self.songLength
            if (curpos/10.0)/lensong >= 98.0:
                pygame.mixer.music.stop()
                #pygame.mixer.music.set_pos(0.0)
                self.stopTimer()
                self.ui.pushButton_PlaySelected.setEnabled(True)
                self.ui.horizontalSliderPos.setValue(0)
                self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, lensong))
                self.ui.comboBox.setEnabled(True)
            else:
                #print("song percent = {:.2f}".format((curpos/10.0)/lensong))
                self.ui.horizontalSliderPos.setValue(int((curpos/10.0)/lensong))
                self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format((curpos/10.0)/lensong, lensong))

    def startTimer(self):
        self.timer.start(200)

    def stopTimer(self):
        self.timer.stop()

    def PlaySelected(self):
        pygame.mixer.music.load(self.ui.comboBox.currentText())
        pygame.mixer.music.play(loops=0) # -1
        self.stoped = False
        self.ui.pushButton_PauseCont.setEnabled(True)
        self.ui.pushButton_PauseCont.setText("пауза")
        pygame.mixer.music.unpause()
        self.startTimer()
        self.ui.pushButton_PlaySelected.setEnabled(False)
        self.song = MP3(self.ui.comboBox.currentText())
        self.songLength = self.song.info.length
        self.ui.comboBox.setEnabled(False)

    def PlayAll(self):
        playArray = []
        for i in range(0, self.ui.comboBox.count()):
            self.ui.comboBox.setCurrentIndex(i)
            playArray.append(self.ui.comboBox.currentText())
            print(i, self.ui.comboBox.currentText())
            if i == 0:
                pygame.mixer.music.load(self.ui.comboBox.currentText())
            else:
                pygame.mixer.music.queue(self.ui.comboBox.currentText())
        #playArray.reverse()
        pygame.mixer.music.play()

    def PauseCont(self):
        if not self.stoped:
            self.ui.pushButton_PauseCont.setText("продолжить")
            pygame.mixer.music.pause()
            self.stoped = True
            self.ui.comboBox.setEnabled(True)
            self.stopTimer()
        else:
            self.ui.pushButton_PauseCont.setText("пауза")
            pygame.mixer.music.unpause()
            self.stoped = False
            self.ui.comboBox.setEnabled(False)
            self.startTimer()

    def SliderChanged(self,value):
        if not self.stoped:
            pygame.mixer.music.set_volume(value/100)
            #print(value)

    def comboBoxTextChanged(self,choose_str):
        if self.stoped == False:
            pygame.mixer.music.stop()
            self.stoped = True
        self.ui.pushButton_PauseCont.setText("Пауза")
        self.ui.pushButton_PauseCont.setEnabled(False)
        self.ui.pushButton_PlaySelected.setEnabled(True)
        self.ui.horizontalSliderPos.setValue(0)
        self.song = MP3(self.ui.comboBox.currentText())
        self.songLength = self.song.info.length
        self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))
        #print(choose_str)

    def ExitPrg(self):
        app.instance().quit()
        pygame.quit()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())

