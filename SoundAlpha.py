from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from PyQt5 import QtWidgets
import sys
from SoundForm import Ui_MainWindow

#pygame.mixer.music.load("alphavillesounds_like_a_melody.mp3")
#pygame.mixer.music.load("Vechnye_Hity-Alphaville_-_Sounds_Like_A_Melody.mp3")


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
        self.ui.comboBox.addItem("MID_alphavillesounds_like_a_melody.mp3")
        self.ui.comboBox.addItem("ORG_Alphaville_Sounds_Like_A_Melody.mp3")
        self.ui.comboBox.setCurrentText("MID_alphavillesounds_like_a_melody.mp3")
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setSingleStep(10)
        self.ui.horizontalSlider.setValue(80)
        self.ui.horizontalSlider.valueChanged.connect(self.SliderChanged)
        self.stoped=True
        pygame.init()



    def btnClicked1(self):
        pygame.mixer.music.load(self.ui.comboBox.currentText())
        pygame.mixer.music.play(-1)
        self.stoped = False
        self.ui.pushButton_2.setEnabled(True)

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



    def btnClicked3(self):
        app.instance().quit()
        pygame.quit()

app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())

