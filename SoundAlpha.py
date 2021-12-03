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
        self.mus_path = os.path.join(os.getcwd(), "mus")
        for file in os.listdir(self.mus_path):
            if file.endswith(".mp3"):
                self.ui.comboBox.addItem(file)
                #print(file)
        if self.ui.comboBox.count() > 0:
            self.ui.pushButton_PlaySelected.setEnabled(True)
            self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
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
        self.playList = []
        self.running = False
        pygame.init()
        pygame.mixer.init()
        # setting up an end event which host an event
        # after the end of every song
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)

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

    def insert_into_playlist(self, music_file):
        # Adding songs file in our playlist
        self.playList.append(music_file)

    def start_playlist(self,playList):

        # Loading first audio file into our player
        pygame.mixer.music.load(playList[0])

        # Removing the loaded song from our playlist list
        playList.pop(0)

        # Playing our music
        pygame.mixer.music.play()

        # Queueing next song into our player
        pygame.mixer.music.queue(playList[0])
        playList.pop(0)

        # setting up an end event which host an event
        # after the end of every song
        #SONG_END = pygame.USEREVENT + 1
        #pygame.mixer.music.set_endevent(SONG_END)

        # Playing the songs in the background
        self.running = True
        while self.running:

            # checking if any event has been
            # hosted at time of playing
            for event in pygame.event.get():

                # A event will be hosted
                # after the end of every song
                if event.type == self.SONG_END:
                    print('Song Finished')

                    # Checking our playList
                    # that if any song exist or
                    # it is empty
                    if len(playList) > 0:
                        # if song available then load it in player
                        # and remove from the player
                        pygame.mixer.music.queue(playList[0])
                        playList.pop(0)

                # Checking whether the
                # player is still playing any song
                # if yes it will return true and false otherwise
                if not pygame.mixer.music.get_busy():
                    print("Playlist completed")

                    # When the playlist has
                    # completed playing successfully
                    # we'll go out of the
                    # while-loop by using break
                    self.running = False
                    break

    def PlaySelected(self):

        self.stoped = False
        self.ui.pushButton_PauseCont.setEnabled(True)
        self.ui.pushButton_PauseCont.setText("пауза")
        self.startTimer()
        self.ui.pushButton_PlaySelected.setEnabled(False)
        self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
        self.songLength = self.song.info.length
        self.ui.comboBox.setEnabled(False)
        pygame.mixer.music.load(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
        pygame.mixer.music.play(loops=0)  # -1
        pygame.mixer.music.unpause()
        self.ui.pushButton_PlayAll.setEnabled(False)

        # Playing the songs in the background
        self.running = True
        while self.running:

            # checking if any event has been
            # hosted at time of playing
            for event in pygame.event.get():

                # A event will be hosted
                # after the end of every song
                if event.type == self.SONG_END:
                    print('Single Song Finished')

                # Checking whether the
                # player is still playing any song
                # if yes it will return true and false otherwise
                if not pygame.mixer.music.get_busy():
                    print("Single Playlist completed")

                    # When the playlist has
                    # completed playing successfully
                    # we'll go out of the
                    # while-loop by using break
                    self.running = False
                    break
        print("Exit Single while loop")
        self.ui.pushButton_PlayAll.setEnabled(True)

    def PlayAll(self):
        for i in range(0,self.ui.comboBox.count()):
            file4play = os.path.join(self.mus_path, self.ui.comboBox.itemText(i))
            print(i, file4play)
            self.insert_into_playlist(file4play)
        self.start_playlist(self.playList)

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
        self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
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

