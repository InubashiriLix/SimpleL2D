# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'voiceSlide.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QSizePolicy, QSlider,
    QWidget)

class Ui_voiceSlide(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setEnabled(True)
        Form.resize(476, 150)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(30, 80, 411, 61))
        self.voiceBar = QSlider(self.groupBox)
        self.voiceBar.setObjectName(u"voiceBar")
        self.voiceBar.setEnabled(True)
        self.voiceBar.setGeometry(QRect(10, 20, 391, 31))
        self.voiceBar.setMaximum(100)
        self.voiceBar.setPageStep(9)
        self.voiceBar.setSliderPosition(0)
        self.voiceBar.setOrientation(Qt.Orientation.Horizontal)
        self.voiceBar.setInvertedAppearance(False)
        self.voiceBar.setInvertedControls(False)
        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(30, 20, 411, 51))
        self.thresholdSlide = QSlider(self.groupBox_2)
        self.thresholdSlide.setObjectName(u"thresholdSlide")
        self.thresholdSlide.setGeometry(QRect(10, 20, 391, 21))
        self.thresholdSlide.setOrientation(Qt.Orientation.Horizontal)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"current DB \uff08do not drag it, it only waste your time\uff09", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"voice Threshold Setting", None))
    # retranslateUi

