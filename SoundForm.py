# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SoundForm.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(243, 342)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pygame.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(241, 342))
        self.centralwidget.setMaximumSize(QtCore.QSize(241, 342))
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_PlaySelected = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_PlaySelected.setGeometry(QtCore.QRect(10, 180, 223, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_PlaySelected.sizePolicy().hasHeightForWidth())
        self.pushButton_PlaySelected.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_PlaySelected.setFont(font)
        self.pushButton_PlaySelected.setObjectName("pushButton_PlaySelected")
        self.pushButton_PauseCont = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_PauseCont.setGeometry(QtCore.QRect(10, 240, 223, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_PauseCont.setFont(font)
        self.pushButton_PauseCont.setObjectName("pushButton_PauseCont")
        self.pushButton_Exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Exit.setGeometry(QtCore.QRect(140, 310, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_Exit.setFont(font)
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 226, 22))
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(10)
        self.comboBox.setFont(font)
        self.comboBox.setCurrentText("")
        self.comboBox.setObjectName("comboBox")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(10, 280, 221, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSliderPos = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSliderPos.setGeometry(QtCore.QRect(10, 150, 221, 22))
        self.horizontalSliderPos.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderPos.setObjectName("horizontalSliderPos")
        self.label_vol = QtWidgets.QLabel(self.centralwidget)
        self.label_vol.setGeometry(QtCore.QRect(10, 270, 223, 20))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(9)
        self.label_vol.setFont(font)
        self.label_vol.setAlignment(QtCore.Qt.AlignCenter)
        self.label_vol.setObjectName("label_vol")
        self.label_pos = QtWidgets.QLabel(self.centralwidget)
        self.label_pos.setGeometry(QtCore.QRect(10, 140, 223, 20))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_pos.setFont(font)
        self.label_pos.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_pos.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pos.setObjectName("label_pos")
        self.pushButton_PlayAll = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_PlayAll.setGeometry(QtCore.QRect(10, 210, 223, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_PlayAll.sizePolicy().hasHeightForWidth())
        self.pushButton_PlayAll.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_PlayAll.setFont(font)
        self.pushButton_PlayAll.setObjectName("pushButton_PlayAll")
        self.pushButton_Stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Stop.setGeometry(QtCore.QRect(10, 310, 90, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.pushButton_Stop.setFont(font)
        self.pushButton_Stop.setObjectName("pushButton_Stop")
        self.label_cursong = QtWidgets.QLabel(self.centralwidget)
        self.label_cursong.setGeometry(QtCore.QRect(16, 120, 211, 20))
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(10)
        self.label_cursong.setFont(font)
        self.label_cursong.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_cursong.setText("")
        self.label_cursong.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cursong.setObjectName("label_cursong")
        self.pushButton_Choose = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Choose.setGeometry(QtCore.QRect(10, 69, 223, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.pushButton_Choose.setFont(font)
        self.pushButton_Choose.setObjectName("pushButton_Choose")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(12, 36, 221, 28))
        font = QtGui.QFont()
        font.setFamily("Arial Narrow")
        font.setPointSize(8)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TestPyQt"))
        self.pushButton_PlaySelected.setText(_translate("MainWindow", "играть выбранную"))
        self.pushButton_PauseCont.setText(_translate("MainWindow", "пауза"))
        self.pushButton_Exit.setText(_translate("MainWindow", "выход"))
        self.label_vol.setText(_translate("MainWindow", "громкость"))
        self.label_pos.setText(_translate("MainWindow", "позиция:"))
        self.pushButton_PlayAll.setText(_translate("MainWindow", "играть все"))
        self.pushButton_Stop.setText(_translate("MainWindow", "стоп"))
        self.pushButton_Choose.setText(_translate("MainWindow", "выбрать каталог"))
