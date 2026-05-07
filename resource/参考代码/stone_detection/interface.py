# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interface.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import src_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1229, 932)
        icon = QIcon()
        icon.addFile(u":/pic/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"#widget{background-color: rgb(9, 10, 14)}\n"
"#widget_2{background-color: rgb(230, 230, 230)}\n"
"#widget_4{background-color: rgb(240, 240, 240);border-width: 1px;border-style: solid;border-color: rgb(5, 5, 5)}\n"
"#widget_5{border-width: 1px;border-style: solid;border-color: rgb(5, 5, 5)}\n"
"#widget_6{border-width: 1px;border-style: solid;border-color: rgb(5, 5, 5)}\n"
"#widget_8{background-color: rgb(230, 230, 230)}\n"
"#widget_26{background-color: rgb(240, 240, 240);border-width: 1px;border-style: solid;border-color: rgb(5, 5, 5)}\n"
"#widget_33{border-width: 1px;border-style: solid;border-color: rgb(5, 5, 5)}\n"
"\n"
"#label_20{color: white}\n"
"\n"
"#toolButton{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_2{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_3{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButto"
                        "n_4{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_5{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_6{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_7{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_8{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_9{background-color: rgb(255, 250, 250);border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_10{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_15{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_16{background-color: rgb(0, 136, 255);color : white;border-"
                        "radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_20{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_21{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_22{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_23{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_24{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_25{background-color: rgb(0, 136, 255);color : white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_26{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_27{border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_28{background-color: rgb(255, 250, 250);border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#to"
                        "olButton_29{background-color: rgb(255, 250, 250);border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"#toolButton_30{background-color: rgb(255, 40, 40);color: white;border-radius: 10px; border: 2px groove gray;border-style: outset}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        font = QFont()
        font.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        self.scrollArea.setFont(font)
        self.scrollArea.setStyleSheet(u"")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(-21, 0, 1248, 888))
        self.verticalLayout_14 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.scrollAreaWidgetContents)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(0, 75))
        self.widget.setMaximumSize(QSize(16777215, 100))
        self.widget.setFont(font)
        self.widget.setStyleSheet(u"")
        self.horizontalLayout_23 = QHBoxLayout(self.widget)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.label_20 = QLabel(self.widget)
        self.label_20.setObjectName(u"label_20")
        font1 = QFont()
        font1.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font1.setPointSize(25)
        self.label_20.setFont(font1)

        self.horizontalLayout_23.addWidget(self.label_20)

        self.horizontalSpacer_14 = QSpacerItem(648, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_14)

        self.homeBtn = QToolButton(self.widget)
        self.homeBtn.setObjectName(u"homeBtn")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.homeBtn.sizePolicy().hasHeightForWidth())
        self.homeBtn.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font2.setPointSize(20)
        self.homeBtn.setFont(font2)
        self.homeBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}")
        self.homeBtn.setCheckable(True)
        self.homeBtn.setChecked(True)

        self.horizontalLayout_23.addWidget(self.homeBtn)

        self.cutDataBtn = QToolButton(self.widget)
        self.cutDataBtn.setObjectName(u"cutDataBtn")
        sizePolicy1.setHeightForWidth(self.cutDataBtn.sizePolicy().hasHeightForWidth())
        self.cutDataBtn.setSizePolicy(sizePolicy1)
        self.cutDataBtn.setFont(font2)
        self.cutDataBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}")
        self.cutDataBtn.setCheckable(True)

        self.horizontalLayout_23.addWidget(self.cutDataBtn)

        self.scanDataBtn = QToolButton(self.widget)
        self.scanDataBtn.setObjectName(u"scanDataBtn")
        sizePolicy1.setHeightForWidth(self.scanDataBtn.sizePolicy().hasHeightForWidth())
        self.scanDataBtn.setSizePolicy(sizePolicy1)
        self.scanDataBtn.setFont(font2)
        self.scanDataBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}")
        self.scanDataBtn.setCheckable(True)

        self.horizontalLayout_23.addWidget(self.scanDataBtn)

        self.defectDetectBtn = QToolButton(self.widget)
        self.defectDetectBtn.setObjectName(u"defectDetectBtn")
        sizePolicy1.setHeightForWidth(self.defectDetectBtn.sizePolicy().hasHeightForWidth())
        self.defectDetectBtn.setSizePolicy(sizePolicy1)
        self.defectDetectBtn.setFont(font2)
        self.defectDetectBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}")
        self.defectDetectBtn.setCheckable(True)

        self.horizontalLayout_23.addWidget(self.defectDetectBtn)

        self.cadBtn = QToolButton(self.widget)
        self.cadBtn.setObjectName(u"cadBtn")
        sizePolicy1.setHeightForWidth(self.cadBtn.sizePolicy().hasHeightForWidth())
        self.cadBtn.setSizePolicy(sizePolicy1)
        self.cadBtn.setFont(font2)
        self.cadBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}")
        self.cadBtn.setCheckable(True)

        self.horizontalLayout_23.addWidget(self.cadBtn)

        self.hardwareCtrlBtn = QToolButton(self.widget)
        self.hardwareCtrlBtn.setObjectName(u"hardwareCtrlBtn")
        sizePolicy1.setHeightForWidth(self.hardwareCtrlBtn.sizePolicy().hasHeightForWidth())
        self.hardwareCtrlBtn.setSizePolicy(sizePolicy1)
        self.hardwareCtrlBtn.setFont(font2)
        self.hardwareCtrlBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}")
        self.hardwareCtrlBtn.setCheckable(True)

        self.horizontalLayout_23.addWidget(self.hardwareCtrlBtn)

        self.userCtlBtn = QToolButton(self.widget)
        self.userCtlBtn.setObjectName(u"userCtlBtn")
        sizePolicy1.setHeightForWidth(self.userCtlBtn.sizePolicy().hasHeightForWidth())
        self.userCtlBtn.setSizePolicy(sizePolicy1)
        self.userCtlBtn.setFont(font2)
        self.userCtlBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}\n"
"\n"
"QToolButton:disabled {\n"
"    background-color: lightgray;  /* \u7981\u7528\u7070\u8272 */\n"
"    color: gray;\n"
"    border: 1px solid #aaa;\n"
"}")
        self.userCtlBtn.setCheckable(True)

        self.horizontalLayout_23.addWidget(self.userCtlBtn)

        self.settingsBtn = QToolButton(self.widget)
        self.settingsBtn.setObjectName(u"settingsBtn")
        sizePolicy1.setHeightForWidth(self.settingsBtn.sizePolicy().hasHeightForWidth())
        self.settingsBtn.setSizePolicy(sizePolicy1)
        self.settingsBtn.setFont(font2)
        self.settingsBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: yellow;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"QToolButton:checked {\n"
"    background-color: darkgreen;  /* checked \u72b6\u6001\u6df1\u7eff\u8272 */\n"
"    color: white;                 /* \u6587\u5b57\u6362\u6210\u767d\u8272\u66f4\u660e\u663e */\n"
"}")
        self.settingsBtn.setCheckable(True)

        self.horizontalLayout_23.addWidget(self.settingsBtn)

        self.closeBtn = QToolButton(self.widget)
        self.closeBtn.setObjectName(u"closeBtn")
        sizePolicy1.setHeightForWidth(self.closeBtn.sizePolicy().hasHeightForWidth())
        self.closeBtn.setSizePolicy(sizePolicy1)
        self.closeBtn.setFont(font2)
        self.closeBtn.setStyleSheet(u"QToolButton {\n"
"    background-color: red;   /* \u9ed8\u8ba4\uff08\u975e checked \u72b6\u6001\uff09\u4eae\u9ec4\u8272 */\n"
"    border: 1px solid #666;\n"
"    border-radius: 6px;\n"
"    padding: 4px;\n"
"}\n"
"")
        self.closeBtn.setCheckable(False)

        self.horizontalLayout_23.addWidget(self.closeBtn)

        self.horizontalLayout_23.setStretch(0, 1)
        self.horizontalLayout_23.setStretch(10, 1)

        self.verticalLayout_14.addWidget(self.widget)

        self.stackedWidget = QStackedWidget(self.scrollAreaWidgetContents)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setFont(font)
        self.homePage = QWidget()
        self.homePage.setObjectName(u"homePage")
        self.homePage.setEnabled(True)
        self.verticalLayout_19 = QVBoxLayout(self.homePage)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.verticalLayout_16 = QVBoxLayout()
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.cuttingMachineLabel = QLabel(self.homePage)
        self.cuttingMachineLabel.setObjectName(u"cuttingMachineLabel")

        self.horizontalLayout_10.addWidget(self.cuttingMachineLabel)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.widget_37 = QWidget(self.homePage)
        self.widget_37.setObjectName(u"widget_37")
        self.verticalLayout_9 = QVBoxLayout(self.widget_37)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.widget_39 = QWidget(self.widget_37)
        self.widget_39.setObjectName(u"widget_39")
        self.widget_39.setFont(font)
        self.gridLayout_12 = QGridLayout(self.widget_39)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.label_31 = QLabel(self.widget_39)
        self.label_31.setObjectName(u"label_31")
        self.label_31.setFont(font2)

        self.gridLayout_12.addWidget(self.label_31, 0, 0, 1, 1)

        self.stoneSlabView = QGraphicsView(self.widget_39)
        self.stoneSlabView.setObjectName(u"stoneSlabView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.stoneSlabView.sizePolicy().hasHeightForWidth())
        self.stoneSlabView.setSizePolicy(sizePolicy2)

        self.gridLayout_12.addWidget(self.stoneSlabView, 1, 0, 1, 1)


        self.verticalLayout_9.addWidget(self.widget_39)

        self.verticalLayout_9.setStretch(0, 3)

        self.horizontalLayout_8.addWidget(self.widget_37)

        self.widget_23 = QWidget(self.homePage)
        self.widget_23.setObjectName(u"widget_23")
        self.verticalLayout_7 = QVBoxLayout(self.widget_23)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_24 = QWidget(self.widget_23)
        self.widget_24.setObjectName(u"widget_24")
        self.gridLayout_10 = QGridLayout(self.widget_24)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.label_30 = QLabel(self.widget_24)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFont(font2)

        self.gridLayout_10.addWidget(self.label_30, 1, 0, 1, 1)

        self.homeScanView = QGraphicsView(self.widget_24)
        self.homeScanView.setObjectName(u"homeScanView")
        sizePolicy2.setHeightForWidth(self.homeScanView.sizePolicy().hasHeightForWidth())
        self.homeScanView.setSizePolicy(sizePolicy2)

        self.gridLayout_10.addWidget(self.homeScanView, 2, 0, 1, 2)

        self.gridLayout_10.setColumnStretch(0, 3)

        self.verticalLayout_7.addWidget(self.widget_24)

        self.verticalLayout_7.setStretch(0, 3)

        self.horizontalLayout_8.addWidget(self.widget_23)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 1)

        self.verticalLayout_16.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.edgeProcessingLabel = QLabel(self.homePage)
        self.edgeProcessingLabel.setObjectName(u"edgeProcessingLabel")

        self.horizontalLayout_7.addWidget(self.edgeProcessingLabel)

        self.receivingLabel = QLabel(self.homePage)
        self.receivingLabel.setObjectName(u"receivingLabel")
        sizePolicy1.setHeightForWidth(self.receivingLabel.sizePolicy().hasHeightForWidth())
        self.receivingLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.receivingLabel)


        self.verticalLayout_16.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.monitorVideoLabel1 = QLabel(self.homePage)
        self.monitorVideoLabel1.setObjectName(u"monitorVideoLabel1")

        self.horizontalLayout_9.addWidget(self.monitorVideoLabel1)

        self.monitorVideoLabel2 = QLabel(self.homePage)
        self.monitorVideoLabel2.setObjectName(u"monitorVideoLabel2")

        self.horizontalLayout_9.addWidget(self.monitorVideoLabel2)


        self.verticalLayout_16.addLayout(self.horizontalLayout_9)

        self.verticalLayout_16.setStretch(0, 1)
        self.verticalLayout_16.setStretch(1, 1)
        self.verticalLayout_16.setStretch(2, 1)

        self.horizontalLayout_11.addLayout(self.verticalLayout_16)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.scanRateWidget = QWidget(self.homePage)
        self.scanRateWidget.setObjectName(u"scanRateWidget")

        self.verticalLayout_8.addWidget(self.scanRateWidget)

        self.label_13 = QLabel(self.homePage)
        self.label_13.setObjectName(u"label_13")
        font3 = QFont()
        font3.setPointSize(24)
        self.label_13.setFont(font3)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_13)

        self.passRateWidget = QWidget(self.homePage)
        self.passRateWidget.setObjectName(u"passRateWidget")

        self.verticalLayout_8.addWidget(self.passRateWidget)

        self.label_21 = QLabel(self.homePage)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font3)
        self.label_21.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_21)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.completedBtn = QPushButton(self.homePage)
        self.completedBtn.setObjectName(u"completedBtn")
        self.completedBtn.setFont(font3)

        self.horizontalLayout_6.addWidget(self.completedBtn)

        self.uncompletedBtn = QPushButton(self.homePage)
        self.uncompletedBtn.setObjectName(u"uncompletedBtn")
        self.uncompletedBtn.setFont(font3)

        self.horizontalLayout_6.addWidget(self.uncompletedBtn)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.verticalLayout_8.setStretch(0, 10)
        self.verticalLayout_8.setStretch(1, 1)
        self.verticalLayout_8.setStretch(2, 10)
        self.verticalLayout_8.setStretch(3, 1)
        self.verticalLayout_8.setStretch(4, 1)

        self.horizontalLayout_11.addLayout(self.verticalLayout_8)


        self.verticalLayout_19.addLayout(self.horizontalLayout_11)

        self.stackedWidget.addWidget(self.homePage)
        self.cutPage = QWidget()
        self.cutPage.setObjectName(u"cutPage")
        sizePolicy1.setHeightForWidth(self.cutPage.sizePolicy().hasHeightForWidth())
        self.cutPage.setSizePolicy(sizePolicy1)
        self.horizontalLayout_12 = QHBoxLayout(self.cutPage)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.verticalLayout_18 = QVBoxLayout()
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.widget_22 = QWidget(self.cutPage)
        self.widget_22.setObjectName(u"widget_22")
        self.widget_22.setFont(font)
        self.horizontalLayout_24 = QHBoxLayout(self.widget_22)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(0, 6, 0, 6)
        self.label_22 = QLabel(self.widget_22)
        self.label_22.setObjectName(u"label_22")
        font4 = QFont()
        font4.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font4.setPointSize(22)
        font4.setKerning(True)
        self.label_22.setFont(font4)
        self.label_22.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_24.addWidget(self.label_22)

        self.horizontalSpacer_15 = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_15)


        self.verticalLayout_18.addWidget(self.widget_22)

        self.widget_38 = QWidget(self.cutPage)
        self.widget_38.setObjectName(u"widget_38")
        self.widget_38.setFont(font)
        self.verticalLayout_15 = QVBoxLayout(self.widget_38)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.widget_42 = QWidget(self.widget_38)
        self.widget_42.setObjectName(u"widget_42")
        self.widget_42.setFont(font)
        self.verticalLayout_17 = QVBoxLayout(self.widget_42)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.widget_43 = QWidget(self.widget_42)
        self.widget_43.setObjectName(u"widget_43")
        self.widget_43.setFont(font2)
        self.horizontalLayout_28 = QHBoxLayout(self.widget_43)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.label_24 = QLabel(self.widget_43)
        self.label_24.setObjectName(u"label_24")
        font5 = QFont()
        font5.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font5.setPointSize(13)
        self.label_24.setFont(font5)

        self.horizontalLayout_28.addWidget(self.label_24)

        self.horizontalSpacer_17 = QSpacerItem(118, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_17)

        self.cutStartDateEdit = QDateEdit(self.widget_43)
        self.cutStartDateEdit.setObjectName(u"cutStartDateEdit")
        self.cutStartDateEdit.setFont(font2)
        self.cutStartDateEdit.setDateTime(QDateTime(QDate(2025, 9, 1), QTime(0, 0, 0)))

        self.horizontalLayout_28.addWidget(self.cutStartDateEdit)

        self.label_25 = QLabel(self.widget_43)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font2)

        self.horizontalLayout_28.addWidget(self.label_25)

        self.cutEndDateEdit = QDateEdit(self.widget_43)
        self.cutEndDateEdit.setObjectName(u"cutEndDateEdit")
        self.cutEndDateEdit.setFont(font2)

        self.horizontalLayout_28.addWidget(self.cutEndDateEdit)

        self.cutDataQueryTBtn = QToolButton(self.widget_43)
        self.cutDataQueryTBtn.setObjectName(u"cutDataQueryTBtn")
        self.cutDataQueryTBtn.setFont(font2)

        self.horizontalLayout_28.addWidget(self.cutDataQueryTBtn)

        self.dateResetTBtn = QToolButton(self.widget_43)
        self.dateResetTBtn.setObjectName(u"dateResetTBtn")
        self.dateResetTBtn.setFont(font2)

        self.horizontalLayout_28.addWidget(self.dateResetTBtn)


        self.verticalLayout_17.addWidget(self.widget_43)

        self.cutDataTable = QTableWidget(self.widget_42)
        if (self.cutDataTable.columnCount() < 11):
            self.cutDataTable.setColumnCount(11)
        font6 = QFont()
        font6.setPointSize(15)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(9, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        __qtablewidgetitem10.setFont(font6);
        self.cutDataTable.setHorizontalHeaderItem(10, __qtablewidgetitem10)
        if (self.cutDataTable.rowCount() < 20):
            self.cutDataTable.setRowCount(20)
        self.cutDataTable.setObjectName(u"cutDataTable")
        self.cutDataTable.setFont(font2)
        self.cutDataTable.setLayoutDirection(Qt.LeftToRight)
        self.cutDataTable.setAutoFillBackground(False)
        self.cutDataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cutDataTable.setSortingEnabled(False)
        self.cutDataTable.setRowCount(20)
        self.cutDataTable.horizontalHeader().setCascadingSectionResizes(False)
        self.cutDataTable.horizontalHeader().setDefaultSectionSize(175)
        self.cutDataTable.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_17.addWidget(self.cutDataTable)


        self.verticalLayout_15.addWidget(self.widget_42)

        self.verticalLayout_15.setStretch(0, 4)

        self.verticalLayout_18.addWidget(self.widget_38)


        self.horizontalLayout_12.addLayout(self.verticalLayout_18)

        self.stackedWidget.addWidget(self.cutPage)
        self.hardwareCtrl = QWidget()
        self.hardwareCtrl.setObjectName(u"hardwareCtrl")
        self.horizontalLayout_37 = QHBoxLayout(self.hardwareCtrl)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.allCtrBox = QGroupBox(self.hardwareCtrl)
        self.allCtrBox.setObjectName(u"allCtrBox")
        font7 = QFont()
        font7.setPointSize(16)
        self.allCtrBox.setFont(font7)
        self.verticalLayout_23 = QVBoxLayout(self.allCtrBox)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.connect_all_btn = QPushButton(self.allCtrBox)
        self.connect_all_btn.setObjectName(u"connect_all_btn")

        self.horizontalLayout_30.addWidget(self.connect_all_btn)

        self.disconnect_all_btn = QPushButton(self.allCtrBox)
        self.disconnect_all_btn.setObjectName(u"disconnect_all_btn")

        self.horizontalLayout_30.addWidget(self.disconnect_all_btn)

        self.start_qr_monitor_btn = QPushButton(self.allCtrBox)
        self.start_qr_monitor_btn.setObjectName(u"start_qr_monitor_btn")

        self.horizontalLayout_30.addWidget(self.start_qr_monitor_btn)

        self.stop_qr_monitor = QPushButton(self.allCtrBox)
        self.stop_qr_monitor.setObjectName(u"stop_qr_monitor")

        self.horizontalLayout_30.addWidget(self.stop_qr_monitor)


        self.verticalLayout_23.addLayout(self.horizontalLayout_30)


        self.horizontalLayout_31.addWidget(self.allCtrBox)

        self.flipperCtrBox = QGroupBox(self.hardwareCtrl)
        self.flipperCtrBox.setObjectName(u"flipperCtrBox")
        font8 = QFont()
        font8.setPointSize(18)
        font8.setUnderline(False)
        self.flipperCtrBox.setFont(font8)
        self.flipperCtrBox.setMouseTracking(False)
        self.flipperCtrBox.setTabletTracking(False)
        self.flipperCtrBox.setFlat(False)
        self.horizontalLayout_32 = QHBoxLayout(self.flipperCtrBox)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.connect_flipper_btn = QPushButton(self.flipperCtrBox)
        self.connect_flipper_btn.setObjectName(u"connect_flipper_btn")

        self.horizontalLayout_13.addWidget(self.connect_flipper_btn)

        self.disconnect_flipper_btn = QPushButton(self.flipperCtrBox)
        self.disconnect_flipper_btn.setObjectName(u"disconnect_flipper_btn")

        self.horizontalLayout_13.addWidget(self.disconnect_flipper_btn)

        self.start_flipper_monitor_btn = QPushButton(self.flipperCtrBox)
        self.start_flipper_monitor_btn.setObjectName(u"start_flipper_monitor_btn")

        self.horizontalLayout_13.addWidget(self.start_flipper_monitor_btn)

        self.stop_flipper_monitor_btn = QPushButton(self.flipperCtrBox)
        self.stop_flipper_monitor_btn.setObjectName(u"stop_flipper_monitor_btn")

        self.horizontalLayout_13.addWidget(self.stop_flipper_monitor_btn)


        self.horizontalLayout_32.addLayout(self.horizontalLayout_13)


        self.horizontalLayout_31.addWidget(self.flipperCtrBox)


        self.verticalLayout_21.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.edgeGrinderCtrBox = QGroupBox(self.hardwareCtrl)
        self.edgeGrinderCtrBox.setObjectName(u"edgeGrinderCtrBox")
        font9 = QFont()
        font9.setPointSize(18)
        self.edgeGrinderCtrBox.setFont(font9)
        self.horizontalLayout_29 = QHBoxLayout(self.edgeGrinderCtrBox)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.connect_edge_btn = QPushButton(self.edgeGrinderCtrBox)
        self.connect_edge_btn.setObjectName(u"connect_edge_btn")

        self.horizontalLayout_15.addWidget(self.connect_edge_btn)

        self.disconnect_edge_btn = QPushButton(self.edgeGrinderCtrBox)
        self.disconnect_edge_btn.setObjectName(u"disconnect_edge_btn")

        self.horizontalLayout_15.addWidget(self.disconnect_edge_btn)

        self.start_edge_monitor_btn = QPushButton(self.edgeGrinderCtrBox)
        self.start_edge_monitor_btn.setObjectName(u"start_edge_monitor_btn")

        self.horizontalLayout_15.addWidget(self.start_edge_monitor_btn)

        self.stop_edge_monitor_btn = QPushButton(self.edgeGrinderCtrBox)
        self.stop_edge_monitor_btn.setObjectName(u"stop_edge_monitor_btn")

        self.horizontalLayout_15.addWidget(self.stop_edge_monitor_btn)


        self.horizontalLayout_29.addLayout(self.horizontalLayout_15)


        self.horizontalLayout_33.addWidget(self.edgeGrinderCtrBox)

        self.sorterCtrBox = QGroupBox(self.hardwareCtrl)
        self.sorterCtrBox.setObjectName(u"sorterCtrBox")
        self.sorterCtrBox.setFont(font9)
        self.verticalLayout_22 = QVBoxLayout(self.sorterCtrBox)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.connect_sorter_btn = QPushButton(self.sorterCtrBox)
        self.connect_sorter_btn.setObjectName(u"connect_sorter_btn")

        self.horizontalLayout_14.addWidget(self.connect_sorter_btn)

        self.disconnect_sorter_btn = QPushButton(self.sorterCtrBox)
        self.disconnect_sorter_btn.setObjectName(u"disconnect_sorter_btn")

        self.horizontalLayout_14.addWidget(self.disconnect_sorter_btn)

        self.start_sorter_monitor_btn = QPushButton(self.sorterCtrBox)
        self.start_sorter_monitor_btn.setObjectName(u"start_sorter_monitor_btn")

        self.horizontalLayout_14.addWidget(self.start_sorter_monitor_btn)

        self.stop_sorter_monitor_btn = QPushButton(self.sorterCtrBox)
        self.stop_sorter_monitor_btn.setObjectName(u"stop_sorter_monitor_btn")

        self.horizontalLayout_14.addWidget(self.stop_sorter_monitor_btn)


        self.verticalLayout_22.addLayout(self.horizontalLayout_14)


        self.horizontalLayout_33.addWidget(self.sorterCtrBox)


        self.verticalLayout_21.addLayout(self.horizontalLayout_33)

        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.flipperStateLabel = QLabel(self.hardwareCtrl)
        self.flipperStateLabel.setObjectName(u"flipperStateLabel")
        self.flipperStateLabel.setFont(font9)

        self.horizontalLayout_26.addWidget(self.flipperStateLabel)

        self.sorterStateLabel = QLabel(self.hardwareCtrl)
        self.sorterStateLabel.setObjectName(u"sorterStateLabel")
        self.sorterStateLabel.setFont(font9)

        self.horizontalLayout_26.addWidget(self.sorterStateLabel)

        self.qrBeforeEdgeStateLabel = QLabel(self.hardwareCtrl)
        self.qrBeforeEdgeStateLabel.setObjectName(u"qrBeforeEdgeStateLabel")
        self.qrBeforeEdgeStateLabel.setFont(font9)

        self.horizontalLayout_26.addWidget(self.qrBeforeEdgeStateLabel)

        self.qrBeforeSorterStateLabel = QLabel(self.hardwareCtrl)
        self.qrBeforeSorterStateLabel.setObjectName(u"qrBeforeSorterStateLabel")
        self.qrBeforeSorterStateLabel.setFont(font9)

        self.horizontalLayout_26.addWidget(self.qrBeforeSorterStateLabel)


        self.verticalLayout_20.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.edgeGrinderStateLabel1 = QLabel(self.hardwareCtrl)
        self.edgeGrinderStateLabel1.setObjectName(u"edgeGrinderStateLabel1")
        self.edgeGrinderStateLabel1.setFont(font9)

        self.horizontalLayout_25.addWidget(self.edgeGrinderStateLabel1)

        self.edgeGrinderStateLabel2 = QLabel(self.hardwareCtrl)
        self.edgeGrinderStateLabel2.setObjectName(u"edgeGrinderStateLabel2")
        self.edgeGrinderStateLabel2.setFont(font9)

        self.horizontalLayout_25.addWidget(self.edgeGrinderStateLabel2)

        self.edgeGrinderStateLabel3 = QLabel(self.hardwareCtrl)
        self.edgeGrinderStateLabel3.setObjectName(u"edgeGrinderStateLabel3")
        self.edgeGrinderStateLabel3.setFont(font9)

        self.horizontalLayout_25.addWidget(self.edgeGrinderStateLabel3)

        self.edgeGrinderStateLabel4 = QLabel(self.hardwareCtrl)
        self.edgeGrinderStateLabel4.setObjectName(u"edgeGrinderStateLabel4")
        self.edgeGrinderStateLabel4.setFont(font9)

        self.horizontalLayout_25.addWidget(self.edgeGrinderStateLabel4)


        self.verticalLayout_20.addLayout(self.horizontalLayout_25)


        self.verticalLayout_21.addLayout(self.verticalLayout_20)

        self.groupBox_5 = QGroupBox(self.hardwareCtrl)
        self.groupBox_5.setObjectName(u"groupBox_5")
        font10 = QFont()
        font10.setPointSize(20)
        self.groupBox_5.setFont(font10)
        self.horizontalLayout_27 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.logPlainTextEdit = QPlainTextEdit(self.groupBox_5)
        self.logPlainTextEdit.setObjectName(u"logPlainTextEdit")
        self.logPlainTextEdit.setReadOnly(True)
        self.logPlainTextEdit.setCenterOnScroll(False)
        # 确保垂直滚动条始终开启，并设置自动换行
        self.logPlainTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)  # 始终显示滑块
        self.logPlainTextEdit.setLineWrapMode(QPlainTextEdit.WidgetWidth)  # 自动换行
        self.logPlainTextEdit.setReadOnly(True)


        self.horizontalLayout_27.addWidget(self.logPlainTextEdit)

        self.verticalLayout_21.addWidget(self.groupBox_5)


        self.horizontalLayout_37.addLayout(self.verticalLayout_21)

        self.stackedWidget.addWidget(self.hardwareCtrl)
        self.scanPage = QWidget()
        self.scanPage.setObjectName(u"scanPage")
        self.verticalLayout = QVBoxLayout(self.scanPage)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.scanPage)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setFont(font)
        self.horizontalLayout_21 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 6, 0, 6)
        self.label_18 = QLabel(self.widget_2)
        self.label_18.setObjectName(u"label_18")
        font11 = QFont()
        font11.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font11.setPointSize(22)
        self.label_18.setFont(font11)
        self.label_18.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_21.addWidget(self.label_18)

        self.scanStartBtn = QToolButton(self.widget_2)
        self.scanStartBtn.setObjectName(u"scanStartBtn")
        sizePolicy1.setHeightForWidth(self.scanStartBtn.sizePolicy().hasHeightForWidth())
        self.scanStartBtn.setSizePolicy(sizePolicy1)
        self.scanStartBtn.setFont(font2)
        self.scanStartBtn.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px; \n"
"    border: 2px groove gray;\n"
"    border-style: outset;\n"
"    background-color: none;\n"
"    color: black;\n"
"}\n"
"QToolButton:checked {\n"
"    background-color: rgb(0, 136, 255);\n"
"    color: white;\n"
"}\n"
"")
        self.scanStartBtn.setCheckable(True)

        self.horizontalLayout_21.addWidget(self.scanStartBtn)

        self.widget_36 = QWidget(self.widget_2)
        self.widget_36.setObjectName(u"widget_36")
        self.widget_36.setFont(font)
        self.horizontalLayout_22 = QHBoxLayout(self.widget_36)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")

        self.horizontalLayout_21.addWidget(self.widget_36)

        self.horizontalSpacer_13 = QSpacerItem(316, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_13)

        self.scanViewLargeBtn = QToolButton(self.widget_2)
        self.scanViewLargeBtn.setObjectName(u"scanViewLargeBtn")
        sizePolicy1.setHeightForWidth(self.scanViewLargeBtn.sizePolicy().hasHeightForWidth())
        self.scanViewLargeBtn.setSizePolicy(sizePolicy1)
        self.scanViewLargeBtn.setFont(font2)
        self.scanViewLargeBtn.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px; \n"
"    border: 2px groove gray;\n"
"    border-style: outset;\n"
"    background-color: none;\n"
"    color: black;\n"
"}")

        self.horizontalLayout_21.addWidget(self.scanViewLargeBtn)

        self.scanOriginalBtn = QToolButton(self.widget_2)
        self.scanOriginalBtn.setObjectName(u"scanOriginalBtn")
        sizePolicy1.setHeightForWidth(self.scanOriginalBtn.sizePolicy().hasHeightForWidth())
        self.scanOriginalBtn.setSizePolicy(sizePolicy1)
        self.scanOriginalBtn.setFont(font2)
        self.scanOriginalBtn.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px; \n"
"    border: 2px groove gray;\n"
"    border-style: outset;\n"
"    background-color: none;\n"
"    color: black;\n"
"}\n"
"QToolButton:checked {\n"
"    background-color: rgb(0, 136, 255);\n"
"    color: white;\n"
"}\n"
"")
        self.scanOriginalBtn.setCheckable(True)
        self.scanOriginalBtn.setChecked(True)

        self.horizontalLayout_21.addWidget(self.scanOriginalBtn)

        self.scanRulerBtn = QToolButton(self.widget_2)
        self.scanRulerBtn.setObjectName(u"scanRulerBtn")
        sizePolicy1.setHeightForWidth(self.scanRulerBtn.sizePolicy().hasHeightForWidth())
        self.scanRulerBtn.setSizePolicy(sizePolicy1)
        self.scanRulerBtn.setFont(font2)
        self.scanRulerBtn.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px; \n"
"    border: 2px groove gray;\n"
"    border-style: outset;\n"
"    background-color: none;\n"
"    color: black;\n"
"}\n"
"QToolButton:checked {\n"
"    background-color: rgb(0, 136, 255);\n"
"    color: white;\n"
"}\n"
"")
        self.scanRulerBtn.setCheckable(True)

        self.horizontalLayout_21.addWidget(self.scanRulerBtn)

        self.horizontalLayout_21.setStretch(0, 1)
        self.horizontalLayout_21.setStretch(1, 1)
        self.horizontalLayout_21.setStretch(2, 1)
        self.horizontalLayout_21.setStretch(3, 2)
        self.horizontalLayout_21.setStretch(4, 1)
        self.horizontalLayout_21.setStretch(5, 1)
        self.horizontalLayout_21.setStretch(6, 1)

        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.scanPage)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setFont(font)
        self.horizontalLayout_16 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_16.setSpacing(6)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.widget_26 = QWidget(self.widget_3)
        self.widget_26.setObjectName(u"widget_26")
        self.widget_26.setFont(font)
        self.verticalLayout_10 = QVBoxLayout(self.widget_26)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.widget_27 = QWidget(self.widget_26)
        self.widget_27.setObjectName(u"widget_27")
        self.widget_27.setMaximumSize(QSize(16777215, 50))
        self.widget_27.setFont(font)
        self.verticalLayout_11 = QVBoxLayout(self.widget_27)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.widget_28 = QWidget(self.widget_27)
        self.widget_28.setObjectName(u"widget_28")
        self.widget_28.setMaximumSize(QSize(16777215, 50))
        self.widget_28.setFont(font)
        self.horizontalLayout_17 = QHBoxLayout(self.widget_28)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.areaStatsTBtn = QToolButton(self.widget_28)
        self.areaStatsTBtn.setObjectName(u"areaStatsTBtn")
        sizePolicy1.setHeightForWidth(self.areaStatsTBtn.sizePolicy().hasHeightForWidth())
        self.areaStatsTBtn.setSizePolicy(sizePolicy1)
        font12 = QFont()
        font12.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font12.setPointSize(16)
        self.areaStatsTBtn.setFont(font12)
        self.areaStatsTBtn.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px; \n"
"    border: 2px groove gray;\n"
"    border-style: outset;\n"
"    background-color: none;\n"
"    color: black;\n"
"}\n"
"QToolButton:checked {\n"
"    background-color: rgb(0, 136, 255);\n"
"    color: white;\n"
"}\n"
"")
        self.areaStatsTBtn.setCheckable(True)
        self.areaStatsTBtn.setChecked(True)

        self.horizontalLayout_17.addWidget(self.areaStatsTBtn)

        self.countStatsTBtn = QToolButton(self.widget_28)
        self.countStatsTBtn.setObjectName(u"countStatsTBtn")
        sizePolicy1.setHeightForWidth(self.countStatsTBtn.sizePolicy().hasHeightForWidth())
        self.countStatsTBtn.setSizePolicy(sizePolicy1)
        self.countStatsTBtn.setFont(font12)
        self.countStatsTBtn.setStyleSheet(u"QToolButton {\n"
"    border-radius: 10px; \n"
"    border: 2px groove gray;\n"
"    border-style: outset;\n"
"    background-color: none;\n"
"    color: black;\n"
"}\n"
"QToolButton:checked {\n"
"    background-color: rgb(0, 136, 255);\n"
"    color: white;\n"
"}\n"
"")
        self.countStatsTBtn.setCheckable(True)

        self.horizontalLayout_17.addWidget(self.countStatsTBtn)

        self.horizontalSpacer_10 = QSpacerItem(368, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_10)

        self.scanStatusLabel = QLabel(self.widget_28)
        self.scanStatusLabel.setObjectName(u"scanStatusLabel")
        self.scanStatusLabel.setFont(font2)
        self.scanStatusLabel.setStyleSheet(u"#scanStatusLabel {\n"
"    border: 2px solid gray;      /* \u8fb9\u6846\u5bbd\u5ea6 + \u989c\u8272 */\n"
"    border-radius: 10px;         /* \u5706\u89d2\u534a\u5f84 */\n"
"    background-color: white;     /* \u80cc\u666f\u8272 */\n"
"}\n"
"")

        self.horizontalLayout_17.addWidget(self.scanStatusLabel)

        self.horizontalLayout_17.setStretch(0, 1)
        self.horizontalLayout_17.setStretch(1, 1)
        self.horizontalLayout_17.setStretch(2, 1)
        self.horizontalLayout_17.setStretch(3, 1)

        self.verticalLayout_11.addWidget(self.widget_28)

        self.verticalLayout_11.setStretch(0, 1)

        self.verticalLayout_10.addWidget(self.widget_27)

        self.widget_29 = QWidget(self.widget_26)
        self.widget_29.setObjectName(u"widget_29")
        self.widget_29.setFont(font)
        self.widget_29.setStyleSheet(u"#widget_29 {\n"
"    border: 2px solid gray;      /* \u8fb9\u6846\u5bbd\u5ea6 + \u989c\u8272 */\n"
"    border-radius: 10px;         /* \u5706\u89d2\u534a\u5f84 */\n"
"    background-color: white;     /* \u80cc\u666f\u8272 */\n"
"}\n"
"")
        self.horizontalLayout_18 = QHBoxLayout(self.widget_29)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_19 = QLabel(self.widget_29)
        self.label_19.setObjectName(u"label_19")
        font13 = QFont()
        font13.setPointSize(22)
        self.label_19.setFont(font13)
        self.label_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_19)

        self.totalScanLabel = QLabel(self.widget_29)
        self.totalScanLabel.setObjectName(u"totalScanLabel")
        self.totalScanLabel.setFont(font13)

        self.horizontalLayout_18.addWidget(self.totalScanLabel)

        self.label_34 = QLabel(self.widget_29)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setFont(font13)
        self.label_34.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_18.addWidget(self.label_34)

        self.todayScanLabel = QLabel(self.widget_29)
        self.todayScanLabel.setObjectName(u"todayScanLabel")
        self.todayScanLabel.setFont(font13)

        self.horizontalLayout_18.addWidget(self.todayScanLabel)


        self.verticalLayout_10.addWidget(self.widget_29)

        self.widget_30 = QWidget(self.widget_26)
        self.widget_30.setObjectName(u"widget_30")
        self.widget_30.setFont(font)
        self.verticalLayout_12 = QVBoxLayout(self.widget_30)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.widget_31 = QWidget(self.widget_30)
        self.widget_31.setObjectName(u"widget_31")
        self.widget_31.setFont(font)
        self.widget_31.setStyleSheet(u"#widget_31 {\n"
"    border: 2px solid gray;      /* \u8fb9\u6846\u5bbd\u5ea6 + \u989c\u8272 */\n"
"    border-radius: 10px;         /* \u5706\u89d2\u534a\u5f84 */\n"
"    background-color: white;     /* \u80cc\u666f\u8272 */\n"
"}\n"
"")
        self.horizontalLayout_19 = QHBoxLayout(self.widget_31)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalSpacer_11 = QSpacerItem(118, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_11)

        self.scanStartDateEdit = QDateEdit(self.widget_31)
        self.scanStartDateEdit.setObjectName(u"scanStartDateEdit")
        self.scanStartDateEdit.setFont(font2)

        self.horizontalLayout_19.addWidget(self.scanStartDateEdit)

        self.label_16 = QLabel(self.widget_31)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setFont(font2)

        self.horizontalLayout_19.addWidget(self.label_16)

        self.scanEndDateEdit = QDateEdit(self.widget_31)
        self.scanEndDateEdit.setObjectName(u"scanEndDateEdit")
        self.scanEndDateEdit.setFont(font2)

        self.horizontalLayout_19.addWidget(self.scanEndDateEdit)

        self.scanQueryBtn = QToolButton(self.widget_31)
        self.scanQueryBtn.setObjectName(u"scanQueryBtn")
        self.scanQueryBtn.setFont(font2)

        self.horizontalLayout_19.addWidget(self.scanQueryBtn)

        self.scanResetBtn = QToolButton(self.widget_31)
        self.scanResetBtn.setObjectName(u"scanResetBtn")
        self.scanResetBtn.setFont(font2)

        self.horizontalLayout_19.addWidget(self.scanResetBtn)


        self.verticalLayout_12.addWidget(self.widget_31)
        # 配置一个名为 self.scanDataTable 的表格控件的表头（Header）、行数（Row Count）、字体和行为属性。
        self.scanDataTable = QTableWidget(self.widget_30)
        if (self.scanDataTable.columnCount() < 8):
            self.scanDataTable.setColumnCount(8)
        __qtablewidgetitem11 = QTableWidgetItem()
        __qtablewidgetitem11.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        __qtablewidgetitem12.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        __qtablewidgetitem13.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(2, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        __qtablewidgetitem14.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(3, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(4, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        __qtablewidgetitem16.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(5, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        __qtablewidgetitem17.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(6, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        __qtablewidgetitem18.setFont(font10);
        self.scanDataTable.setHorizontalHeaderItem(7, __qtablewidgetitem18)
        if (self.scanDataTable.rowCount() < 20):
            self.scanDataTable.setRowCount(20)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.scanDataTable.setItem(0, 2, __qtablewidgetitem19)
        self.scanDataTable.setObjectName(u"scanDataTable")
        self.scanDataTable.setFont(font2)
        self.scanDataTable.setLayoutDirection(Qt.LeftToRight)
        self.scanDataTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.scanDataTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.scanDataTable.setRowCount(20)
        self.scanDataTable.horizontalHeader().setDefaultSectionSize(150)

        self.verticalLayout_12.addWidget(self.scanDataTable)


        self.verticalLayout_10.addWidget(self.widget_30)

        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(2, 4)

        self.horizontalLayout_16.addWidget(self.widget_26)

        self.widget_32 = QWidget(self.widget_3)
        self.widget_32.setObjectName(u"widget_32")
        self.widget_32.setFont(font)
        self.verticalLayout_13 = QVBoxLayout(self.widget_32)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.widget_33 = QWidget(self.widget_32)
        self.widget_33.setObjectName(u"widget_33")
        self.widget_33.setFont(font)
        self.gridLayout_5 = QGridLayout(self.widget_33)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setHorizontalSpacing(0)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.scanPicView = QGraphicsView(self.widget_33)
        self.scanPicView.setObjectName(u"scanPicView")

        self.gridLayout_5.addWidget(self.scanPicView, 0, 0, 1, 1)


        self.verticalLayout_13.addWidget(self.widget_33)

        self.widget_34 = QWidget(self.widget_32)
        self.widget_34.setObjectName(u"widget_34")
        self.widget_34.setFont(font)
        self.horizontalLayout_20 = QHBoxLayout(self.widget_34)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_17 = QLabel(self.widget_34)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font2)
        self.horizontalLayout_20.addWidget(self.label_17)
        self.horizontalSpacer_12 = QSpacerItem(344, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(self.horizontalSpacer_12)
        self.verticalLayout_13.addWidget(self.widget_34)

        self.widget_35 = QWidget(self.widget_32)
        self.widget_35.setObjectName(u"widget_35")
        self.widget_35.setFont(font)
        self.gridLayout_4 = QGridLayout(self.widget_35)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.scanLogBrowser = QTextBrowser(self.widget_35)
        self.scanLogBrowser.setObjectName(u"scanLogBrowser")
        self.scanLogBrowser.setFont(font2)

        self.gridLayout_4.addWidget(self.scanLogBrowser, 0, 0, 1, 1)
        self.verticalLayout_13.addWidget(self.widget_35)

        self.verticalLayout_13.setStretch(0, 6)
        self.verticalLayout_13.setStretch(1, 1)
        self.verticalLayout_13.setStretch(2, 6)

        self.horizontalLayout_16.addWidget(self.widget_32)

        self.horizontalLayout_16.setStretch(0, 3)
        self.horizontalLayout_16.setStretch(1, 2)

        self.verticalLayout.addWidget(self.widget_3)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 14)
        self.stackedWidget.addWidget(self.scanPage)
        self.cadPage = QWidget()
        self.cadPage.setObjectName(u"cadPage")
        self.cadPage.setStyleSheet(u"")
        self.gridLayout = QGridLayout(self.cadPage)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_8 = QWidget(self.cadPage)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.widget_9 = QWidget(self.widget_8)
        self.widget_9.setObjectName(u"widget_9")
        self.verticalLayout_5 = QVBoxLayout(self.widget_9)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_11 = QWidget(self.widget_9)
        self.widget_11.setObjectName(u"widget_11")
        self.widget_11.setFont(font)
        self.gridLayout_3 = QGridLayout(self.widget_11)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_2 = QLabel(self.widget_11)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.graphicsView_3 = QGraphicsView(self.widget_11)
        self.graphicsView_3.setObjectName(u"graphicsView_3")
        sizePolicy2.setHeightForWidth(self.graphicsView_3.sizePolicy().hasHeightForWidth())
        self.graphicsView_3.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.graphicsView_3, 1, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.widget_11)

        self.widget_12 = QWidget(self.widget_9)
        self.widget_12.setObjectName(u"widget_12")
        self.gridLayout_6 = QGridLayout(self.widget_12)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_4 = QLabel(self.widget_12)
        self.label_4.setObjectName(u"label_4")
        font14 = QFont()
        font14.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font14.setPointSize(14)
        self.label_4.setFont(font14)

        self.gridLayout_6.addWidget(self.label_4, 0, 0, 1, 4)

        self.verticalSpacer_2 = QSpacerItem(20, 37, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(104, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_2, 2, 0, 1, 1)

        self.toolButton_7 = QToolButton(self.widget_12)
        self.toolButton_7.setObjectName(u"toolButton_7")
        sizePolicy1.setHeightForWidth(self.toolButton_7.sizePolicy().hasHeightForWidth())
        self.toolButton_7.setSizePolicy(sizePolicy1)
        self.toolButton_7.setFont(font14)

        self.gridLayout_6.addWidget(self.toolButton_7, 2, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(104, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 2, 2, 1, 1)

        self.toolButton_6 = QToolButton(self.widget_12)
        self.toolButton_6.setObjectName(u"toolButton_6")
        sizePolicy1.setHeightForWidth(self.toolButton_6.sizePolicy().hasHeightForWidth())
        self.toolButton_6.setSizePolicy(sizePolicy1)
        self.toolButton_6.setFont(font14)

        self.gridLayout_6.addWidget(self.toolButton_6, 2, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(104, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_4, 2, 4, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 37, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_6.addItem(self.verticalSpacer_3, 3, 2, 1, 1)

        self.toolButton_10 = QToolButton(self.widget_12)
        self.toolButton_10.setObjectName(u"toolButton_10")
        sizePolicy1.setHeightForWidth(self.toolButton_10.sizePolicy().hasHeightForWidth())
        self.toolButton_10.setSizePolicy(sizePolicy1)
        self.toolButton_10.setFont(font14)

        self.gridLayout_6.addWidget(self.toolButton_10, 0, 4, 1, 1)

        self.gridLayout_6.setRowStretch(0, 1)
        self.gridLayout_6.setRowStretch(1, 1)
        self.gridLayout_6.setRowStretch(2, 1)
        self.gridLayout_6.setRowStretch(3, 1)
        self.gridLayout_6.setColumnStretch(0, 1)
        self.gridLayout_6.setColumnStretch(1, 2)
        self.gridLayout_6.setColumnStretch(2, 1)
        self.gridLayout_6.setColumnStretch(3, 2)
        self.gridLayout_6.setColumnStretch(4, 1)

        self.verticalLayout_5.addWidget(self.widget_12)

        self.verticalLayout_5.setStretch(0, 3)
        self.verticalLayout_5.setStretch(1, 1)

        self.horizontalLayout_3.addWidget(self.widget_9)

        self.widget_10 = QWidget(self.widget_8)
        self.widget_10.setObjectName(u"widget_10")
        self.verticalLayout_6 = QVBoxLayout(self.widget_10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget_13 = QWidget(self.widget_10)
        self.widget_13.setObjectName(u"widget_13")
        self.gridLayout_2 = QGridLayout(self.widget_13)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_3 = QLabel(self.widget_13)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font2)

        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)

        self.graphicsView_4 = QGraphicsView(self.widget_13)
        self.graphicsView_4.setObjectName(u"graphicsView_4")
        sizePolicy2.setHeightForWidth(self.graphicsView_4.sizePolicy().hasHeightForWidth())
        self.graphicsView_4.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.graphicsView_4, 1, 0, 1, 2)

        self.toolButton_15 = QToolButton(self.widget_13)
        self.toolButton_15.setObjectName(u"toolButton_15")
        sizePolicy1.setHeightForWidth(self.toolButton_15.sizePolicy().hasHeightForWidth())
        self.toolButton_15.setSizePolicy(sizePolicy1)
        self.toolButton_15.setFont(font14)

        self.gridLayout_2.addWidget(self.toolButton_15, 0, 1, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 3)
        self.gridLayout_2.setColumnStretch(1, 1)

        self.verticalLayout_6.addWidget(self.widget_13)

        self.widget_14 = QWidget(self.widget_10)
        self.widget_14.setObjectName(u"widget_14")
        self.gridLayout_7 = QGridLayout(self.widget_14)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.verticalSpacer_4 = QSpacerItem(20, 59, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_4, 0, 1, 1, 2)

        self.horizontalSpacer_6 = QSpacerItem(73, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_6, 1, 0, 1, 1)

        self.toolButton_8 = QToolButton(self.widget_14)
        self.toolButton_8.setObjectName(u"toolButton_8")
        sizePolicy1.setHeightForWidth(self.toolButton_8.sizePolicy().hasHeightForWidth())
        self.toolButton_8.setSizePolicy(sizePolicy1)
        self.toolButton_8.setFont(font14)

        self.gridLayout_7.addWidget(self.toolButton_8, 1, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(73, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.toolButton_16 = QToolButton(self.widget_14)
        self.toolButton_16.setObjectName(u"toolButton_16")
        sizePolicy1.setHeightForWidth(self.toolButton_16.sizePolicy().hasHeightForWidth())
        self.toolButton_16.setSizePolicy(sizePolicy1)
        font15 = QFont()
        font15.setPointSize(14)
        self.toolButton_16.setFont(font15)

        self.gridLayout_7.addWidget(self.toolButton_16, 1, 3, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(73, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_7.addItem(self.horizontalSpacer_8, 1, 4, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 59, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_5, 2, 1, 1, 2)

        self.gridLayout_7.setRowStretch(0, 3)
        self.gridLayout_7.setRowStretch(1, 2)
        self.gridLayout_7.setRowStretch(2, 3)
        self.gridLayout_7.setColumnStretch(0, 1)
        self.gridLayout_7.setColumnStretch(1, 2)
        self.gridLayout_7.setColumnStretch(2, 1)
        self.gridLayout_7.setColumnStretch(3, 2)
        self.gridLayout_7.setColumnStretch(4, 1)

        self.verticalLayout_6.addWidget(self.widget_14)

        self.verticalLayout_6.setStretch(0, 3)
        self.verticalLayout_6.setStretch(1, 1)

        self.horizontalLayout_3.addWidget(self.widget_10)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 1)

        self.gridLayout.addWidget(self.widget_8, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.cadPage)
        self.defectPage = QWidget()
        self.defectPage.setObjectName(u"defectPage")
        self.horizontalLayout_43 = QHBoxLayout(self.defectPage)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.defectImgQGraView = QGraphicsView(self.defectPage)
        self.defectImgQGraView.setObjectName(u"defectImgQGraView")

        self.horizontalLayout_42.addWidget(self.defectImgQGraView)

        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.label_14 = QLabel(self.defectPage)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setFont(font3)

        self.verticalLayout_26.addWidget(self.label_14)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.label_23 = QLabel(self.defectPage)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font3)

        self.horizontalLayout_38.addWidget(self.label_23)

        self.defectTotalCountLabel = QLabel(self.defectPage)
        self.defectTotalCountLabel.setObjectName(u"defectTotalCountLabel")
        self.defectTotalCountLabel.setFont(font3)
        self.defectTotalCountLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_38.addWidget(self.defectTotalCountLabel)


        self.verticalLayout_26.addLayout(self.horizontalLayout_38)

        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.label_26 = QLabel(self.defectPage)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFont(font3)

        self.horizontalLayout_39.addWidget(self.label_26)

        self.defectChippedCornerLabel = QLabel(self.defectPage)
        self.defectChippedCornerLabel.setObjectName(u"defectChippedCornerLabel")
        self.defectChippedCornerLabel.setFont(font3)
        self.defectChippedCornerLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_39.addWidget(self.defectChippedCornerLabel)


        self.verticalLayout_26.addLayout(self.horizontalLayout_39)

        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.label_27 = QLabel(self.defectPage)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFont(font3)

        self.horizontalLayout_40.addWidget(self.label_27)

        self.defectSurfaceStainLabel = QLabel(self.defectPage)
        self.defectSurfaceStainLabel.setObjectName(u"defectSurfaceStainLabel")
        self.defectSurfaceStainLabel.setFont(font3)
        self.defectSurfaceStainLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_40.addWidget(self.defectSurfaceStainLabel)


        self.verticalLayout_26.addLayout(self.horizontalLayout_40)

        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.label_28 = QLabel(self.defectPage)
        self.label_28.setObjectName(u"label_28")
        self.label_28.setFont(font3)

        self.horizontalLayout_41.addWidget(self.label_28)

        self.defectCrackLabel = QLabel(self.defectPage)
        self.defectCrackLabel.setObjectName(u"defectCrackLabel")
        self.defectCrackLabel.setFont(font3)
        self.defectCrackLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_41.addWidget(self.defectCrackLabel)


        self.verticalLayout_26.addLayout(self.horizontalLayout_41)


        self.horizontalLayout_42.addLayout(self.verticalLayout_26)


        self.horizontalLayout_43.addLayout(self.horizontalLayout_42)

        self.stackedWidget.addWidget(self.defectPage)
        self.settingPage = QWidget()
        self.settingPage.setObjectName(u"settingPage")
        self.verticalLayout_2 = QVBoxLayout(self.settingPage)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.settingPage)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget_4)
        self.label.setObjectName(u"label")
        self.label.setFont(font11)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(884, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toolButton = QToolButton(self.widget_4)
        self.toolButton.setObjectName(u"toolButton")
        sizePolicy1.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy1)
        font16 = QFont()
        font16.setFamily(u"Adobe \u9ed1\u4f53 Std R")
        font16.setPointSize(17)
        self.toolButton.setFont(font16)

        self.horizontalLayout.addWidget(self.toolButton)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 9)
        self.horizontalLayout.setStretch(2, 2)

        self.verticalLayout_2.addWidget(self.widget_4)

        self.widget_5 = QWidget(self.settingPage)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_6 = QWidget(self.widget_5)
        self.widget_6.setObjectName(u"widget_6")
        self.verticalLayout_4 = QVBoxLayout(self.widget_6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.graphicsView_2 = QGraphicsView(self.widget_6)
        self.graphicsView_2.setObjectName(u"graphicsView_2")

        self.verticalLayout_4.addWidget(self.graphicsView_2)

        self.toolButton_2 = QToolButton(self.widget_6)
        self.toolButton_2.setObjectName(u"toolButton_2")
        sizePolicy1.setHeightForWidth(self.toolButton_2.sizePolicy().hasHeightForWidth())
        self.toolButton_2.setSizePolicy(sizePolicy1)
        self.toolButton_2.setFont(font14)

        self.verticalLayout_4.addWidget(self.toolButton_2)

        self.verticalSpacer = QSpacerItem(20, 463, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.verticalLayout_4.setStretch(0, 4)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 9)

        self.horizontalLayout_2.addWidget(self.widget_6)

        self.widget_7 = QWidget(self.widget_5)
        self.widget_7.setObjectName(u"widget_7")
        self.gridLayout_9 = QGridLayout(self.widget_7)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.widget_16 = QWidget(self.widget_7)
        self.widget_16.setObjectName(u"widget_16")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_16)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_11 = QLabel(self.widget_16)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font14)

        self.horizontalLayout_4.addWidget(self.label_11)

        self.pushButton = QPushButton(self.widget_16)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setFont(font14)

        self.horizontalLayout_4.addWidget(self.pushButton)


        self.gridLayout_9.addWidget(self.widget_16, 2, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(589, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_7, 2, 1, 1, 1)

        self.widget_15 = QWidget(self.widget_7)
        self.widget_15.setObjectName(u"widget_15")
        self.gridLayout_8 = QGridLayout(self.widget_15)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_5 = QLabel(self.widget_15)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font15)

        self.gridLayout_8.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_6 = QLabel(self.widget_15)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font15)

        self.gridLayout_8.addWidget(self.label_6, 1, 0, 1, 1)

        self.toolButton_11 = QToolButton(self.widget_15)
        self.toolButton_11.setObjectName(u"toolButton_11")
        sizePolicy1.setHeightForWidth(self.toolButton_11.sizePolicy().hasHeightForWidth())
        self.toolButton_11.setSizePolicy(sizePolicy1)
        self.toolButton_11.setFont(font14)

        self.gridLayout_8.addWidget(self.toolButton_11, 1, 1, 1, 1)

        self.label_7 = QLabel(self.widget_15)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setFont(font15)
        self.gridLayout_8.addWidget(self.label_7, 2, 0, 1, 1)

        self.toolButton_12 = QToolButton(self.widget_15)
        self.toolButton_12.setObjectName(u"toolButton_12")
        sizePolicy1.setHeightForWidth(self.toolButton_12.sizePolicy().hasHeightForWidth())
        self.toolButton_12.setSizePolicy(sizePolicy1)
        self.toolButton_12.setFont(font14)
        self.gridLayout_8.addWidget(self.toolButton_12, 2, 1, 1, 1)

        self.label_8 = QLabel(self.widget_15)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFont(font15)
        self.gridLayout_8.addWidget(self.label_8, 3, 0, 1, 1)

        self.label_9 = QLabel(self.widget_15)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFont(font15)

        self.gridLayout_8.addWidget(self.label_9, 4, 0, 1, 1)

        self.toolButton_14 = QToolButton(self.widget_15)
        self.toolButton_14.setObjectName(u"toolButton_14")
        sizePolicy1.setHeightForWidth(self.toolButton_14.sizePolicy().hasHeightForWidth())
        self.toolButton_14.setSizePolicy(sizePolicy1)
        self.toolButton_14.setFont(font14)

        self.gridLayout_8.addWidget(self.toolButton_14, 4, 1, 1, 1)

        self.label_10 = QLabel(self.widget_15)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font15)

        self.gridLayout_8.addWidget(self.label_10, 5, 0, 1, 1)

        self.toolButton_13 = QToolButton(self.widget_15)
        self.toolButton_13.setObjectName(u"toolButton_13")
        sizePolicy1.setHeightForWidth(self.toolButton_13.sizePolicy().hasHeightForWidth())
        self.toolButton_13.setSizePolicy(sizePolicy1)
        self.toolButton_13.setFont(font14)

        self.gridLayout_8.addWidget(self.toolButton_13, 5, 1, 1, 1)

        self.gridLayout_8.setRowStretch(0, 1)
        self.gridLayout_8.setRowStretch(1, 1)
        self.gridLayout_8.setRowStretch(2, 1)
        self.gridLayout_8.setRowStretch(3, 1)
        self.gridLayout_8.setRowStretch(4, 1)
        self.gridLayout_8.setRowStretch(5, 1)
        self.gridLayout_8.setColumnStretch(0, 5)
        self.gridLayout_8.setColumnStretch(1, 1)

        self.gridLayout_9.addWidget(self.widget_15, 0, 0, 1, 2)

        self.widget_17 = QWidget(self.widget_7)
        self.widget_17.setObjectName(u"widget_17")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_17)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_12 = QLabel(self.widget_17)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setFont(font15)

        self.horizontalLayout_5.addWidget(self.label_12)

        self.pushButton_2 = QPushButton(self.widget_17)
        self.pushButton_2.setObjectName(u"pushButton_2")
        sizePolicy1.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy1)
        self.pushButton_2.setFont(font15)

        self.horizontalLayout_5.addWidget(self.pushButton_2)


        self.gridLayout_9.addWidget(self.widget_17, 1, 0, 1, 1)

        self.gridLayout_9.setRowStretch(0, 5)
        self.gridLayout_9.setRowStretch(1, 1)
        self.gridLayout_9.setRowStretch(2, 1)
        self.gridLayout_9.setColumnStretch(0, 2)
        self.gridLayout_9.setColumnStretch(1, 3)

        self.horizontalLayout_2.addWidget(self.widget_7)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 5)

        self.verticalLayout_2.addWidget(self.widget_5)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 11)
        self.stackedWidget.addWidget(self.settingPage)
        self.UserInfoPage = QWidget()
        self.UserInfoPage.setObjectName(u"UserInfoPage")
        self.horizontalLayout_44 = QHBoxLayout(self.UserInfoPage)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.widget_18 = QWidget(self.UserInfoPage)
        self.widget_18.setObjectName(u"widget_18")
        self.horizontalLayout_47 = QHBoxLayout(self.widget_18)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.widget_25 = QWidget(self.widget_18)
        self.widget_25.setObjectName(u"widget_25")
        self.widget_25.setFont(font)
        self.horizontalLayout_45 = QHBoxLayout(self.widget_25)
        self.horizontalLayout_45.setSpacing(0)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(0, 6, 0, 6)
        self.label_29 = QLabel(self.widget_25)
        self.label_29.setObjectName(u"label_29")
        self.label_29.setFont(font4)
        self.label_29.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_45.addWidget(self.label_29)

        self.horizontalSpacer_16 = QSpacerItem(500, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_45.addItem(self.horizontalSpacer_16)


        self.verticalLayout_27.addWidget(self.widget_25)

        self.widget_40 = QWidget(self.widget_18)
        self.widget_40.setObjectName(u"widget_40")
        self.widget_40.setFont(font)
        self.verticalLayout_28 = QVBoxLayout(self.widget_40)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.widget_44 = QWidget(self.widget_40)
        self.widget_44.setObjectName(u"widget_44")
        self.widget_44.setFont(font)
        self.verticalLayout_29 = QVBoxLayout(self.widget_44)
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.widget_45 = QWidget(self.widget_44)
        self.widget_45.setObjectName(u"widget_45")
        self.widget_45.setMaximumSize(QSize(16777215, 50))
        self.widget_45.setFont(font)
        self.horizontalLayout_46 = QHBoxLayout(self.widget_45)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.horizontalSpacer_18 = QSpacerItem(118, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_46.addItem(self.horizontalSpacer_18)

        self.refreshUserInfoTBtn = QToolButton(self.widget_45)
        self.refreshUserInfoTBtn.setObjectName(u"refreshUserInfoTBtn")
        self.refreshUserInfoTBtn.setFont(font11)

        self.horizontalLayout_46.addWidget(self.refreshUserInfoTBtn)

        self.updateUserInfoTBtn = QToolButton(self.widget_45)
        self.updateUserInfoTBtn.setObjectName(u"updateUserInfoTBtn")
        self.updateUserInfoTBtn.setFont(font11)

        self.horizontalLayout_46.addWidget(self.updateUserInfoTBtn)

        self.deleUserInfoTBtn = QToolButton(self.widget_45)
        self.deleUserInfoTBtn.setObjectName(u"deleUserInfoTBtn")
        self.deleUserInfoTBtn.setFont(font11)

        self.horizontalLayout_46.addWidget(self.deleUserInfoTBtn)


        self.verticalLayout_29.addWidget(self.widget_45)

        self.userInfoTable = QTableWidget(self.widget_44)
        if (self.userInfoTable.columnCount() < 7):
            self.userInfoTable.setColumnCount(7)
        __qtablewidgetitem20 = QTableWidgetItem()
        __qtablewidgetitem20.setFont(font13);
        self.userInfoTable.setHorizontalHeaderItem(0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        __qtablewidgetitem21.setFont(font13);
        self.userInfoTable.setHorizontalHeaderItem(1, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        __qtablewidgetitem22.setFont(font13);
        self.userInfoTable.setHorizontalHeaderItem(2, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        __qtablewidgetitem23.setFont(font13);
        self.userInfoTable.setHorizontalHeaderItem(3, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        __qtablewidgetitem24.setFont(font13);
        self.userInfoTable.setHorizontalHeaderItem(4, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        __qtablewidgetitem25.setFont(font13);
        self.userInfoTable.setHorizontalHeaderItem(5, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        __qtablewidgetitem26.setFont(font13);
        self.userInfoTable.setHorizontalHeaderItem(6, __qtablewidgetitem26)
        if (self.userInfoTable.rowCount() < 20):
            self.userInfoTable.setRowCount(20)
        self.userInfoTable.setObjectName(u"userInfoTable")
        self.userInfoTable.setFont(font11)
        self.userInfoTable.setLayoutDirection(Qt.LeftToRight)
        self.userInfoTable.setAutoFillBackground(False)
        self.userInfoTable.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.userInfoTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.userInfoTable.setSortingEnabled(False)
        self.userInfoTable.setRowCount(20)
        self.userInfoTable.horizontalHeader().setCascadingSectionResizes(False)
        self.userInfoTable.horizontalHeader().setDefaultSectionSize(250)
        self.userInfoTable.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_29.addWidget(self.userInfoTable)


        self.verticalLayout_28.addWidget(self.widget_44)

        self.verticalLayout_28.setStretch(0, 4)

        self.verticalLayout_27.addWidget(self.widget_40)


        self.horizontalLayout_47.addLayout(self.verticalLayout_27)


        self.horizontalLayout_44.addWidget(self.widget_18)

        self.stackedWidget.addWidget(self.UserInfoPage)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)

        self.verticalLayout_14.addWidget(self.stackedWidget)

        self.verticalLayout_14.setStretch(0, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u77f3\u6750\u68c0\u6d4b\u8f6f\u4ef6", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u77f3\u6750\u81ea\u52a8\u5316\u6d41\u6c34\u7ebf\u7cfb\u7edf", None))
        self.homeBtn.setText(QCoreApplication.translate("MainWindow", u"    \u4e3b\u9875    ", None))
        self.cutDataBtn.setText(QCoreApplication.translate("MainWindow", u"\u5207\u5272\u6570\u636e", None))
        self.scanDataBtn.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u6570\u636e", None))
        self.defectDetectBtn.setText(QCoreApplication.translate("MainWindow", u"\u7f3a\u9677\u68c0\u6d4b", None))
        self.cadBtn.setText(QCoreApplication.translate("MainWindow", u"   CAD   ", None))
        self.hardwareCtrlBtn.setText(QCoreApplication.translate("MainWindow", u"\u786c\u4ef6\u63a7\u5236", None))
        self.userCtlBtn.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u4fe1\u606f", None))
        self.settingsBtn.setText(QCoreApplication.translate("MainWindow", u"   \u8bbe\u7f6e    ", None))
        self.closeBtn.setText(QCoreApplication.translate("MainWindow", u"    \u5173\u95ed    ", None))
        self.cuttingMachineLabel.setText(QCoreApplication.translate("MainWindow", u"\u5207\u673a", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"\u77f3\u6750\u5927\u677f\u56fe", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u56fe", None))
        self.edgeProcessingLabel.setText(QCoreApplication.translate("MainWindow", u"\u8fb9\u52a0\u5de5", None))
        self.receivingLabel.setText(QCoreApplication.translate("MainWindow", u"\u6536\u8d27", None))
        self.monitorVideoLabel1.setText(QCoreApplication.translate("MainWindow", u"\u76d1\u63a7\u89c6\u98911", None))
        self.monitorVideoLabel2.setText(QCoreApplication.translate("MainWindow", u"\u76d1\u63a7\u89c6\u98912", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u7387", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u5408\u683c\u7387", None))
        self.completedBtn.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u5b8c\u6210", None))
        self.uncompletedBtn.setText(QCoreApplication.translate("MainWindow", u"\u672a\u5b8c\u6210", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u5207\u5272\u6570\u636e", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u6570\u636e\u5185\u5bb9", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.cutDataQueryTBtn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2\u6570\u636e", None))
        self.dateResetTBtn.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u65e5\u671f", None))
        ___qtablewidgetitem = self.cutDataTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u64cd\u4f5c\u4eba\u5458", None));
        ___qtablewidgetitem1 = self.cutDataTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u6240\u5c5e\u9879\u76ee", None));
        ___qtablewidgetitem2 = self.cutDataTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u957f(mm)", None));
        ___qtablewidgetitem3 = self.cutDataTable.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u5bbd(mm)", None));
        ___qtablewidgetitem4 = self.cutDataTable.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u539a\u5ea6(mm)", None));
        ___qtablewidgetitem5 = self.cutDataTable.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u5207\u5272\u7c73\u6570(m)", None));
        ___qtablewidgetitem6 = self.cutDataTable.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u5927\u677f\u9762\u79ef(m\u00b2)", None));
        ___qtablewidgetitem7 = self.cutDataTable.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u5207\u5272\u72b6\u6001", None));
        ___qtablewidgetitem8 = self.cutDataTable.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u5207\u5272\u65f6\u95f4", None));
        ___qtablewidgetitem9 = self.cutDataTable.horizontalHeaderItem(9)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u53f7", None));
        ___qtablewidgetitem10 = self.cutDataTable.horizontalHeaderItem(10)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"\u7bb1\u53f7", None));
        self.allCtrBox.setTitle(QCoreApplication.translate("MainWindow", u"\u7ffb\u677f\u673a\u3001\u4fa7\u78e8\u673a\u4ee5\u53ca\u5206\u62e3\u673a\u63a7\u5236", None))
        self.connect_all_btn.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8\u8fde\u63a5", None))
        self.disconnect_all_btn.setText(QCoreApplication.translate("MainWindow", u"\u5168\u90e8\u65ad\u5f00", None))
        self.start_qr_monitor_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u76d1\u63a7", None))
        self.stop_qr_monitor.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u76d1\u63a7", None))
        self.flipperCtrBox.setTitle(QCoreApplication.translate("MainWindow", u"\u7ffb\u677f\u673a\u63a7\u5236", None))
        self.connect_flipper_btn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u7ffb\u677f\u673a", None))
        self.disconnect_flipper_btn.setText(QCoreApplication.translate("MainWindow", u"\u65ad\u5f00\u7ffb\u677f\u673a", None))
        self.start_flipper_monitor_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u76d1\u63a7", None))
        self.stop_flipper_monitor_btn.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u76d1\u63a7", None))
        self.edgeGrinderCtrBox.setTitle(QCoreApplication.translate("MainWindow", u"\u4fa7\u78e8\u673a\u63a7\u5236", None))
        self.connect_edge_btn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u4fa7\u78e8\u673a", None))
        self.disconnect_edge_btn.setText(QCoreApplication.translate("MainWindow", u"\u65ad\u5f00\u4fa7\u78e8\u673a", None))
        self.start_edge_monitor_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u76d1\u63a7", None))
        self.stop_edge_monitor_btn.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u76d1\u63a7", None))
        self.sorterCtrBox.setTitle(QCoreApplication.translate("MainWindow", u"\u5206\u62e3\u673a\u63a7\u5236", None))
        self.connect_sorter_btn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u5206\u62e3\u673a", None))
        self.disconnect_sorter_btn.setText(QCoreApplication.translate("MainWindow", u"\u65ad\u5f00\u5206\u62e3\u673a", None))
        self.start_sorter_monitor_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u76d1\u63a7", None))
        self.stop_sorter_monitor_btn.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed\u76d1\u63a7", None))
        self.flipperStateLabel.setText(QCoreApplication.translate("MainWindow", u"\u7ffb\u677f\u673a\uff1a\u672a\u8fde\u63a5", None))
        self.sorterStateLabel.setText(QCoreApplication.translate("MainWindow", u"\u5206\u62e3\u673a\uff1a\u672a\u8fde\u63a5", None))
        self.qrBeforeEdgeStateLabel.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u67aa\uff08\u4fa7\u78e8\u524d\uff09\uff1a\u672a\u8fde\u63a5", None))
        self.qrBeforeSorterStateLabel.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u67aa\uff08\u5206\u62e3\u5904\uff09\uff1a\u672a\u8fde\u63a5", None))
        self.edgeGrinderStateLabel1.setText(QCoreApplication.translate("MainWindow", u"\u4fa7\u78e8\u673a1\u53f7\uff1a\u672a\u8fde\u63a5", None))
        self.edgeGrinderStateLabel2.setText(QCoreApplication.translate("MainWindow", u"\u4fa7\u78e8\u673a2\u53f7\uff1a\u672a\u8fde\u63a5", None))
        self.edgeGrinderStateLabel3.setText(QCoreApplication.translate("MainWindow", u"\u4fa7\u78e8\u673a3\u53f7\uff1a\u672a\u8fde\u63a5", None))
        self.edgeGrinderStateLabel4.setText(QCoreApplication.translate("MainWindow", u"\u4fa7\u78e8\u673a4\u53f7\uff1a\u672a\u8fde\u63a5", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u65e5\u5fd7", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf", None))
        self.scanStartBtn.setText(QCoreApplication.translate("MainWindow", u"\u542f\u52a8\u626b\u63cf", None))
        self.scanViewLargeBtn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u5927\u56fe", None))
        self.scanOriginalBtn.setText(QCoreApplication.translate("MainWindow", u"\u539f\u59cb\u56fe\u7247", None))
        self.scanRulerBtn.setText(QCoreApplication.translate("MainWindow", u"\u91cf\u5c3a\u56fe\u7247", None))
        self.areaStatsTBtn.setText(QCoreApplication.translate("MainWindow", u"\u9762\u79ef\u7edf\u8ba1", None))
        self.countStatsTBtn.setText(QCoreApplication.translate("MainWindow", u"\u7247\u6570\u7edf\u8ba1", None))
        self.scanStatusLabel.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u72b6\u6001\uff1a", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u603b\u5171\u626b\u63cf\uff1a", None))
        self.totalScanLabel.setText("")
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"\u4eca\u65e5\u626b\u63cf\uff1a", None))
        self.todayScanLabel.setText("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.scanQueryBtn.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2\u6570\u636e", None))
        self.scanResetBtn.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u65e5\u671f", None))


        #####----------保留-------------#####
        ___qtablewidgetitem11 = self.scanDataTable.horizontalHeaderItem(0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"\u56fe\u7247", None));
        ___qtablewidgetitem12 = self.scanDataTable.horizontalHeaderItem(1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"\u5355\u53f7", None));
        ___qtablewidgetitem13 = self.scanDataTable.horizontalHeaderItem(2)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u53f7", None));
        ___qtablewidgetitem14 = self.scanDataTable.horizontalHeaderItem(3)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"\u957f", None));
        ___qtablewidgetitem15 = self.scanDataTable.horizontalHeaderItem(4)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"\u5bbd", None));
        ___qtablewidgetitem16 = self.scanDataTable.horizontalHeaderItem(5)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u957f", None));
        ___qtablewidgetitem17 = self.scanDataTable.horizontalHeaderItem(6)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"\u4e8c\u7ef4\u7801\u5bbd", None));
        ___qtablewidgetitem18 = self.scanDataTable.horizontalHeaderItem(7)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u65f6\u95f4", None));

        __sortingEnabled = self.scanDataTable.isSortingEnabled()
        self.scanDataTable.setSortingEnabled(False)
        self.scanDataTable.setSortingEnabled(__sortingEnabled)

        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u65e5\u5fd7", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u77f3\u6750\u5927\u677f\u56fe", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524dCAD\u6587\u4ef6\uff1a", None))
        self.toolButton_7.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u56fe\u7247", None))
        self.toolButton_6.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u5927\u56fe", None))
        self.toolButton_10.setText(QCoreApplication.translate("MainWindow", u"\u66f4\u6539", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u626b\u63cf\u56fe", None))
        self.toolButton_15.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u7f6e\u626b\u63cf\u56fe", None))
        self.toolButton_8.setText(QCoreApplication.translate("MainWindow", u"\u539f\u56fe\u6587\u4ef6\u5939", None))
        self.toolButton_16.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u770b\u5927\u56fe", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u77f3\u6750\u7f3a\u9677\u6570\u636e", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u7f3a\u9677\u603b\u6570\uff1a", None))
        self.defectTotalCountLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\u7f3a\u89d2\uff1a", None))
        self.defectChippedCornerLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\u6c61\u6e0d\uff1a", None))
        self.defectSurfaceStainLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u88c2\u7eb9\uff1a", None))
        self.defectCrackLabel.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.toolButton.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.toolButton_2.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u5f69\u8272\u76f8\u673a\u5f00\u5173", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5173\u95ed", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u9ed1\u767d\u76f8\u673a\u914d\u7f6e", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"vlcf\u6587\u4ef6\uff1a", None))
        self.toolButton_11.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"ini\u6587\u4ef6\uff1a", None))
        self.toolButton_12.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u5f69\u8272\u76f8\u673a\u914d\u7f6e", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"vlcf\u6587\u4ef6\uff1a", None))
        self.toolButton_14.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"ini\u6587\u4ef6\uff1a", None))
        self.toolButton_13.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u91cd\u65b0\u52a0\u8f7d\u914d\u7f6e", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u786e\u8ba4", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u4fe1\u606f", None))
        self.refreshUserInfoTBtn.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u6570\u636e", None))
        self.updateUserInfoTBtn.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u7528\u6237\u6570\u636e", None))
        self.deleUserInfoTBtn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u7528\u6237", None))
        ___qtablewidgetitem19 = self.userInfoTable.horizontalHeaderItem(0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u540d", None));
        ___qtablewidgetitem20 = self.userInfoTable.horizontalHeaderItem(1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"\u4e2d\u6587\u59d3\u540d", None));
        ___qtablewidgetitem21 = self.userInfoTable.horizontalHeaderItem(2)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u5bc6\u7801", None));
        ___qtablewidgetitem22 = self.userInfoTable.horizontalHeaderItem(3)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u6743\u9650", None));
        ___qtablewidgetitem23 = self.userInfoTable.horizontalHeaderItem(4)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"\u6700\u540e\u767b\u5f55\u65f6\u95f4", None));
        ___qtablewidgetitem24 = self.userInfoTable.horizontalHeaderItem(5)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u65f6\u95f4", None));
        ___qtablewidgetitem25 = self.userInfoTable.horizontalHeaderItem(6)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u4fe1\u606f\u65f6\u95f4", None));
    # retranslateUi

