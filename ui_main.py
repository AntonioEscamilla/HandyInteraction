###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    HANDY INTERACTION                                ###
###                        PURPOSE:    WINDOWS/LINUX/MACOS FLAT MODERN UI               ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################

from PyQt5.QtCore import QCoreApplication, QMetaObject, QSize, pyqtSignal, pyqtSlot, Qt, QThread, QEvent
from PyQt5.QtGui import (QFont, QIcon, QPixmap)
from PyQt5.QtWidgets import *
from PyQt5 import QtGui

import mediapipe as mp
import pandas as pd
from tensorflow.keras.models import load_model
import time

from HandPoseEmbedder import *
from HandPoseDraw import *
from KNN_classifier import *

from pythonosc import udp_client
from pythonosc.osc_message_builder import OscMessageBuilder


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 550)
        MainWindow.setMinimumSize(QSize(800, 550))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background:rgb(91,90,90);")
        self.layout_central_widget = QVBoxLayout(self.centralwidget)
        self.layout_central_widget.setSpacing(0)
        self.layout_central_widget.setObjectName(u"layout_central_widget")
        self.layout_central_widget.setContentsMargins(0, 0, 0, 0)

        # -----> Frame superior: Frame Toggle + Frame Window
        self.frame_superior = QFrame(self.centralwidget)
        self.frame_superior.setObjectName(u"frame_superior")
        self.frame_superior.setMaximumSize(QSize(16777215, 55))
        self.frame_superior.setFrameShape(QFrame.NoFrame)
        self.frame_superior.setFrameShadow(QFrame.Plain)
        self.layout_frame_superior = QHBoxLayout(self.frame_superior)
        self.layout_frame_superior.setSpacing(0)
        self.layout_frame_superior.setObjectName(u"layout_frame_superior")
        self.layout_frame_superior.setContentsMargins(0, 0, 0, 0)

        # ---> Frame Toggle: Button Toggle
        self.frame_toggle = QFrame(self.frame_superior)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMinimumSize(QSize(80, 55))
        self.frame_toggle.setMaximumSize(QSize(80, 55))
        self.frame_toggle.setStyleSheet(u"background:rgb(0,143,150);")
        self.frame_toggle.setFrameShape(QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_toggle)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toggle = QPushButton(self.frame_toggle)
        self.toggle.setObjectName(u"toggle")
        self.toggle.setMinimumSize(QSize(80, 55))
        self.toggle.setMaximumSize(QSize(80, 55))
        icon = QIcon()
        icon.addFile(u"icons/1x/logo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.toggle.setIcon(icon)
        self.toggle.setIconSize(QSize(22, 12))
        self.toggle.setFlat(True)
        self.toggle.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(0,178,178);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_3.addWidget(self.toggle)
        self.layout_frame_superior.addWidget(self.frame_toggle)

        # ---> Frame Window: AppName + Min + Max + Close
        self.frame_window = QFrame(self.frame_superior)
        self.frame_window.setObjectName(u"frame_window")
        self.frame_window.setMaximumSize(QSize(16777215, 55))
        self.frame_window.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_window.setFrameShape(QFrame.NoFrame)
        self.frame_window.setFrameShadow(QFrame.Plain)
        self.layout_frame_window = QHBoxLayout(self.frame_window)
        self.layout_frame_window.setSpacing(0)
        self.layout_frame_window.setObjectName(u"layout_frame_window")
        self.layout_frame_window.setContentsMargins(0, 0, 0, 0)
        # -> Frame AppName
        self.frame_appname = QFrame(self.frame_window)
        self.frame_appname.setObjectName(u"frame_appname")
        self.frame_appname.setFrameShape(QFrame.NoFrame)
        self.frame_appname.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_appname)
        self.horizontalLayout_10.setSpacing(7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.appname = QLabel(self.frame_appname)
        self.appname.setObjectName(u"appname")
        font = QFont()
        font.setFamily(u"Segoe UI Light")
        font.setPointSize(24)
        self.appname.setFont(font)
        self.appname.setStyleSheet(u"color:rgb(255,255,255);")
        self.horizontalLayout_10.addWidget(self.appname)
        self.layout_frame_window.addWidget(self.frame_appname)
        # -> Frame Min
        self.frame_min = QFrame(self.frame_window)
        self.frame_min.setObjectName(u"frame_min")
        self.frame_min.setMinimumSize(QSize(55, 55))
        self.frame_min.setMaximumSize(QSize(55, 55))
        self.frame_min.setFrameShape(QFrame.NoFrame)
        self.frame_min.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_min)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.bn_min = QPushButton(self.frame_min)
        self.bn_min.setObjectName(u"bn_min")
        self.bn_min.setMaximumSize(QSize(55, 55))
        icon1 = QIcon()
        icon1.addFile(u"icons/1x/hideAsset 53.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_min.setIcon(icon1)
        self.bn_min.setIconSize(QSize(22, 22))
        self.bn_min.setFlat(True)
        self.bn_min.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(0,143,150);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_7.addWidget(self.bn_min)
        self.layout_frame_window.addWidget(self.frame_min)
        # -> Frame Max
        self.frame_max = QFrame(self.frame_window)
        self.frame_max.setObjectName(u"frame_max")
        self.frame_max.setMinimumSize(QSize(55, 55))
        self.frame_max.setMaximumSize(QSize(55, 55))
        self.frame_max.setFrameShape(QFrame.NoFrame)
        self.frame_max.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_max)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.bn_max = QPushButton(self.frame_max)
        self.bn_max.setObjectName(u"bn_max")
        self.bn_max.setMaximumSize(QSize(55, 55))
        icon2 = QIcon()
        icon2.addFile(u"icons/1x/max.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_max.setIcon(icon2)
        self.bn_max.setIconSize(QSize(22, 22))
        self.bn_max.setFlat(True)
        self.bn_max.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(0,143,150);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_6.addWidget(self.bn_max)
        self.layout_frame_window.addWidget(self.frame_max)
        # -> Frame Close
        self.frame_close = QFrame(self.frame_window)
        self.frame_close.setObjectName(u"frame_close")
        self.frame_close.setMinimumSize(QSize(55, 55))
        self.frame_close.setMaximumSize(QSize(55, 55))
        self.frame_close.setFrameShape(QFrame.NoFrame)
        self.frame_close.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_close)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.bn_close = QPushButton(self.frame_close)
        self.bn_close.setObjectName(u"bn_close")
        self.bn_close.setMaximumSize(QSize(55, 55))
        icon3 = QIcon()
        icon3.addFile(u"icons/1x/closeAsset 43.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_close.setIcon(icon3)
        self.bn_close.setIconSize(QSize(22, 22))
        self.bn_close.setFlat(True)
        self.bn_close.setStyleSheet(u"QPushButton {\n"
                                    "	border: none;\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: rgb(0,143,150);\n"
                                    "}\n"
                                    "QPushButton:pressed {	\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}")
        self.horizontalLayout_5.addWidget(self.bn_close)
        self.layout_frame_window.addWidget(self.frame_close)
        self.layout_frame_superior.addWidget(self.frame_window)
        self.layout_central_widget.addWidget(self.frame_superior)

        # -----> Frame inferior: Frame Izq + Frame Der
        self.frame_inferior = QFrame(self.centralwidget)
        self.frame_inferior.setObjectName(u"frame_inferior")
        self.frame_inferior.setFrameShape(QFrame.NoFrame)
        self.frame_inferior.setFrameShadow(QFrame.Plain)
        self.layout_frame_inferior = QHBoxLayout(self.frame_inferior)
        self.layout_frame_inferior.setSpacing(0)
        self.layout_frame_inferior.setObjectName(u"layout_frame_inferior")
        self.layout_frame_inferior.setContentsMargins(0, 0, 0, 0)

        # ---> Frame Izq: Home + Bug + Cloud + Android + Fixed
        self.frame_izq = QFrame(self.frame_inferior)
        self.frame_izq.setObjectName(u"frame_izq")
        self.frame_izq.setMinimumSize(QSize(80, 0))
        self.frame_izq.setMaximumSize(QSize(80, 16777215))
        self.frame_izq.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_izq.setFrameShape(QFrame.NoFrame)
        self.frame_izq.setFrameShadow(QFrame.Plain)
        self.layout_frame_izq = QVBoxLayout(self.frame_izq)
        self.layout_frame_izq.setSpacing(0)
        self.layout_frame_izq.setObjectName(u"layout_frame_izq")
        self.layout_frame_izq.setContentsMargins(0, 0, 0, 0)
        # -> Frame Home
        self.frame_home = QFrame(self.frame_izq)
        self.frame_home.setObjectName(u"frame_home")
        self.frame_home.setMinimumSize(QSize(80, 55))
        self.frame_home.setMaximumSize(QSize(160, 55))
        self.frame_home.setFrameShape(QFrame.NoFrame)
        self.frame_home.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_home)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.bn_home = QPushButton(self.frame_home)
        self.bn_home.setObjectName(u"bn_home")
        self.bn_home.setMinimumSize(QSize(80, 55))
        self.bn_home.setMaximumSize(QSize(160, 55))
        icon4 = QIcon()
        icon4.addFile(u"icons/1x/peopleAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_home.setIcon(icon4)
        self.bn_home.setIconSize(QSize(30, 30))
        self.bn_home.setFlat(True)
        self.bn_home.setStyleSheet(u"QPushButton {\n"
                                   "	border: none;\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}\n"
                                   "QPushButton:hover {\n"
                                   "	background-color: rgb(91,90,90);\n"
                                   "}\n"
                                   "QPushButton:pressed {	\n"
                                   "	background-color: rgba(0,0,0,0);\n"
                                   "}")
        self.horizontalLayout_15.addWidget(self.bn_home)
        self.layout_frame_izq.addWidget(self.frame_home)
        # -> Frame Bug
        self.frame_bug = QFrame(self.frame_izq)
        self.frame_bug.setObjectName(u"frame_bug")
        self.frame_bug.setMinimumSize(QSize(80, 55))
        self.frame_bug.setMaximumSize(QSize(160, 55))
        self.frame_bug.setFrameShape(QFrame.NoFrame)
        self.frame_bug.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_bug)
        self.horizontalLayout_16.setSpacing(0)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.bn_bug = QPushButton(self.frame_bug)
        self.bn_bug.setObjectName(u"bn_bug")
        self.bn_bug.setMinimumSize(QSize(80, 55))
        self.bn_bug.setMaximumSize(QSize(160, 55))
        icon5 = QIcon()
        icon5.addFile(u"icons/1x/poseAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_bug.setIcon(icon5)
        self.bn_bug.setIconSize(QSize(35, 35))
        self.bn_bug.setFlat(True)
        self.bn_bug.setStyleSheet(u"QPushButton {\n"
                                  "	border: none;\n"
                                  "	background-color: rgba(0,0,0,0);\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "	background-color: rgb(91,90,90);\n"
                                  "}\n"
                                  "QPushButton:pressed {	\n"
                                  "	background-color: rgba(0,0,0,0);\n"
                                  "}")
        self.horizontalLayout_16.addWidget(self.bn_bug)
        self.layout_frame_izq.addWidget(self.frame_bug)
        # -> Frame Cloud
        self.frame_cloud = QFrame(self.frame_izq)
        self.frame_cloud.setObjectName(u"frame_cloud")
        self.frame_cloud.setMinimumSize(QSize(80, 55))
        self.frame_cloud.setMaximumSize(QSize(160, 55))
        self.frame_cloud.setFrameShape(QFrame.NoFrame)
        self.frame_cloud.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_cloud)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.bn_cloud = QPushButton(self.frame_cloud)
        self.bn_cloud.setObjectName(u"bn_cloud")
        self.bn_cloud.setMinimumSize(QSize(80, 55))
        self.bn_cloud.setMaximumSize(QSize(160, 55))
        icon6 = QIcon()
        icon6.addFile(u"icons/1x/gestureAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_cloud.setIcon(icon6)
        self.bn_cloud.setIconSize(QSize(35, 35))
        self.bn_cloud.setFlat(True)
        self.bn_cloud.setStyleSheet(u"QPushButton {\n"
                                    "	border: none;\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "	background-color: rgb(91,90,90);\n"
                                    "}\n"
                                    "QPushButton:pressed {	\n"
                                    "	background-color: rgba(0,0,0,0);\n"
                                    "}")
        self.horizontalLayout_17.addWidget(self.bn_cloud)
        self.layout_frame_izq.addWidget(self.frame_cloud)
        # -> Frame Android
        self.frame_android = QFrame(self.frame_izq)
        self.frame_android.setObjectName(u"frame_android")
        self.frame_android.setMinimumSize(QSize(80, 55))
        self.frame_android.setMaximumSize(QSize(160, 55))
        self.frame_android.setFrameShape(QFrame.NoFrame)
        self.frame_android.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_android)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.bn_android = QPushButton(self.frame_android)
        self.bn_android.setObjectName(u"bn_android")
        self.bn_android.setMinimumSize(QSize(80, 55))
        self.bn_android.setMaximumSize(QSize(160, 55))
        icon7 = QIcon()
        icon7.addFile(u"icons/1x/oscAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_android.setIcon(icon7)
        self.bn_android.setIconSize(QSize(45, 45))
        self.bn_android.setFlat(True)
        self.bn_android.setStyleSheet(u"QPushButton {\n"
                                        "	border: none;\n"
                                        "	background-color: rgba(0,0,0,0);\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "	background-color: rgb(91,90,90);\n"
                                        "}\n"
                                        "QPushButton:pressed {	\n"
                                        "	background-color: rgba(0,0,0,0);\n"
                                        "}")
        self.horizontalLayout_18.addWidget(self.bn_android)
        self.layout_frame_izq.addWidget(self.frame_android)
        # -> Frame Fixed
        self.frame_fixed = QFrame(self.frame_izq)
        self.frame_fixed.setObjectName(u"frame_fixed")
        self.frame_fixed.setFrameShape(QFrame.NoFrame)
        self.frame_fixed.setFrameShadow(QFrame.Plain)
        self.verticalLayout_4 = QVBoxLayout(self.frame_fixed)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.layout_frame_izq.addWidget(self.frame_fixed)
        self.layout_frame_inferior.addWidget(self.frame_izq)

        # ---> Frame Der: Frame Low + Frame Main
        self.frame_der = QFrame(self.frame_inferior)
        self.frame_der.setObjectName(u"frame_der")
        self.frame_der.setFrameShape(QFrame.NoFrame)
        self.frame_der.setFrameShadow(QFrame.Plain)
        self.layout_frame_der = QVBoxLayout(self.frame_der)
        self.layout_frame_der.setSpacing(0)
        self.layout_frame_der.setObjectName(u"layout_frame_der")
        self.layout_frame_der.setContentsMargins(0, 0, 0, 0)
        
        # -> FRAME MAIN: Stacked Widget
        self.frame_main = QFrame(self.frame_der)
        self.frame_main.setObjectName(u"frame")
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Plain)
        self.layout_frame_main = QHBoxLayout(self.frame_main)
        self.layout_frame_main.setSpacing(0)
        self.layout_frame_main.setObjectName(u"layout_frame_main")
        self.layout_frame_main.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame_main)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMinimumSize(QSize(0, 55))
        self.stackedWidget.setStyleSheet(u"")

        # *************** PAGE HOME ******************
        self.page_home = QWidget()
        self.page_home.setObjectName(u"page_home")
        self.page_home.setStyleSheet(u"background:rgb(91,90,90);")
        self.layout_page_home = QHBoxLayout(self.page_home)
        self.layout_page_home.setSpacing(0)
        self.layout_page_home.setObjectName(u"layout_page_home")
        self.layout_page_home.setContentsMargins(0, 5, 0, 5)
        # -> Frame Home Main: Head + Cam + Open/Close/Run
        self.frame_home_main = QFrame(self.page_home)
        self.frame_home_main.setObjectName(u"frame_home_main")
        self.frame_home_main.setFrameShape(QFrame.NoFrame)
        self.frame_home_main.setFrameShadow(QFrame.Plain)
        self.verticalLayout_5 = QVBoxLayout(self.frame_home_main)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.home_main_head = QLabel(self.frame_home_main)
        self.home_main_head.setObjectName(u"home_main_head")
        self.home_main_head.setMinimumSize(QSize(0, 55))
        self.home_main_head.setMaximumSize(QSize(16777215, 55))
        font18 = QFont()
        font18.setFamily(u"Segoe UI Semilight")
        font18.setPointSize(18)
        self.home_main_head.setFont(font18)
        self.home_main_head.setStyleSheet(u"QLabel {\n"
                                        " color:rgb(255,255,255);\n"
                                        "}")
        self.home_main_head.setTextFormat(Qt.RichText)
        self.verticalLayout_5.addWidget(self.home_main_head)
        # -> Cam
        self.home_cam = CamWidget(self.frame_home_main)  # create the label that holds the image
        self.home_cam.setObjectName(u"home_cam")
        # -> Open
        font12 = QFont()
        font12.setFamily(u"Segoe UI")
        font12.setPointSize(12)
        self.home_open_bn = QPushButton(self.frame_home_main)
        self.home_open_bn.setObjectName(u"open_button")
        self.home_open_bn.setMinimumHeight(30)
        self.home_open_bn.setText("Open WebCam")
        self.home_open_bn.setFont(font12)
        self.home_open_bn.setCheckable(False)
        self.home_open_bn.setFlat(True)
        self.home_open_bn.setStyleSheet(u"QPushButton {\n"
                                      "	border: 2px solid rgb(51,51,51);\n"
                                      "	border-radius: 5px;	\n"
                                      "	color:rgb(255,255,255);\n"
                                      "	background-color: rgb(51,51,51);\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "	border: 2px solid rgb(0,143,150);\n"
                                      "	background-color: rgb(0,143,150);\n"
                                      "}\n"
                                      "QPushButton:pressed {	\n"
                                      "	border: 2px solid rgb(0,143,150);\n"
                                      "	background-color: rgb(51,51,51);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:disabled {	\n"
                                      "	border-radius: 5px;	\n"
                                      "	border: 2px solid rgb(112,112,112);\n"
                                      "	background-color: rgb(112,112,112);\n"
                                      "}")
        # -> Close
        self.home_close_bn = QPushButton(self.frame_home_main)  # create close Button
        self.home_close_bn.setText("Close WebCam")
        self.home_close_bn.setObjectName(u"close_button")
        self.home_close_bn.setMinimumHeight(30)
        self.home_close_bn.setFont(font12)
        self.home_close_bn.setCheckable(False)
        self.home_close_bn.setFlat(True)
        self.home_close_bn.setStyleSheet(u"QPushButton {\n"
                                       "	border: 2px solid rgb(51,51,51);\n"
                                       "	border-radius: 5px;	\n"
                                       "	color:rgb(255,255,255);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(0,143,150);\n"
                                       "}\n"
                                       "QPushButton:pressed {	\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:disabled {	\n"
                                       "	border-radius: 5px;	\n"
                                       "	border: 2px solid rgb(112,112,112);\n"
                                       "	background-color: rgb(112,112,112);\n"
                                       "}")
        # -> Run
        self.home_run_bn = QPushButton(self.frame_home_main)  # create inference Button
        self.home_run_bn.setText("Run Model")
        self.home_run_bn.setObjectName(u"close_button")
        self.home_run_bn.setMinimumHeight(30)
        self.home_run_bn.setFont(font12)
        self.home_run_bn.setCheckable(False)
        self.home_run_bn.setFlat(True)
        self.home_run_bn.setStyleSheet(u"QPushButton {\n"
                                           "	border: 2px solid rgb(51,51,51);\n"
                                           "	border-radius: 5px;	\n"
                                           "	color:rgb(255,255,255);\n"
                                           "	background-color: rgb(51,51,51);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "	border: 2px solid rgb(0,143,150);\n"
                                           "	background-color: rgb(0,143,150);\n"
                                           "}\n"
                                           "QPushButton:pressed {	\n"
                                           "	border: 2px solid rgb(0,143,150);\n"
                                           "	background-color: rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QPushButton:disabled {	\n"
                                           "	border-radius: 5px;	\n"
                                           "	border: 2px solid rgb(112,112,112);\n"
                                           "	background-color: rgb(112,112,112);\n"
                                           "}")
        self.h_layout = QHBoxLayout()  # horizontal layout for the 3 Buttons
        self.h_layout.addWidget(self.home_open_bn)
        self.h_layout.addWidget(self.home_close_bn)
        self.h_layout.addWidget(self.home_run_bn)
        self.verticalLayout_5.addWidget(self.home_cam)
        self.verticalLayout_5.addLayout(self.h_layout)
        self.layout_page_home.addWidget(self.frame_home_main)
        # -> Frame Home Division
        self.vert_divide = QFrame(self.page_home)
        self.vert_divide.setObjectName(u"vert_divide")
        self.vert_divide.setFrameShape(QFrame.VLine)
        self.vert_divide.setFrameShadow(QFrame.Sunken)
        self.layout_page_home.addWidget(self.vert_divide)
        # -> Frame Home Stat: Head + Disc
        self.frame_home_stat = QFrame(self.page_home)
        self.frame_home_stat.setObjectName(u"frame_home_stat")
        self.frame_home_stat.setMinimumSize(QSize(220, 0))
        self.frame_home_stat.setMaximumSize(QSize(220, 16777215))
        self.frame_home_stat.setFrameShape(QFrame.NoFrame)
        self.frame_home_stat.setFrameShadow(QFrame.Plain)
        self.verticalLayout_6 = QVBoxLayout(self.frame_home_stat)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.home_stat_hed = QLabel(self.frame_home_stat)
        self.home_stat_hed.setObjectName(u"home_stat_hed")
        self.home_stat_hed.setMinimumSize(QSize(0, 55))
        self.home_stat_hed.setMaximumSize(QSize(16777215, 55))
        self.home_stat_hed.setFont(font18)
        self.home_stat_hed.setStyleSheet(u"QLabel {\n"
                                                " color:rgb(255,255,255);\n"
                                                "}")
        self.home_stat_hed.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.verticalLayout_6.addWidget(self.home_stat_hed)
        # -> ComboBox
        self.model_combo_box = QComboBox(self.frame_home_stat)
        self.model_combo_box.addItem("Hand Landmarks")
        self.model_combo_box.addItem("Hand Center + Size")
        self.model_combo_box.addItem("Scroll Direction")
        self.model_combo_box.addItem("Zoom Direction")
        self.model_combo_box.addItem("Slide Direction")
        self.model_combo_box.addItem("KNN Pose Classifier")
        self.model_combo_box.addItem("Neural Network Pose Classifier")
        self.model_combo_box.addItem("Experimental Gesture Detection")
        self.model_combo_box.setObjectName(u"model_combo_box")
        self.model_combo_box.setMaximumSize(QSize(16777215, 25))
        font11 = QFont()
        font11.setFamily(u"Segoe UI")
        font11.setPointSize(11)
        self.model_combo_box.setFont(font11)
        self.model_combo_box.setStyleSheet(u"QComboBox {\n"
                                        "	border: 2px solid rgb(51,51,51);\n"
                                        "	border-radius: 5px;	\n"
                                        "	color:rgb(255,255,255);\n"
                                        "	background-color: rgb(51,51,51);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox:hover {\n"
                                        "	border: 2px solid rgb(0,143,150);\n"
                                        "	border-radius: 5px;	\n"
                                        "	color:rgb(255,255,255);\n"
                                        "	background-color: rgb(0,143,150);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox:!editable, QComboBox::drop-down:editable {\n"
                                        "	background: rgb(51,51,51);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox:!editable:on, QComboBox::drop-down:editable:on {\n"
                                        "    background:rgb(51,51,51);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox:on { /* shift the text when the popup opens */\n"
                                        "    padding-top: 3px;\n"
                                        "    padding-left: 4px;\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox::drop-down {\n"
                                        "    subcontrol-origin: padding;\n"
                                        "    subcontrol-position: top right;\n"
                                        "    width: 15px;\n"
                                        "\n"
                                        "    border-left-width: 1px;\n"
                                        "    border-left-color: darkgray;\n"
                                        "    border-left-style: solid; /* just a single line */\n"
                                        "    border-top-right-radius: 5px; /* same radius as the QComboBox */\n"
                                        "    border-bottom-right-radius: 5px;\n"
                                        ""
                                        "}\n"
                                        "\n"
                                        "QComboBox::down-arrow {\n"
                                        "    image: url(icons/1x/arrow.png);\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
                                        "    top: 1px;\n"
                                        "    left: 1px;\n"
                                        "}\n"
                                        "\n"
                                        "QComboBox::drop-down {\n"
                                        "    background:rgb(51,51,51);\n"
                                        "}\n"
                                        "\n"
                                        "")
        self.model_combo_box.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.model_combo_box.setFrame(False)
        self.model_combo_box.setModelColumn(0)
        self.verticalLayout_6.addWidget(self.model_combo_box)
        # -> Model Statistics
        self.model_statistics = QLabel(self.frame_home_stat)
        self.model_statistics.setObjectName(u"model_statistics")
        self.model_statistics.setFont(font11)
        self.model_statistics.setStyleSheet(u"QLabel {\n"
                                         " color:rgb(255,255,255);\n"
                                         "}")
        self.model_statistics.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.verticalLayout_6.addWidget(self.model_statistics)
        self.layout_page_home.addWidget(self.frame_home_stat)
        self.stackedWidget.addWidget(self.page_home)

        # *************** PAGE ABOUT HOME ******************
        self.page_about_home = QWidget()
        self.page_about_home.setObjectName(u"page_about_home")
        self.page_about_home.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_13 = QVBoxLayout(self.page_about_home)
        self.verticalLayout_13.setSpacing(5)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(5, 5, 5, 5)
        self.about_home = QLabel(self.page_about_home)
        self.about_home.setObjectName(u"about_home")
        self.about_home.setMinimumSize(QSize(0, 55))
        self.about_home.setMaximumSize(QSize(16777215, 55))
        font3 = QFont()
        font3.setFamily(u"Segoe UI")
        font3.setPointSize(24)
        self.about_home.setFont(font3)
        self.about_home.setStyleSheet(u"color:rgb(255,255,255);")
        self.verticalLayout_13.addWidget(self.about_home)

        self.frame_about_home = QFrame(self.page_about_home)
        self.frame_about_home.setObjectName(u"frame_about_home")
        self.frame_about_home.setFrameShape(QFrame.StyledPanel)
        self.frame_about_home.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.frame_about_home)
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(5, 5, 0, 5)
        self.text_about_home = QTextEdit(self.frame_about_home)
        self.text_about_home.setObjectName(u"text_about_home")
        self.text_about_home.setEnabled(True)
        font10 = QFont()
        font10.setFamily(u"Segoe UI")
        font10.setPointSize(10)
        self.text_about_home.setFont(font10)
        self.text_about_home.setStyleSheet(u"color:rgb(255,255,255);")
        self.text_about_home.setFrameShape(QFrame.NoFrame)
        self.text_about_home.setFrameShadow(QFrame.Plain)
        self.text_about_home.setReadOnly(True)
        self.text_about_home.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.horizontalLayout_28.addWidget(self.text_about_home)

        self.vsb_about_home = QScrollBar(self.frame_about_home)
        self.vsb_about_home.setObjectName(u"vsb_about_home")
        self.vsb_about_home.setStyleSheet(u"QScrollBar:vertical {\n"
                                            "	background:rgb(51,51,51);\n"
                                            "    width:20px;\n"
                                            "    margin: 0px 0px 0px 0px;\n"
                                            "}\n"
                                            "QScrollBar::handle:vertical {\n"
                                            "    background:rgb(0,143,170);\n"
                                            "}\n"
                                            "QScrollBar::add-page:vertical {\n"
                                            " 	background:rgb(51,51,51);\n"
                                            "}\n"
                                            "QScrollBar::sub-page:vertical {\n"
                                            " 	background:rgb(51,51,51);\n"
                                            "}")
        self.vsb_about_home.setOrientation(Qt.Vertical)
        self.horizontalLayout_28.addWidget(self.vsb_about_home)
        self.verticalLayout_13.addWidget(self.frame_about_home)
        self.stackedWidget.addWidget(self.page_about_home)

        # *************** PAGE ABOUT CLOUD ******************
        self.page_about_cloud = QWidget()
        self.page_about_cloud.setObjectName(u"page_about_cloud")
        self.page_about_cloud.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_131 = QVBoxLayout(self.page_about_cloud)
        self.verticalLayout_131.setSpacing(5)
        self.verticalLayout_131.setObjectName(u"verticalLayout_131")
        self.verticalLayout_131.setContentsMargins(5, 5, 5, 5)
        self.about_cloud = QLabel(self.page_about_cloud)
        self.about_cloud.setObjectName(u"about_cloud")
        self.about_cloud.setMinimumSize(QSize(0, 55))
        self.about_cloud.setMaximumSize(QSize(16777215, 55))
        self.about_cloud.setFont(font3)
        self.about_cloud.setStyleSheet(u"color:rgb(255,255,255);")
        self.verticalLayout_131.addWidget(self.about_cloud)

        self.frame_about_cloud = QFrame(self.page_about_cloud)
        self.frame_about_cloud.setObjectName(u"frame_about_home")
        self.frame_about_cloud.setFrameShape(QFrame.StyledPanel)
        self.frame_about_cloud.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_281 = QHBoxLayout(self.frame_about_cloud)
        self.horizontalLayout_281.setSpacing(0)
        self.horizontalLayout_281.setObjectName(u"horizontalLayout_281")
        self.horizontalLayout_281.setContentsMargins(5, 5, 0, 5)
        self.text_about_cloud = QTextEdit(self.frame_about_cloud)
        self.text_about_cloud.setObjectName(u"text_about_cloud")
        self.text_about_cloud.setEnabled(True)
        self.text_about_cloud.setFont(font10)
        self.text_about_cloud.setStyleSheet(u"color:rgb(255,255,255);")
        self.text_about_cloud.setFrameShape(QFrame.NoFrame)
        self.text_about_cloud.setFrameShadow(QFrame.Plain)
        self.text_about_cloud.setReadOnly(True)
        self.text_about_cloud.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.horizontalLayout_281.addWidget(self.text_about_cloud)

        self.vsb_about_cloud = QScrollBar(self.frame_about_cloud)
        self.vsb_about_cloud.setObjectName(u"vsb_about_cloud")
        self.vsb_about_cloud.setStyleSheet(u"QScrollBar:vertical {\n"
                                          "	background:rgb(51,51,51);\n"
                                          "    width:20px;\n"
                                          "    margin: 0px 0px 0px 0px;\n"
                                          "}\n"
                                          "QScrollBar::handle:vertical {\n"
                                          "    background:rgb(0,143,170);\n"
                                          "}\n"
                                          "QScrollBar::add-page:vertical {\n"
                                          " 	background:rgb(51,51,51);\n"
                                          "}\n"
                                          "QScrollBar::sub-page:vertical {\n"
                                          " 	background:rgb(51,51,51);\n"
                                          "}")
        self.vsb_about_cloud.setOrientation(Qt.Vertical)
        self.horizontalLayout_281.addWidget(self.vsb_about_cloud)
        self.verticalLayout_131.addWidget(self.frame_about_cloud)
        self.stackedWidget.addWidget(self.page_about_cloud)

        # *************** PAGE ABOUT ANDROID ******************
        self.page_about_android = QWidget()
        self.page_about_android.setObjectName(u"page_about_android")
        self.page_about_android.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_132 = QVBoxLayout(self.page_about_android)
        self.verticalLayout_132.setSpacing(5)
        self.verticalLayout_132.setObjectName(u"verticalLayout_132")
        self.verticalLayout_132.setContentsMargins(5, 5, 5, 5)
        self.about_android = QLabel(self.page_about_android)
        self.about_android.setObjectName(u"about_android")
        self.about_android.setMinimumSize(QSize(0, 55))
        self.about_android.setMaximumSize(QSize(16777215, 55))
        self.about_android.setFont(font3)
        self.about_android.setStyleSheet(u"color:rgb(255,255,255);")
        self.verticalLayout_132.addWidget(self.about_android)

        self.frame_about_android = QFrame(self.page_about_android)
        self.frame_about_android.setObjectName(u"frame_about_android")
        self.frame_about_android.setFrameShape(QFrame.StyledPanel)
        self.frame_about_android.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_282 = QHBoxLayout(self.frame_about_android)
        self.horizontalLayout_282.setSpacing(0)
        self.horizontalLayout_282.setObjectName(u"horizontalLayout_282")
        self.horizontalLayout_282.setContentsMargins(5, 5, 0, 5)
        self.text_about_android = QTextEdit(self.frame_about_android)
        self.text_about_android.setObjectName(u"text_about_android")
        self.text_about_android.setEnabled(True)
        self.text_about_android.setFont(font10)
        self.text_about_android.setStyleSheet(u"color:rgb(255,255,255);")
        self.text_about_android.setFrameShape(QFrame.NoFrame)
        self.text_about_android.setFrameShadow(QFrame.Plain)
        self.text_about_android.setReadOnly(True)
        self.text_about_android.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.horizontalLayout_282.addWidget(self.text_about_android)

        self.vsb_about_android = QScrollBar(self.frame_about_android)
        self.vsb_about_android.setObjectName(u"vsb_about_android")
        self.vsb_about_android.setStyleSheet(u"QScrollBar:vertical {\n"
                                          "	background:rgb(51,51,51);\n"
                                          "    width:20px;\n"
                                          "    margin: 0px 0px 0px 0px;\n"
                                          "}\n"
                                          "QScrollBar::handle:vertical {\n"
                                          "    background:rgb(0,143,170);\n"
                                          "}\n"
                                          "QScrollBar::add-page:vertical {\n"
                                          " 	background:rgb(51,51,51);\n"
                                          "}\n"
                                          "QScrollBar::sub-page:vertical {\n"
                                          " 	background:rgb(51,51,51);\n"
                                          "}")
        self.vsb_about_android.setOrientation(Qt.Vertical)
        self.horizontalLayout_282.addWidget(self.vsb_about_android)
        self.verticalLayout_132.addWidget(self.frame_about_android)
        self.stackedWidget.addWidget(self.page_about_android)

        # *************** PAGE ABOUT BUG ******************
        self.page_about_bug = QWidget()
        self.page_about_bug.setObjectName(u"page_about_bug")
        self.page_about_bug.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_133 = QVBoxLayout(self.page_about_bug)
        self.verticalLayout_133.setSpacing(5)
        self.verticalLayout_133.setObjectName(u"verticalLayout_133")
        self.verticalLayout_133.setContentsMargins(5, 5, 5, 5)
        self.about_bug = QLabel(self.page_about_bug)
        self.about_bug.setObjectName(u"about_bug")
        self.about_bug.setMinimumSize(QSize(0, 55))
        self.about_bug.setMaximumSize(QSize(16777215, 55))
        self.about_bug.setFont(font3)
        self.about_bug.setStyleSheet(u"color:rgb(255,255,255);")
        self.verticalLayout_133.addWidget(self.about_bug)

        self.frame_about_bug= QFrame(self.page_about_bug)
        self.frame_about_bug.setObjectName(u"frame_about_bug")
        self.frame_about_bug.setFrameShape(QFrame.StyledPanel)
        self.frame_about_bug.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_283 = QHBoxLayout(self.frame_about_bug)
        self.horizontalLayout_283.setSpacing(0)
        self.horizontalLayout_283.setObjectName(u"horizontalLayout_283")
        self.horizontalLayout_283.setContentsMargins(5, 5, 0, 5)
        self.text_about_bug = QTextEdit(self.frame_about_bug)
        self.text_about_bug.setObjectName(u"text_about_bug")
        self.text_about_bug.setEnabled(True)
        self.text_about_bug.setFont(font10)
        self.text_about_bug.setStyleSheet(u"color:rgb(255,255,255);")
        self.text_about_bug.setFrameShape(QFrame.NoFrame)
        self.text_about_bug.setFrameShadow(QFrame.Plain)
        self.text_about_bug.setReadOnly(True)
        self.text_about_bug.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.horizontalLayout_283.addWidget(self.text_about_bug)

        self.vsb_about_bug = QScrollBar(self.frame_about_bug)
        self.vsb_about_bug.setObjectName(u"vsb_about_bug")
        self.vsb_about_bug.setStyleSheet(u"QScrollBar:vertical {\n"
                                             "	background:rgb(51,51,51);\n"
                                             "    width:20px;\n"
                                             "    margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical {\n"
                                             "    background:rgb(0,143,170);\n"
                                             "}\n"
                                             "QScrollBar::add-page:vertical {\n"
                                             " 	background:rgb(51,51,51);\n"
                                             "}\n"
                                             "QScrollBar::sub-page:vertical {\n"
                                             " 	background:rgb(51,51,51);\n"
                                             "}")
        self.vsb_about_bug.setOrientation(Qt.Vertical)
        self.horizontalLayout_283.addWidget(self.vsb_about_bug)
        self.verticalLayout_133.addWidget(self.frame_about_bug)
        self.stackedWidget.addWidget(self.page_about_bug)

        # *************** PAGE BUG ******************
        self.page_bug = QWidget()
        self.page_bug.setObjectName(u"page_bug")
        self.page_bug.setStyleSheet(u"background:rgb(91,90,90);")
        self.layout_page_bug = QHBoxLayout(self.page_bug)
        self.layout_page_bug.setSpacing(0)
        self.layout_page_bug.setObjectName(u"layout_page_bug")
        self.layout_page_bug.setContentsMargins(0, 5, 0, 5)
        self.frame_bug_main = QFrame(self.page_bug)
        self.frame_bug_main.setObjectName(u"frame_bug_main")
        self.frame_bug_main.setFrameShape(QFrame.NoFrame)
        self.frame_bug_main.setFrameShadow(QFrame.Plain)
        self.layout_frame_bug = QVBoxLayout(self.frame_bug_main)
        self.layout_frame_bug.setSpacing(5)
        self.layout_frame_bug.setObjectName(u"layout_frame_bug")
        self.layout_frame_bug.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.bug_head = QLabel(self.frame_bug_main)
        self.bug_head.setObjectName(u"bug_head")
        self.bug_head.setMinimumSize(QSize(0, 55))
        self.bug_head.setMaximumSize(QSize(16777215, 55))
        self.bug_head.setFont(font18)
        self.bug_head.setStyleSheet(u"color:rgb(255,255,255);")
        self.layout_frame_bug.addWidget(self.bug_head)
        # -> Cam
        self.bug_cam = CamRecordWidget(self.frame_bug_main)  # create the label that holds the image
        self.bug_cam.setObjectName(u"home_cam")
        self.layout_frame_bug.addWidget(self.bug_cam)
        # -> Horizontal Layout for LineEdit + 2 Buttons + ProgressBar
        self.h_layout_2 = QHBoxLayout()
        # -> Class Label
        self.class_label = QLabel(self.frame_bug_main)
        self.class_label.setObjectName(u"class_label")
        self.class_label.setMinimumSize(QSize(50, 30))
        self.class_label.setMaximumSize(QSize(50, 30))
        self.class_label.setFont(font12)
        self.class_label.setStyleSheet(u"color:rgb(255,255,255);")
        self.h_layout_2.addWidget(self.class_label)
        # -> Class Line
        self.class_name = QLineEdit(self.frame_bug_main)
        self.class_name.setObjectName(u"class_name")
        self.class_name.setEnabled(True)
        self.class_name.setMinimumSize(QSize(130, 30))
        self.class_name.setMaximumSize(QSize(130, 30))
        self.class_name.setFont(font12)
        self.class_name.setStyleSheet(u"QLineEdit {\n"
                                           "	color:rgb(255,255,255);\n"
                                           "	border:2px solid rgb(51,51,51);\n"
                                           "	border-radius:4px;\n"
                                           "	background:rgb(51,51,51);\n"
                                           "}\n"
                                           "\n"
                                           "QLineEdit:disabled {\n"
                                           "	color:rgb(255,255,255);\n"
                                           "	border:2px solid rgb(112,112,112);\n"
                                           "	border-radius:4px;\n"
                                           "	background:rgb(112,112,112);\n"
                                           "}")
        self.h_layout_2.addWidget(self.class_name)
        # -> Start
        self.bn_bug_start = QPushButton(self.frame_bug_main)
        self.bn_bug_start.setObjectName(u"bn_bug_start")
        self.bn_bug_start.setMinimumSize(QSize(100, 30))
        self.bn_bug_start.setMaximumSize(QSize(100, 30))
        self.bn_bug_start.setFont(font12)
        self.bn_bug_start.setStyleSheet(u"QPushButton {\n"
                                        "	border: 2px solid rgb(51,51,51);\n"
                                        "	border-radius: 5px;	\n"
                                        "	color:rgb(255,255,255);\n"
                                        "	background-color: rgb(51,51,51);\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "	border: 2px solid rgb(0,143,150);\n"
                                        "	background-color: rgb(0,143,150);\n"
                                        "}\n"
                                        "QPushButton:pressed {	\n"
                                        "	border: 2px solid rgb(0,143,150);\n"
                                        "	background-color: rgb(51,51,51);\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:disabled {	\n"
                                        "	border-radius: 5px;	\n"
                                        "	border: 2px solid rgb(112,112,112);\n"
                                        "	background-color: rgb(112,112,112);\n"
                                        "}")
        self.bn_bug_start.setCheckable(False)
        self.bn_bug_start.setFlat(True)
        self.bn_bug_start.setEnabled(False)
        self.h_layout_2.addWidget(self.bn_bug_start)
        # -> Progress Bar
        self.time_bar = ProgressTimer(self.frame_bug_main, time_limit=5.0)
        self.time_bar.setObjectName(u"time_bar")
        self.time_bar.setMinimumSize(QSize(130, 40))
        self.time_bar.setMaximumSize(QSize(130, 40))
        self.h_layout_2.addWidget(self.time_bar)
        # -> Stop
        self.bn_bug_stop = QPushButton(self.frame_bug_main)
        self.bn_bug_stop.setObjectName(u"bn_bug_stop")
        self.bn_bug_stop.setMinimumSize(QSize(100, 30))
        self.bn_bug_stop.setMaximumSize(QSize(100, 30))
        self.bn_bug_stop.setFont(font12)
        self.bn_bug_stop.setStyleSheet(u"QPushButton {\n"
                                       "	border: 2px solid rgb(51,51,51);\n"
                                       "	border-radius: 5px;	\n"
                                       "	color:rgb(255,255,255);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(0,143,150);\n"
                                       "}\n"
                                       "QPushButton:pressed {	\n"
                                       "	border: 2px solid rgb(0,143,150);\n"
                                       "	background-color: rgb(51,51,51);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:disabled {	\n"
                                       "	border-radius: 5px;	\n"
                                       "	border: 2px solid rgb(112,112,112);\n"
                                       "	background-color: rgb(112,112,112);\n"
                                       "}")
        self.bn_bug_stop.setCheckable(False)
        self.bn_bug_stop.setFlat(True)
        self.bn_bug_stop.setEnabled(False)
        self.h_layout_2.addWidget(self.bn_bug_stop)
        # -> Spacer
        self.horizontalSpacer_1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.h_layout_2.addItem(self.horizontalSpacer_1)
        
        self.layout_frame_bug.addLayout(self.h_layout_2)
        self.layout_page_bug.addWidget(self.frame_bug_main)
        self.stackedWidget.addWidget(self.page_bug)

        # *************** PAGE CLOUD ******************
        self.page_cloud = QWidget()
        self.page_cloud.setObjectName(u"page_cloud")
        self.page_cloud.setStyleSheet(u"background:rgb(91,90,90);")
        self.layout_page_cloud = QHBoxLayout(self.page_cloud)
        self.layout_page_cloud.setSpacing(0)
        self.layout_page_cloud.setObjectName(u"layout_page_cloud")
        self.layout_page_cloud.setContentsMargins(0, 5, 0, 5)
        self.frame_cloud_main = QFrame(self.page_cloud)
        self.frame_cloud_main.setObjectName(u"frame_cloud_main")
        self.frame_cloud_main.setFrameShape(QFrame.StyledPanel)
        self.frame_cloud_main.setFrameShadow(QFrame.Raised)
        self.layout_frame_cloud = QVBoxLayout(self.frame_cloud_main)
        self.layout_frame_cloud.setSpacing(5)
        self.layout_frame_cloud.setObjectName(u"layout_frame_cloud")
        self.layout_frame_cloud.setContentsMargins(5, 5, 5, 5)
        # -> Head
        self.cloud_head = QLabel(self.frame_cloud_main)
        self.cloud_head.setObjectName(u"cloud_head")
        self.cloud_head.setMinimumSize(QSize(0, 55))
        self.cloud_head.setMaximumSize(QSize(16777215, 55))
        self.cloud_head.setFont(font18)
        self.cloud_head.setStyleSheet(u"QLabel {\n"
"	color:rgb(255,255,255);\n"
"}")
        self.layout_frame_cloud.addWidget(self.cloud_head)
        # -> Cam
        self.cloud_cam = CamRecordWidget(self.frame_cloud_main)  # create the label that holds the image
        self.cloud_cam.setObjectName(u"cloud_cam")
        self.layout_frame_cloud.addWidget(self.cloud_cam)
        # -> Grid Layout: Label + LineEdit + ProgressBar + 3 Buttons
        self.cloud_grid_layout = QGridLayout(self.frame_cloud_main)
        self.cloud_grid_layout.setObjectName(u"cloud_grid_layout")
        self.cloud_grid_layout.setHorizontalSpacing(5)
        self.cloud_grid_layout.setVerticalSpacing(0)
        self.cloud_grid_layout.setContentsMargins(5, 5, 5, 5)
        # -> Class Label
        self.label_class = QLabel(self.frame_cloud_main)
        self.label_class.setObjectName(u"label_class")
        self.label_class.setMinimumSize(QSize(70, 0))
        self.label_class.setFont(font12)
        self.label_class.setStyleSheet(u"color:rgb(255,255,255);")
        self.cloud_grid_layout.addWidget(self.label_class, 0, 0, 1, 1)
        # -> Class Line
        self.line_class_name = QLineEdit(self.frame_cloud_main)
        self.line_class_name.setObjectName(u"line_class_name")
        self.line_class_name.setEnabled(True)
        self.line_class_name.setMinimumSize(QSize(200, 25))
        self.line_class_name.setMaximumSize(QSize(500, 25))
        self.line_class_name.setFont(font12)
        self.line_class_name.setStyleSheet(u"QLineEdit {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(51,51,51);\n"
"	border-radius:4px;\n"
"	background:rgb(51,51,51);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(112,112,112);\n"
"	border-radius:4px;\n"
"	background:rgb(112,112,112);\n"
"}")
        self.cloud_grid_layout.addWidget(self.line_class_name, 0, 1, 1, 2)
        # -> Add Class Button
        self.bn_add_class = QPushButton(self.frame_cloud_main)
        self.bn_add_class.setObjectName(u"bn_add_class")
        self.bn_add_class.setEnabled(False)
        self.bn_add_class.setMinimumSize(QSize(90, 25))
        self.bn_add_class.setMaximumSize(QSize(90, 25))
        self.bn_add_class.setFont(font12)
        self.bn_add_class.setStyleSheet(u"QPushButton {\n"
                                         "	border: 2px solid rgb(51,51,51);\n"
                                         "	border-radius: 5px;	\n"
                                         "	color:rgb(255,255,255);\n"
                                         "	background-color: rgb(51,51,51);\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "	border: 2px solid rgb(0,143,150);\n"
                                         "	background-color: rgb(0,143,150);\n"
                                         "}\n"
                                         "QPushButton:pressed {	\n"
                                         "	border: 2px solid rgb(0,143,150);\n"
                                         "	background-color: rgb(51,51,51);\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:disabled {	\n"
                                         "	border-radius: 5px;	\n"
                                         "	border: 2px solid rgb(112,112,112);\n"
                                         "	background-color: rgb(112,112,112);\n"
                                         "}")
        self.cloud_grid_layout.addWidget(self.bn_add_class, 0, 3, 1, 1)
        # -> Spacer
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.cloud_grid_layout.addItem(self.horizontalSpacer_2, 0, 4, 1, 1)
        # -> Record Button
        self.bn_cloud_start = QPushButton(self.frame_cloud_main)
        self.bn_cloud_start.setObjectName(u"bn_cloud_start")
        self.bn_cloud_start.setEnabled(False)
        self.bn_cloud_start.setMinimumSize(QSize(90, 25))
        self.bn_cloud_start.setMaximumSize(QSize(90, 25))
        self.bn_cloud_start.setFont(font12)
        self.bn_cloud_start.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(112,0,0);\n"
"	background-color: rgb(112,0,0);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(112,0,0);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")
        self.cloud_grid_layout.addWidget(self.bn_cloud_start, 1, 0, 1, 1)
        # -> Progress Bar
        self.cloud_time_bar = ProgressTimer(self.frame_cloud_main, time_limit=1.0)
        self.cloud_time_bar.setObjectName(u"cloud_time_bar")
        self.cloud_time_bar.setMinimumSize(QSize(150, 40))
        self.cloud_time_bar.setMaximumSize(QSize(150, 40))
        self.cloud_grid_layout.addWidget(self.cloud_time_bar, 1, 1, 1, 1)
        # -> Frames Counter Label
        self.count_frames_label = QLabel(self.frame_cloud_main)
        self.count_frames_label.setObjectName(u"bn_cloud_connect")
        self.count_frames_label.setMinimumSize(QSize(90, 25))
        self.count_frames_label.setMaximumSize(QSize(90, 25))
        self.count_frames_label.setFont(font12)
        self.count_frames_label.setStyleSheet(u"QLabel {\n"
                                      "	color:rgb(255,255,255);\n"
                                      "}")
        self.cloud_grid_layout.addWidget(self.count_frames_label, 1, 2, 1, 1)
        # -> Save Button
        self.bn_cloud_save = QPushButton(self.frame_cloud_main)
        self.bn_cloud_save.setObjectName(u"bn_cloud_save")
        self.bn_cloud_save.setEnabled(False)
        self.bn_cloud_save.setMinimumSize(QSize(90, 25))
        self.bn_cloud_save.setMaximumSize(QSize(90, 25))
        self.bn_cloud_save.setFont(font12)
        self.bn_cloud_save.setStyleSheet(u"QPushButton {\n"
                                          "	border: 2px solid rgb(51,51,51);\n"
                                          "	border-radius: 5px;	\n"
                                          "	color:rgb(255,255,255);\n"
                                          "	background-color: rgb(51,51,51);\n"
                                          "}\n"
                                          "QPushButton:hover {\n"
                                          "	border: 2px solid rgb(0,143,150);\n"
                                          "	background-color: rgb(0,143,150);\n"
                                          "}\n"
                                          "QPushButton:pressed {	\n"
                                          "	border: 2px solid rgb(0,143,150);\n"
                                          "	background-color: rgb(51,51,51);\n"
                                          "}\n"
                                          "\n"
                                          "QPushButton:disabled {	\n"
                                          "	border-radius: 5px;	\n"
                                          "	border: 2px solid rgb(112,112,112);\n"
                                          "	background-color: rgb(112,112,112);\n"
                                          "}")
        self.cloud_grid_layout.addWidget(self.bn_cloud_save, 1, 3, 1, 1)

        self.layout_frame_cloud.addLayout(self.cloud_grid_layout)

        self.layout_page_cloud.addWidget(self.frame_cloud_main)
        self.stackedWidget.addWidget(self.page_cloud)

        # *************** PAGE ANDROID ******************
        self.page_android = QWidget()
        self.page_android.setObjectName(u"page_android")
        self.page_android.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_9 = QVBoxLayout(self.page_android)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_android_menu = QFrame(self.page_android)
        self.frame_android_menu.setObjectName(u"frame_android_menu")
        self.frame_android_menu.setMinimumSize(QSize(0, 30))
        self.frame_android_menu.setMaximumSize(QSize(16777215, 30))
        self.frame_android_menu.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_android_menu.setFrameShape(QFrame.NoFrame)
        self.frame_android_menu.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_android_menu)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)

        self.frame_android_contact = QFrame(self.frame_android_menu)
        self.frame_android_contact.setObjectName(u"frame_android_contact")
        self.frame_android_contact.setMinimumSize(QSize(80, 30))
        self.frame_android_contact.setMaximumSize(QSize(80, 30))
        self.frame_android_contact.setFrameShape(QFrame.NoFrame)
        self.frame_android_contact.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_android_contact)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.bn_android_contact = QPushButton(self.frame_android_contact)
        self.bn_android_contact.setObjectName(u"bn_android_contact")
        self.bn_android_contact.setMinimumSize(QSize(80, 30))
        self.bn_android_contact.setMaximumSize(QSize(80, 30))
        self.bn_android_contact.setStyleSheet(u"QPushButton {\n"
"	border: none;\n"
"	background-color: rgba(0,0,0,0);\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(91,90,90);\n"
"}\n"
"QPushButton:pressed {	\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        icon8 = QIcon()
        icon8.addFile(u"icons/1x/oscLogoAsset.png", QSize(), QIcon.Normal, QIcon.Off)
        self.bn_android_contact.setIcon(icon8)
        self.bn_android_contact.setIconSize(QSize(30, 30))
        self.bn_android_contact.setFlat(True)
        self.horizontalLayout_21.addWidget(self.bn_android_contact)
        self.horizontalLayout_20.addWidget(self.frame_android_contact)

        self.horizontalSpacer_4 = QSpacerItem(397, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_20.addItem(self.horizontalSpacer_4)
        self.verticalLayout_9.addWidget(self.frame_android_menu)

        ##**** ANDROID - CONTACT ****##
        self.stackedWidget_android = QStackedWidget(self.page_android)
        self.stackedWidget_android.setObjectName(u"stackedWidget_android")
        self.stackedWidget_android.setStyleSheet(u"background:rgb(91,90,90);")
        self.page_android_contact = QWidget()
        self.page_android_contact.setObjectName(u"page_android_contact")
        self.page_android_contact.setStyleSheet(u"background:rgb(91,90,90);")
        self.verticalLayout_10 = QVBoxLayout(self.page_android_contact)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(5, 5, 5, 5)
        # -> osc Label
        self.osc_config_label = QLabel(self.page_android_contact)
        self.osc_config_label.setObjectName(u"osc_config_label")
        self.osc_config_label.setMinimumSize(QSize(0, 55))
        self.osc_config_label.setMaximumSize(QSize(16777215, 55))
        self.osc_config_label.setFont(font18)
        self.osc_config_label.setStyleSheet(u"color:rgb(255,255,255);")
        self.verticalLayout_10.addWidget(self.osc_config_label)

        self.frame_android_bottom = QFrame(self.page_android_contact)
        self.frame_android_bottom.setObjectName(u"frame_android_bottom")
        self.frame_android_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_android_bottom.setFrameShadow(QFrame.Plain)
        self.gridLayout_3 = QGridLayout(self.frame_android_bottom)
        self.gridLayout_3.setSpacing(5)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(5, 5, 5, 5)
        # -> Android field: (IP + Port + Path) Labels and LineEdits
        self.frame_android_field = QFrame(self.frame_android_bottom)
        self.frame_android_field.setObjectName(u"frame_android_field")
        self.frame_android_field.setFrameShape(QFrame.NoFrame)
        self.frame_android_field.setFrameShadow(QFrame.Plain)
        self.gridLayout_4 = QGridLayout(self.frame_android_field)
        self.gridLayout_4.setSpacing(5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(5, 5, 5, 5)
        # -> IP Label
        font14 = QFont()
        font14.setFamily(u"Segoe UI")
        font14.setPointSize(14)
        self.label = QLabel(self.frame_android_field)
        self.label.setObjectName(u"label")
        self.label.setFont(font14)
        self.label.setStyleSheet(u"color:rgb(255,255,255);")
        self.gridLayout_4.addWidget(self.label, 1, 0, 1, 3)
        # -> Port Label
        self.label_5 = QLabel(self.frame_android_field)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font14)
        self.label_5.setStyleSheet(u"color:rgb(255,255,255);")
        self.gridLayout_4.addWidget(self.label_5, 3, 0, 1, 3)
        # -> Path Label
        self.label_6 = QLabel(self.frame_android_field)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font14)
        self.label_6.setStyleSheet(u"color:rgb(255,255,255);")
        self.gridLayout_4.addWidget(self.label_6, 4, 0, 1, 1)
        # ->  IP LineEdit
        self.line_android_name = QLineEdit(self.frame_android_field)
        self.line_android_name.setObjectName(u"line_android_name")
        self.line_android_name.setEnabled(False)
        self.line_android_name.setMinimumSize(QSize(300, 25))
        self.line_android_name.setMaximumSize(QSize(400, 25))
        self.line_android_name.setFont(font12)
        self.line_android_name.setStyleSheet(u"QLineEdit {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(51,51,51);\n"
"	border-radius:4px;\n"
"	background:rgb(51,51,51);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(112,112,112);\n"
"	border-radius:4px;\n"
"	background:rgb(112,112,112);\n"
"}")
        self.gridLayout_4.addWidget(self.line_android_name, 1, 3, 1, 1)
        # ->  Port LineEdit
        self.line_android_adress = QLineEdit(self.frame_android_field)
        self.line_android_adress.setObjectName(u"line_android_adress")
        self.line_android_adress.setEnabled(False)
        self.line_android_adress.setMinimumSize(QSize(300, 25))
        self.line_android_adress.setMaximumSize(QSize(400, 25))
        self.line_android_adress.setFont(font12)
        self.line_android_adress.setStyleSheet(u"QLineEdit {\n"
                                               "	color:rgb(255,255,255);\n"
                                               "	border:2px solid rgb(51,51,51);\n"
                                               "	border-radius:4px;\n"
                                               "	background:rgb(51,51,51);\n"
                                               "}\n"
                                               "\n"
                                               "QLineEdit:disabled {\n"
                                               "	color:rgb(255,255,255);\n"
                                               "	border:2px solid rgb(112,112,112);\n"
                                               "	border-radius:4px;\n"
                                               "	background:rgb(112,112,112);\n"
                                               "}")
        self.gridLayout_4.addWidget(self.line_android_adress, 3, 3, 1, 1)
        # ->  Path LineEdit
        self.line_android_org = QLineEdit(self.frame_android_field)
        self.line_android_org.setObjectName(u"line_android_org")
        self.line_android_org.setEnabled(False)
        self.line_android_org.setMinimumSize(QSize(300, 25))
        self.line_android_org.setMaximumSize(QSize(400, 25))
        self.line_android_org.setFont(font12)
        self.line_android_org.setStyleSheet(u"QLineEdit {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(51,51,51);\n"
"	border-radius:4px;\n"
"	background:rgb(51,51,51);\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"	color:rgb(255,255,255);\n"
"	border:2px solid rgb(112,112,112);\n"
"	border-radius:4px;\n"
"	background:rgb(112,112,112);\n"
"}")
        self.gridLayout_4.addWidget(self.line_android_org, 4, 3, 1, 1)
        # -> Spacers
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(self.horizontalSpacer_6, 8, 8, 1, 1)
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.gridLayout_4.addItem(self.horizontalSpacer_5, 4, 8, 1, 1)
        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout_4.addItem(self.verticalSpacer_4, 9, 3, 1, 1)
        # -> Frame: edit + save buttons
        self.frame_3 = QFrame(self.frame_android_field)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_25 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(100, 0, 0, 0)
        # -> edit button
        self.bn_android_contact_edit = QPushButton(self.frame_3)
        self.bn_android_contact_edit.setObjectName(u"bn_android_contact_edit")
        self.bn_android_contact_edit.setMinimumSize(QSize(69, 25))
        self.bn_android_contact_edit.setMaximumSize(QSize(69, 25))
        self.bn_android_contact_edit.setFont(font12)
        self.bn_android_contact_edit.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")
        self.horizontalLayout_25.addWidget(self.bn_android_contact_edit)
        # -> save button
        self.bn_android_contact_save = QPushButton(self.frame_3)
        self.bn_android_contact_save.setObjectName(u"bn_android_contact_save")
        self.bn_android_contact_save.setEnabled(False)
        self.bn_android_contact_save.setMinimumSize(QSize(69, 25))
        self.bn_android_contact_save.setMaximumSize(QSize(69, 25))
        self.bn_android_contact_save.setFont(font12)
        self.bn_android_contact_save.setStyleSheet(u"QPushButton {\n"
"	border: 2px solid rgb(51,51,51);\n"
"	border-radius: 5px;	\n"
"	color:rgb(255,255,255);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"QPushButton:hover {\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(0,143,150);\n"
"}\n"
"QPushButton:pressed {	\n"
"	border: 2px solid rgb(0,143,150);\n"
"	background-color: rgb(51,51,51);\n"
"}\n"
"\n"
"QPushButton:disabled {	\n"
"	border-radius: 5px;	\n"
"	border: 2px solid rgb(112,112,112);\n"
"	background-color: rgb(112,112,112);\n"
"}")
        self.horizontalLayout_25.addWidget(self.bn_android_contact_save)

        self.gridLayout_4.addWidget(self.frame_3, 8, 0, 1, 7)
        self.gridLayout_3.addWidget(self.frame_android_field, 0, 0, 2, 1)
        self.verticalLayout_10.addWidget(self.frame_android_bottom)
        self.stackedWidget_android.addWidget(self.page_android_contact)
        self.verticalLayout_9.addWidget(self.stackedWidget_android)

        self.stackedWidget.addWidget(self.page_android)
        self.layout_frame_main.addWidget(self.stackedWidget)
        self.layout_frame_der.addWidget(self.frame_main)


        # *************** LOWER FRAME ******************
        self.frame_low = QFrame(self.frame_der)
        self.frame_low.setObjectName(u"frame_low")
        self.frame_low.setMinimumSize(QSize(0, 20))
        self.frame_low.setMaximumSize(QSize(16777215, 20))
        self.frame_low.setStyleSheet(u"")
        self.frame_low.setFrameShape(QFrame.NoFrame)
        self.frame_low.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_low)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.frame_tab = QFrame(self.frame_low)
        self.frame_tab.setObjectName(u"frame_tab")
        font10 = QFont()
        font10.setFamily(u"Segoe UI")
        self.frame_tab.setFont(font10)
        self.frame_tab.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_tab.setFrameShape(QFrame.NoFrame)
        self.frame_tab.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_tab)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.tab = QLabel(self.frame_tab)
        self.tab.setObjectName(u"tab")
        font10 = QFont()
        font10.setFamily(u"Segoe UI Light")
        font10.setPointSize(10)
        self.tab.setFont(font10)
        self.tab.setStyleSheet(u"color:rgb(255,255,255);")

        self.horizontalLayout_12.addWidget(self.tab)
        self.horizontalLayout_11.addWidget(self.frame_tab)

        self.frame_drag = QFrame(self.frame_low)
        self.frame_drag.setObjectName(u"frame_drag")
        self.frame_drag.setMinimumSize(QSize(20, 20))
        self.frame_drag.setMaximumSize(QSize(20, 20))
        self.frame_drag.setStyleSheet(u"background:rgb(51,51,51);")
        self.frame_drag.setFrameShape(QFrame.NoFrame)
        self.frame_drag.setFrameShadow(QFrame.Plain)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_drag)
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_11.addWidget(self.frame_drag)

        self.layout_frame_der.addWidget(self.frame_low)
        self.layout_frame_inferior.addWidget(self.frame_der)
        self.layout_central_widget.addWidget(self.frame_inferior)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(7)
        self.stackedWidget_android.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toggle.setText("")
        self.appname.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))

        self.bn_min.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
        self.bn_min.setText("")
        self.bn_max.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
        self.bn_max.setText("")
        self.bn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
        self.bn_close.setText("")
        self.bn_home.setToolTip(QCoreApplication.translate("MainWindow", u"Run Model", None))
        self.bn_home.setText("")
        self.bn_bug.setToolTip(QCoreApplication.translate("MainWindow", u"Pose Recording", None))
        self.bn_bug.setText("")
        self.bn_cloud.setToolTip(QCoreApplication.translate("MainWindow", u"Gesture Recording", None))
        self.bn_cloud.setText("")
        self.bn_android.setToolTip(QCoreApplication.translate("MainWindow", u"OSC Settings", None))
        self.bn_android.setText("")
        self.home_main_head.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Capture from webcam</span></p></body></html>", None))
        self.home_stat_hed.setText(QCoreApplication.translate("MainWindow", u"Select Model", None))
        #self.model_statistics.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Weather: Rainy<br/>Skys: Cloudy<br/>Wind: blowing Fast<br/>Temperature: 32 Degree Celcious</span></p></body></html>", None))
        self.about_home.setText(QCoreApplication.translate("MainWindow", u"About: Run Model", None))
        self.about_bug.setText(QCoreApplication.translate("MainWindow", u"About: Pose Recording", None))
        self.about_cloud.setText(QCoreApplication.translate("MainWindow", u"About: Gesture Recording", None))
        self.about_android.setText(QCoreApplication.translate("MainWindow", u"About: Osc Settings", None))
        self.bug_head.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" color:#ffffff;\">Gather Pose Data for Training</span></p></body></html>", None))
        self.class_label.setText(QCoreApplication.translate("MainWindow", u"Class :", None))

        self.bn_bug_start.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.bn_bug_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.cloud_head.setText(QCoreApplication.translate("MainWindow", u"Gather Gesture Data for Training", None))
        self.label_class.setText(QCoreApplication.translate("MainWindow", u"Class :", None))
        self.bn_cloud_start.setText(QCoreApplication.translate("MainWindow", u"Record", None))
        self.bn_cloud_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.bn_add_class.setText(QCoreApplication.translate("MainWindow", u"Add Class", None))

        self.count_frames_label.setText(QCoreApplication.translate("MainWindow", u"Frames: ", None))
        self.bn_android_contact.setToolTip(QCoreApplication.translate("MainWindow", u"Contact", None))
        self.bn_android_contact.setText("")

        self.osc_config_label.setText(QCoreApplication.translate("MainWindow", u"OSC Configuration", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Path:", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"IP Address: ", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Port: ", None))
        self.line_android_name.setText(QCoreApplication.translate("MainWindow", u"127.0.0.1", None))
        self.line_android_org.setText(QCoreApplication.translate("MainWindow", u"/handy/", None))
        self.line_android_adress.setText(QCoreApplication.translate("MainWindow", u"7500", None))
        self.bn_android_contact_edit.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.bn_android_contact_save.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.tab.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><br/></p></body></html>", None))
        self.frame_drag.setToolTip(QCoreApplication.translate("MainWindow", u"Drag", None))
    # retranslateUi


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    #clear_pixmap_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # capture from web cam
        while self.run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()  # shut down capture system

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        #self.clear_pixmap_signal.emit(True)
        self.run_flag = False
        self.wait()


class CamWidget(QWidget):
    frame_counter_signal = pyqtSignal(bool)
    update_stats_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super(CamWidget, self).__init__(parent)
        self.main_state = 0

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)

        self.pose_embedder = HandPoseEmbedder()
        self.pose_drawer = HandPoseDraw()
        self.load_knn_model(self.pose_embedder)

        self.ip = '127.0.0.1'
        self.port = 7500
        self.root_address = '/handy'
        self.client = udp_client.SimpleUDPClient(self.ip, self.port)

        self.frame_counter = 0
        self.model_index = 0
        self.model_features = {}

        self.pose_classifier = load_model('./models/handpose_classifier/saved_model', compile=False)
        self.class_names = ['open', 'fist', 'peace', 'ok']

        self.gesture_detector = load_model('./models/handgesture_detection_v3/saved_model', compile=False)
        self.gesture_class_names = ['grab', 'turn-right', 'hand_tap', 'fingers_tap', 'open_hand', 'close_hand']
        self.gesture = np.zeros((10, 63))

        self.imageLabel = QLabel(self)  # create the label that holds the image
        self.main_layout = QVBoxLayout()  # create vertical box layout and add label + buttons
        self.main_layout.addWidget(self.imageLabel)
        self.setLayout(self.main_layout)  # set the vbox layout as the widgets layout

        self.thread = VideoThread()  # create the video capture thread
        self.thread.change_pixmap_signal.connect(self.UpdateImage)

    @pyqtSlot(np.ndarray)
    def UpdateImage(self, cv_img):
        cv_img = cv2.flip(cv_img, 1)
        cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        if self.main_state >= 1:
            cv_img = self.runModel(cv_img)
        qt_img = self.toQPix(cv_img)
        self.imageLabel.setPixmap(qt_img)
        if not self.thread.run_flag:
            self.imageLabel.clear()
            self.imageLabel.repaint()

    def toQPix(self, rgb_image):
        """Convert from an opencv image to QPixmap"""
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_qt.scaled(self.size().width(), self.size().height(), Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def runModel(self, frame):
        image = np.copy(frame)

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        results = self.hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks, start=1):
                if self.model_index == 0:
                    self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    landmarks = HandPoseEmbedder.get_landmarks_list(hand_landmarks.landmark)
                    self.send_hand_detection(self.client, self.root_address+"/keypoints", hand_idx, landmarks)

                elif self.model_index == 1:
                    self.model_features = self.pose_embedder.get_center_and_size(hand_landmarks.landmark)
                    center = [self.model_features['Hand center x'], self.model_features['Hand center y']]
                    self.pose_drawer.draw_center_point(image, center, self.model_features['Hand size'])
                    self.update_stats_signal.emit(True)
                    self.send_hand_detection(self.client, self.root_address+"/center_size", hand_idx, self.model_features)

                elif self.model_index == 2:
                    self.model_features = self.pose_embedder.scroll_direction(hand_landmarks.landmark)
                    if self.model_features['Hand state'] is not None:
                        self.update_stats_signal.emit(True)
                        self.send_hand_detection(self.client, self.root_address+"/scroll", hand_idx, self.model_features)

                elif self.model_index == 3:
                    self.model_features = self.pose_embedder.zoom_direction(hand_landmarks.landmark)
                    if self.model_features['Hand state'] is not None:
                        self.update_stats_signal.emit(True)
                        self.send_hand_detection(self.client, self.root_address+"/zoom", hand_idx, self.model_features)

                elif self.model_index == 4:
                    self.model_features = self.pose_embedder.slide_direction(hand_landmarks.landmark)
                    if self.model_features['Hand state'] is not None:
                        self.update_stats_signal.emit(True)
                        self.send_hand_detection(self.client, self.root_address+"/slide", hand_idx, self.model_features)

                elif self.model_index == 5:
                    landmarks = HandPoseEmbedder.get_landmarks_2dArray(hand_landmarks.landmark)
                    self.model_features = self.knn_model_predict(landmarks)
                    self.update_stats_signal.emit(True)
                    self.send_hand_detection(self.client, self.root_address+"/knn_classifier", hand_idx, self.model_features)

                elif self.model_index == 6:
                    landmarks = HandPoseEmbedder.get_landmarks_array(hand_landmarks.landmark)
                    pose_probability = np.round(self.pose_classifier.predict(landmarks).astype('float64') * 10, 3)[0]
                    self.model_features = {'open': pose_probability[0], 'fist': pose_probability[1], 'peace': pose_probability[2], 'ok': pose_probability[3]}
                    self.update_stats_signal.emit(True)
                    self.send_hand_detection(self.client, self.root_address+"/dnn_classifier", hand_idx, self.model_features)

                elif self.model_index == 7:
                    if self.frame_counter == 10:
                        print('gesture!!')
                        self.frame_counter = 0
                        self.gesture = np.expand_dims(self.gesture, axis=0)
                        gesture_probability = self.gesture_detector.predict(self.gesture)
                        idx_class = np.argmax(gesture_probability)
                        if np.max(gesture_probability) > 0.99 and idx_class < 4:
                            print('predicted class: {}, with propability {}%'.format(self.gesture_class_names[idx_class], np.max(gesture_probability)*100))
                    else:
                        self.gesture = self.record_gesture(hand_landmarks.landmark, self.gesture, self.frame_counter, gesture_size=(10, 63))
                        self.frame_counter_signal.emit(True)

                # if self.run_gesture_detector:
                #     self.short_gesture = gtr.add_pose_to_gesture(hand_landmarks.landmark, self.short_gesture)
                #     gesture_probability = self.gesture_detector.predict(self.short_gesture)
                #     idx_class = np.argmax(gesture_probability)
                #     if np.max(gesture_probability) > 0.7:
                #         print('predicted class: {}'.format(self.class_names[idx_class]))


        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def load_knn_model(self, pose_embedder):
        pose_samples_folder = './models/knn_classifier/handpose_data'

        # Initialize classifier.
        self.knn_classifier = PoseClassifier(pose_samples_folder, pose_embedder)

        # Initialize EMA smoothing.
        self.knn_classification_filter = EMADictSmoothing(window_size=10, alpha=0.2)

    def knn_model_predict(self, landmarks):
        pose_classification = self.knn_classifier(landmarks)
        filtered = self.knn_classification_filter(pose_classification)
        classification_results = {k: np.round(v, 2) for (k, v) in filtered.items()}
        return classification_results

    def record_gesture(self, landmark, gesture, frame_counter, gesture_size=(45, 21, 3)):
        if frame_counter == 0:
            gesture = np.zeros(gesture_size)                        # gesture shape (size[0], size[1], size[2])

        landmark = HandPoseEmbedder.get_landmarks_2dArray(landmark)                         # landmark shape (21, 3)
        if len(gesture_size) == 2:
            gesture[frame_counter] = self.pose_embedder.normalize_pose_landmarks(landmark).reshape((1, 63))
        elif len(gesture_size) == 3:
            if gesture_size[2] == 2:
                landmark = landmark[:, :2]
            gesture[frame_counter] = self.pose_embedder.normalize_pose_landmarks(landmark)

        return gesture

    @staticmethod
    def send_hand_detection(udp_client, address, hand_idx, detections):

        if type(detections) == dict:
            detect_list = [len(detections)]
            for i in detections:
                detect_list.append(i)
                detect_list.append(detections[i])
            detections = detect_list

        # create message and send
        builder = OscMessageBuilder(address)
        builder.add_arg(hand_idx)
        for feature in detections:
            builder.add_arg(feature)
        msg = builder.build()
        udp_client.send(msg)

    @staticmethod
    def add_pose_to_gesture(landmark, gesture):
        gesture[0][:-1, :, :] = gesture[0][1:, :, :]
        gesture[0][-1] = HandPoseEmbedder.get_xy_landmarks_2dArray(landmark)
        return gesture


class CamRecordWidget(CamWidget):
    counter_ended_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.main_state = 0
        self.df = pd.DataFrame()
        self.gesture = np.zeros((45, 21, 3))
        self.frame_counter = 0
        self.features_dataset = []
        self.labels_dataset = []
        self.class_names = {}

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)

        self.pose_embedder = HandPoseEmbedder()

        self.imageLabel = QLabel(self)  # create the label that holds the image
        self.main_layout = QVBoxLayout()  # create vertical box layout and add label + buttons
        self.main_layout.addWidget(self.imageLabel)
        self.setLayout(self.main_layout)  # set the vbox layout as the widgets layout

        self.thread = VideoThread()  # create the video capture thread
        self.thread.change_pixmap_signal.connect(self.UpdateImage)

    def runModel(self, frame):
        image = np.copy(frame)

        # To improve performance, optionally mark the image as not writeable to pass by reference.
        image.flags.writeable = False
        results = self.hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                if self.main_state == 2:
                    self.df = pd.DataFrame(columns=np.arange(21 * 3))
                    self.main_state = 3

                elif self.main_state == 3:
                    self.df.loc[len(self.df)] = HandPoseEmbedder.get_landmarks_list(hand_landmarks.landmark)

                elif self.main_state == 4:
                    if self.frame_counter == 45:
                        self.frame_counter = 0
                        self.features_dataset.append(self.gesture)
                        self.labels_dataset.append(len(self.class_names) - 1)
                        self.counter_ended_signal.emit(True)
                    else:
                        self.gesture = self.record_gesture(hand_landmarks.landmark, self.gesture, self.frame_counter, gesture_size=(45, 21, 3))
                        self.frame_counter_signal.emit(True)

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image


class TimerThread(QThread):
    countChanged = pyqtSignal(float)

    def __init__(self, time_limit):
        super().__init__()
        self.TIME_LIMIT = time_limit

    def run(self):
        count = 0
        while count < self.TIME_LIMIT:
            count += 0.01
            time.sleep(0.01)
            self.countChanged.emit(count)


class ProgressTimer(QWidget):
    timerEnded = pyqtSignal(bool)

    def __init__(self, parent, time_limit):
        super(ProgressTimer, self).__init__(parent)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setObjectName(u"progress_bar")
        self.progress_bar.setEnabled(True)
        self.progress_bar.setStyleSheet(u"QProgressBar\n"
                                           "{\n"
                                           "	color:rgb(255,255,255);\n"
                                           "	background-color :rgb(51,51,51);\n"
                                           "	border : 2px;\n"
                                           "	border-radius:4px;\n"
                                           "}\n"
                                           "\n"
                                           "QProgressBar::chunk{\n"
                                           "	border : 2px;\n"
                                           "	border-radius:4px;\n"
                                           "	background-color:rgb(0,143,150);\n"
                                           "}")
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setOrientation(Qt.Horizontal)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setTextDirection(QProgressBar.TopToBottom)

        self.TIME_LIMIT = time_limit

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.progress_bar)
        self.setLayout(self.main_layout)  # set the vbox layout as the widgets layout

        self.thread = TimerThread(self.TIME_LIMIT)
        self.thread.countChanged.connect(self.onCountChanged)

    def onCountChanged(self, value):
        self.progress_bar.setValue(value*100.0/self.TIME_LIMIT)
        if value >= self.TIME_LIMIT:
            self.timerEnded.emit(True)
