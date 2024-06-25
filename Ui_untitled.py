# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidgetItem, QVBoxLayout, QWidget)

from qfluentwidgets import (IndeterminateProgressBar, TableWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1000, 700)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer = QSpacerItem(20, 50, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.inputLabel = QLabel(self.widget)
        self.inputLabel.setObjectName(u"inputLabel")
        self.inputLabel.setMaximumSize(QSize(1024, 1024))
        font = QFont()
        font.setPointSize(12)
        self.inputLabel.setFont(font)
        self.inputLabel.setFrameShape(QFrame.NoFrame)
        self.inputLabel.setFrameShadow(QFrame.Plain)
        self.inputLabel.setScaledContents(False)
        self.inputLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.inputLabel)


        self.horizontalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.outputLabel = QLabel(self.widget_2)
        self.outputLabel.setObjectName(u"outputLabel")
        self.outputLabel.setMaximumSize(QSize(1024, 1024))
        self.outputLabel.setFont(font)
        self.outputLabel.setFrameShape(QFrame.NoFrame)
        self.outputLabel.setScaledContents(False)
        self.outputLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.outputLabel)


        self.horizontalLayout.addWidget(self.widget_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.startButton = QPushButton(Form)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout_2.addWidget(self.startButton)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.horizontalLayout_2.addWidget(self.progressBar)

        self.resetButton = QPushButton(Form)
        self.resetButton.setObjectName(u"resetButton")

        self.horizontalLayout_2.addWidget(self.resetButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tableWidget = TableWidget(Form)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMaximumSize(QSize(600, 200))

        self.horizontalLayout_3.addWidget(self.tableWidget)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.progressBar_2 = IndeterminateProgressBar(Form)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setValue(24)

        self.verticalLayout_3.addWidget(self.progressBar_2)

        self.progressBar_3 = IndeterminateProgressBar(Form)
        self.progressBar_3.setObjectName(u"progressBar_3")
        self.progressBar_3.setValue(24)

        self.verticalLayout_3.addWidget(self.progressBar_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.inputLabel.setText(QCoreApplication.translate("Form", u"\u539f\u59cb\u56fe\u50cf", None))
        self.outputLabel.setText(QCoreApplication.translate("Form", u"\u76ee\u6807\u56fe\u50cf", None))
        self.startButton.setText("")
        self.resetButton.setText("")
    # retranslateUi

