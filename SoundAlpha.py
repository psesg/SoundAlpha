import sys
import os
import platform
import logging
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
from PyQt5.QtCore import Qt, QTimer
from mutagen.mp3 import MP3
from SoundForm import Ui_MainWindow

# next line for UHD display scaling
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

# pyuic5 SoundForm.ui -o SoundForm.py
# for Win:  pyinstaller SoundAlpha.py -F -w --icon pygame.ico --version-file file_version_info.txt

logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)  # DEBUG, CRITICAL

TIMER_MSEC = 200
TIME_SLEEP = 0.075


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # подключение клик-сигнал к слоту btnClicked
        self.ui.pushButton_PlaySelected.clicked.connect(self.play_selected)
        self.ui.pushButton_PlayAll.clicked.connect(self.play_all)
        self.ui.pushButton_PauseCont.clicked.connect(self.pause_continue)
        self.ui.pushButton_Exit.clicked.connect(self.exit_prg)
        self.ui.pushButton_Stop.clicked.connect(self.stop_play)
        self.ui.pushButton_PauseCont.setEnabled(False)
        self.mus_path = os.path.join(os.getcwd(), "mus")
        logging.info("os.getcwd() = '{}', self.mus_path = '{}'".format(os.getcwd(), self.mus_path))
        self.file = ""
        self.file4play = ""
        self.ui.lineEdit.setText(self.mus_path)
        for self.file in os.listdir(self.mus_path):
            if self.file.endswith(".mp3"):
                self.ui.comboBox.addItem(self.file)
                logging.info("self.file = '{}'".format(self.file))
        if self.ui.comboBox.count() > 0:
            self.ui.pushButton_PlaySelected.setEnabled(True)
            self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
            self.songLength = self.song.info.length
            self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))
        else:
            self.ui.pushButton_PlaySelected.setEnabled(False)
            self.ui.pushButton_PlayAll.setEnabled(False)
        self.ui.comboBox.setCurrentText(self.file)
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setSingleStep(10)
        self.ui.horizontalSlider.setValue(100)
        self.ui.horizontalSlider.valueChanged.connect(self.slider_changed)
        self.is_playing = False
        self.ui.comboBox.currentTextChanged.connect(self.combobox_text_changed)
        self.timer = QTimer(self)  # QTimer()
        self.timer.timeout.connect(self.show_timer)
        self.song = None
        self.songLength = 0.0
        self.ui.progressBarCurSong.setMaximum(100)
        self.ui.progressBarCurSong.setMinimum(0)
        self.ui.progressBarCurSong.setEnabled(False)
        self.ui.progressBarCurSong.setValue(0)
        self.ui.progressBarTotalSongs.setMaximum(1)
        self.ui.progressBarTotalSongs.setMinimum(0)
        self.ui.progressBarTotalSongs.setEnabled(False)
        self.ui.progressBarTotalSongs.setValue(0)
        self.running = False
        self.playList = []
        self.running = False
        pygame.init()
        pygame.mixer.init()
        # setting up an end event which host an event
        # after the end of every song
        self.SONG_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.SONG_END)
        self.ui.pushButton_Stop.setEnabled(False)
        # self.ui.lineEdit.setEnabled(False)
        self.ui.pushButton_Choose.clicked.connect(self.btn_choose_dir)
        self.dirname = ""
        self.total_list_duration_sec = 0.0
        self.current_list_duration_sec = 0.0

    def new_timer(self):
        self.timer.start(TIMER_MSEC)

    def del_timer(self):
        self.timer.stop()

    def do_nothing(self):
        logging.info("Nothing")
        time.sleep(TIME_SLEEP)

    def btn_choose_dir(self):
        QApplication.processEvents()
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.DirectoryOnly)
        dlg.setDirectory(self.mus_path)
        dlg.setModal(True)
        if dlg.exec_():
            self.dirname = dlg.selectedFiles()[0]
            self.ui.lineEdit.setText(self.dirname)
            self.mus_path = self.dirname
            plat = platform.system()
            logging.info("platform = '{}', self.mus_path = '{}'".format(plat, self.mus_path))
            if plat == "Linux" or plat == "Darwin":
                pass
            if plat == "Windows":
                self.mus_path = self.mus_path.replace('/', '\\')
            logging.info("platform = '{}', self.mus_path = '{}'".format(plat, self.mus_path))
            self.ui.lineEdit.setText(self.mus_path)
            self.ui.comboBox.currentTextChanged.disconnect()
            if self.ui.comboBox.count() > 0:
                self.ui.comboBox.clear()
                logging.info("executed self.ui.comboBox.clear()")
            self.total_list_duration_sec = 0
            for self.file in os.listdir(self.mus_path):
                if self.file.endswith(".mp3"):
                    self.ui.comboBox.addItem(self.file)
                    logging.info("self.file = '{}'".format(self.file))
            if self.ui.comboBox.count() > 0:
                self.ui.pushButton_PlaySelected.setEnabled(True)
                self.ui.pushButton_PlayAll.setEnabled(True)
                self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
                self.songLength = self.song.info.length
                self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))
            else:
                self.ui.pushButton_PlaySelected.setEnabled(False)
                self.ui.pushButton_PlayAll.setEnabled(False)
            self.ui.comboBox.currentTextChanged.connect(self.combobox_text_changed)

    def show_timer(self):
        QApplication.processEvents()
        if self.is_playing:
            curpos = pygame.mixer.music.get_pos()
            lensong = self.songLength
            if (curpos / 10.0) / lensong >= 98.0:
                pygame.mixer.music.stop()
                self.del_timer()
                self.ui.progressBarCurSong.setValue(0)
                self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, lensong))
                self.ui.comboBox.setEnabled(True)
            else:
                self.ui.progressBarCurSong.setValue(int((curpos / 10.0) / lensong))
                self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format((curpos / 10.0) / lensong, lensong))

    def start_playlist(self):
        QApplication.processEvents()
        # Loading first audio file into our player
        pygame.mixer.music.load(self.playList[0])
        self.song = MP3(self.playList[0])
        self.songLength = self.song.info.length
        self.ui.label_cursong.setText(os.path.basename(self.playList[0]))
        self.ui.progressBarTotalSongs.setMaximum(len(self.playList))
        self.ui.progressBarTotalSongs.setValue(len(self.playList))
        self.total_list_duration_sec = 0.0
        self.current_list_duration_sec = 0.0
        for i in range(len(self.playList)):
            self.song = MP3(self.playList[i])
            self.songLength = self.song.info.length
            self.total_list_duration_sec = self.total_list_duration_sec + self.songLength
        self.current_list_duration_sec = self.total_list_duration_sec
        hours = int(self.total_list_duration_sec // 3060)
        minuts = int((self.total_list_duration_sec % 3060) // 60)
        secunds = int((self.total_list_duration_sec % 3060) % 60)
        self.ui.label_pos_songs.setText("{} [{:02d}:{:02d}:{:02d}] из {} [{:02d}:{:02d}:{:02d}]".format(len(self.playList),hours, minuts, secunds, len(self.playList),
                                                                          hours, minuts, secunds))
        self.new_timer()
        # Removing the loaded song from our playlist list
        self.playList.pop(0)

        # Playing our music
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(self.SONG_END)

        # Playing the songs in the background
        self.running = True
        while self.running:
            QApplication.processEvents()
            # logging.info("while loop list...")
            # checking if any event has been
            # hosted at time of playing
            for event in pygame.event.get():

                # A event will be hosted
                # after the end of every song
                if event.type == self.SONG_END:
                    logging.info("Song from list finished")
                    self.del_timer()

                    # Checking our playList
                    # that if any song exist or
                    # it is empty
                    if len(self.playList) > 0:
                        # if song available then load it in player
                        # and remove from the player
                        pygame.mixer.music.load(self.playList[0])
                        self.song = MP3(self.playList[0])
                        self.songLength = self.song.info.length
                        self.ui.label_cursong.setText(os.path.basename(self.playList[0]))
                        self.ui.progressBarTotalSongs.setValue(len(self.playList))
                        self.current_list_duration_sec = self.total_list_duration_sec - self.songLength
                        rhours = int(self.current_list_duration_sec // 3060)
                        rminuts = int((self.current_list_duration_sec % 3060) // 60)
                        rsecunds = int((self.current_list_duration_sec % 3060) % 60)

                        hours = int(self.total_list_duration_sec // 3060)
                        minuts = int((self.total_list_duration_sec % 3060) // 60)
                        secunds = int((self.total_list_duration_sec % 3060) % 60)
                        self.ui.label_pos_songs.setText(
                            "{} [{:02d}:{:02d}:{:02d}] из {} [{:02d}:{:02d}:{:02d}]".format(len(self.playList), rhours,
                                                                                              rminuts, rsecunds,
                                                                                              self.ui.progressBarTotalSongs.maximum(),
                                                                                              hours, minuts, secunds))
                        pygame.mixer.music.play()
                        self.new_timer()
                        self.playList.pop(0)

                # Checking whether the
                # player is still playing any song
                # if yes it will return true and false otherwise
                if not pygame.mixer.music.get_busy() and self.is_playing:
                    logging.info("Playlist completed")
                    self.ui.pushButton_PlayAll.setEnabled(True)
                    self.ui.pushButton_PlaySelected.setEnabled(True)
                    self.ui.pushButton_Stop.setEnabled(False)
                    self.ui.pushButton_Exit.setEnabled(True)
                    self.ui.pushButton_PauseCont.setEnabled(False)
                    self.ui.label_cursong.setText("")
                    self.is_playing = False
                    self.del_timer()
                    self.ui.pushButton_Choose.setEnabled(True)
                    self.ui.progressBarCurSong.setValue(0)
                    self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
                    self.songLength = self.song.info.length
                    self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))
                    self.ui.progressBarTotalSongs.setMaximum(1)
                    self.ui.progressBarTotalSongs.setValue(0)
                    self.ui.label_pos_songs.setText("песен: {} из {}".format(0, 0))
                    # When the playlist has
                    # completed playing successfully
                    # we'll go out of the
                    # while-loop by using break
                    self.running = False
                    break
        logging.info("Exit list while loop")

    def play_selected(self):
        QApplication.processEvents()
        self.is_playing = True
        self.ui.pushButton_PauseCont.setEnabled(True)
        self.ui.pushButton_PauseCont.setText("пауза")
        self.new_timer()
        self.ui.pushButton_PlaySelected.setEnabled(False)
        self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
        self.songLength = self.song.info.length
        self.ui.comboBox.setEnabled(False)
        self.ui.pushButton_Choose.setEnabled(False)
        pygame.mixer.music.load(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
        self.ui.label_cursong.setText(self.ui.comboBox.currentText())
        pygame.mixer.music.play(loops=0)  # -1
        self.ui.pushButton_PlayAll.setEnabled(False)
        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.pushButton_Exit.setEnabled(False)
        self.ui.progressBarTotalSongs.setMaximum(1)
        self.ui.progressBarTotalSongs.setValue(1)
        self.ui.label_pos_songs.setText("песен: {} из {}".format(1, 1))

        # Playing the songs in the background
        self.running = True
        while self.running:
            self.do_nothing()
            QApplication.processEvents()
            # logging.info("while loop single...")
            # checking if any event has been
            # hosted at time of playing
            for event in pygame.event.get():

                # A event will be hosted
                # after the end of every song
                if event.type == self.SONG_END:
                    logging.info("Single Song finished")

                # Checking whether the
                # player is still playing any song
                # if yes it will return true and false otherwise
                if not pygame.mixer.music.get_busy() and self.is_playing:
                    logging.info("Single Playlist completed")

                    # When the playlist has
                    # completed playing successfully
                    # we'll go out of the
                    # while-loop by using break
                    self.running = False
                    break
        logging.info("Exit Single while loop")

        self.ui.pushButton_PlayAll.setEnabled(True)
        self.ui.pushButton_PlaySelected.setEnabled(True)
        self.ui.pushButton_Stop.setEnabled(False)
        self.ui.pushButton_Exit.setEnabled(True)
        self.ui.pushButton_PauseCont.setEnabled(False)
        self.ui.pushButton_Choose.setEnabled(True)
        self.ui.label_cursong.setText("")
        self.is_playing = False
        self.del_timer()
        self.ui.progressBarCurSong.setValue(0)
        self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))
        self.ui.progressBarTotalSongs.setValue(0)
        self.ui.label_pos_songs.setText("песен: {} из {}".format(0, 0))

    def play_all(self):
        QApplication.processEvents()
        for i in range(0, self.ui.comboBox.count()):
            self.file4play = os.path.join(self.mus_path, self.ui.comboBox.itemText(i))
            logging.info("i = {},  self.file4play = '{}'".format(i, self.file4play))
            self.playList.append(self.file4play)
        self.ui.pushButton_Stop.setEnabled(True)
        self.ui.pushButton_PlaySelected.setEnabled(False)
        self.ui.pushButton_PlayAll.setEnabled(False)
        self.ui.pushButton_Exit.setEnabled(False)
        self.ui.comboBox.setEnabled(False)
        self.ui.pushButton_PauseCont.setEnabled(True)
        self.is_playing = True
        self.ui.pushButton_Choose.setEnabled(False)
        self.start_playlist()

    def pause_continue(self):
        QApplication.processEvents()
        if self.timer.isActive():
            logging.info("before self.timer.isActive() = True")
        else:
            logging.info("before self.timer.isActive() = False")
        ########################################################
        if self.is_playing:
            self.is_playing = False
            self.ui.pushButton_PauseCont.setText("продолжить")
            self.ui.pushButton_Stop.setEnabled(False)
            self.del_timer()
            pygame.mixer.music.pause()
        else:
            self.is_playing = True
            self.ui.pushButton_PauseCont.setText("пауза")
            self.ui.pushButton_Stop.setEnabled(True)
            self.new_timer()
            pygame.mixer.music.unpause()
        #######################################################
        if self.timer.isActive():
            logging.info("after self.timer.isActive() = True")
        else:
            logging.info("after self.timer.isActive() = False")

    def slider_changed(self, value):
        QApplication.processEvents()
        if self.is_playing:
            pygame.mixer.music.set_volume(value / 100)
            logging.info("value = {}".format(value))

    def combobox_text_changed(self, choose_str):
        QApplication.processEvents()
        logging.info("choose_str = {}".format(choose_str))
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
        self.ui.pushButton_PauseCont.setText("пауза")
        self.ui.pushButton_PauseCont.setEnabled(False)
        self.ui.pushButton_PlaySelected.setEnabled(True)
        self.ui.progressBarCurSong.setValue(0)
        self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
        self.songLength = self.song.info.length
        self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))

    def stop_play(self):
        QApplication.processEvents()
        self.ui.comboBox.setEnabled(True)
        self.ui.pushButton_PlaySelected.setEnabled(True)
        self.ui.pushButton_PlayAll.setEnabled(True)
        self.ui.pushButton_PauseCont.setEnabled(False)
        self.ui.pushButton_Exit.setEnabled(True)
        self.ui.progressBarCurSong.setValue(0)
        self.song = MP3(os.path.join(self.mus_path, self.ui.comboBox.currentText()))
        self.songLength = self.song.info.length
        self.ui.label_pos.setText("позиция: {:.2f}% из {:.2f} сек".format(0.0, self.songLength))
        if len(self.playList) > 0:
            self.playList.clear()
        pygame.mixer.music.stop()

    @staticmethod
    def exit_prg():
        QApplication.processEvents()
        app.instance().quit()
        pygame.quit()


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())
