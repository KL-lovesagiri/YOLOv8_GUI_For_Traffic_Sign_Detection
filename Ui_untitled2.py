# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled2.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QSlider, QVBoxLayout,
    QWidget)

from qfluentwidgets import (DoubleSpinBox, Slider, SpinBox)

class Ui_Form2(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(300, 300)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.confSpinBox = DoubleSpinBox(Form)
        self.confSpinBox.setObjectName(u"confSpinBox")
        self.confSpinBox.setAlignment(Qt.AlignCenter)
        self.confSpinBox.setMaximum(1.000000000000000)
        self.confSpinBox.setSingleStep(0.010000000000000)
        self.confSpinBox.setStepType(QAbstractSpinBox.DefaultStepType)
        self.confSpinBox.setValue(0.250000000000000)

        self.gridLayout.addWidget(self.confSpinBox, 2, 1, 1, 1)

        self.numSpinBox = SpinBox(Form)
        self.numSpinBox.setObjectName(u"numSpinBox")
        self.numSpinBox.setAlignment(Qt.AlignCenter)
        self.numSpinBox.setMaximum(300)
        self.numSpinBox.setValue(300)

        self.gridLayout.addWidget(self.numSpinBox, 4, 1, 1, 1)

        self.resetOldSettingButton = QPushButton(Form)
        self.resetOldSettingButton.setObjectName(u"resetOldSettingButton")

        self.gridLayout.addWidget(self.resetOldSettingButton, 6, 0, 1, 2)

        self.confLabel = QLabel(Form)
        self.confLabel.setObjectName(u"confLabel")
        self.confLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.confLabel, 2, 0, 1, 1)

        self.iouLabel = QLabel(Form)
        self.iouLabel.setObjectName(u"iouLabel")
        self.iouLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.iouLabel, 0, 0, 1, 1)

        self.confSlider = Slider(Form)
        self.confSlider.setObjectName(u"confSlider")
        self.confSlider.setMaximum(100)
        self.confSlider.setValue(25)
        self.confSlider.setOrientation(Qt.Horizontal)
        self.confSlider.setTickPosition(QSlider.TicksAbove)
        self.confSlider.setTickInterval(10)

        self.gridLayout.addWidget(self.confSlider, 3, 0, 1, 2)

        self.numLabel = QLabel(Form)
        self.numLabel.setObjectName(u"numLabel")
        self.numLabel.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.numLabel, 4, 0, 1, 1)

        self.iouSlider = Slider(Form)
        self.iouSlider.setObjectName(u"iouSlider")
        self.iouSlider.setMaximum(100)
        self.iouSlider.setValue(70)
        self.iouSlider.setOrientation(Qt.Horizontal)
        self.iouSlider.setTickPosition(QSlider.TicksAbove)
        self.iouSlider.setTickInterval(10)

        self.gridLayout.addWidget(self.iouSlider, 1, 0, 1, 2)

        self.iouSpinBox = DoubleSpinBox(Form)
        self.iouSpinBox.setObjectName(u"iouSpinBox")
        self.iouSpinBox.setAlignment(Qt.AlignCenter)
        self.iouSpinBox.setMaximum(1.000000000000000)
        self.iouSpinBox.setSingleStep(0.010000000000000)
        self.iouSpinBox.setStepType(QAbstractSpinBox.DefaultStepType)
        self.iouSpinBox.setValue(0.700000000000000)

        self.gridLayout.addWidget(self.iouSpinBox, 0, 1, 1, 1)

        self.numSlider = Slider(Form)
        self.numSlider.setObjectName(u"numSlider")
        self.numSlider.setMaximum(300)
        self.numSlider.setValue(300)
        self.numSlider.setOrientation(Qt.Horizontal)
        self.numSlider.setTickPosition(QSlider.TicksAbove)
        self.numSlider.setTickInterval(10)

        self.gridLayout.addWidget(self.numSlider, 5, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.resetOldSettingButton.setText(QCoreApplication.translate("Form", u"\u6062\u590d\u9ed8\u8ba4", None))
        self.confLabel.setText(QCoreApplication.translate("Form", u"\u7f6e\u4fe1\u5ea6", None))
        self.iouLabel.setText(QCoreApplication.translate("Form", u"\u4ea4\u5e76\u6bd4", None))
        self.numLabel.setText(QCoreApplication.translate("Form", u"\u6700\u5927\u68c0\u6d4b\u6570\u91cf", None))
    # retranslateUi

