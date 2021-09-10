###########################################################################################
###                        CODE:       WRITTEN BY: ANTONIO ESCAMILLA                    ###
###                        PROJECT:    HANDY INTERACTION                                ###
###                        PURPOSE:    WINDOWS/LINUX/MACOS FLAT MODERN UI               ###
###                                    BASED ON QT DESIGNER                             ###
###                        LICENCE:    MIT OPENSOURCE LICENCE                           ###
###                                                                                     ###
###                            CODE IS FREE TO USE AND MODIFY                           ###
###########################################################################################
import numpy as np
from about import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QTimer, QEasingCurve, QPropertyAnimation, Qt, QEvent
from pythonosc import udp_client

GLOBAL_STATE = 0  # NECESSARY FOR CHECKING WEATHER THE WINDOW IS FULL SCREEN OR NOT
GLOBAL_TITLE_BAR = True  # NECESSARY FOR CHECKING WEATHER THE WINDOW IS FULL SCREEN OR NOT
init = False  # NECESSARY FOR INITIATION OF THE WINDOW.


# THIS CLASS HOUSES ALL FUNCTION NECESSARY FOR OUR PROGRAMME TO RUN.
class UIFunction:

    # ----> INITIAL FUNCTION TO LOAD THE FRONT STACK WIDGET AND TAB BUTTON I.E. HOME PAGE
    # INITIALISING THE WELCOME PAGE TO: HOME PAGE IN THE STACKEDWIDGET, SETTING THE BOTTOM LABEL AS THE PAGE NAME, SETTING THE BUTTON STYLE.
    def initStackTab(self):
        global init
        if not init:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
            self.ui.tab.setText("Home")
            self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            init = True

    ################################################################################################

    # ------> SETTING THE APPLICATION NAME IN OUR CUSTOM MADE TAB, WHERE LABEL NAMED: appname()
    def labelTitle(self, appName):
        self.ui.appname.setText(appName)

    ################################################################################################

    # ----> MAXIMISE/RESTORE FUNCTION
    # THIS FUNCTION MAXIMISES OUR MAIN WINDOW WHEN THE MAXIMISE BUTTON IS PRESSED OR IF DOUBLE MOUSE LEFT PRESS IS DOES OVER THE TOP FRAME.
    # THIS MAKE THE APPLICATION TO OCCUPY THE WHOLE MONITOR.
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.bn_max.setToolTip("Restore")
            self.ui.bn_max.setIcon(QIcon("icons/1x/restore.png"))  # CHANGE THE MAXIMISE ICON TO RESTORE ICON
            self.ui.frame_drag.hide()  # HIDE DRAG AS NOT NECESSARY
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.bn_max.setToolTip("Maximize")
            self.ui.bn_max.setIcon(QIcon("icons/1x/max.png"))  # CHANGE BACK TO MAXIMISE ICON
            self.ui.frame_drag.show()

    ################################################################################################

    # ----> RETURN STATUS MAX OR RESTORE
    # NECESSARY FOR THE MAXIMISE FUNCTION TO WORK.
    @staticmethod
    def returnStatus():
        return GLOBAL_STATE

    @staticmethod
    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # ------> TOGGLE MENU FUNCTION
    # THIS FUNCTION TOGGLES THE MENU BAR TO DOUBLE THE LENGTH OPENING A NEW ARE OF ABOUT TAB IN FRONT.
    # ALSO IT SETS THE ABOUT>HOME AS THE FIRST PAGE.
    # IF THE PAGE IS IN THE ABOUT PAGE THEN PRESSING AGAIN WILL RESULT IN UNDOING THE PROCESS AND COMING BACK TO THE
    # HOME PAGE.
    def toggleMenu(self, maxWidth, clicked):

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS : I.E. MAKING THEN NORMAL COLOR THAN LIGHTER COLOR.
        for each in self.ui.frame_izq.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if clicked:
            currentWidth = self.ui.frame_izq.width()  # Reads the current width of the frame
            minWidth = 80  # MINIMUM WIDTH OF THE BOTTOM_WEST FRAME
            if currentWidth == 80:
                extend = maxWidth
                # ----> MAKE THE STACKED WIDGET PAGE TO ABOUT HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.tab.setText("About > Run Model")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            else:
                extend = minWidth
                # -----> REVERT THE ABOUT HOME PAGE TO NORMAL HOME PAGE
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.tab.setText("Run Model")
                self.ui.frame_home.setStyleSheet("background:rgb(91,90,90)")
            # THIS ANIMATION IS RESPONSIBLE FOR THE TOGGLE TO MOVE IN A SOME FIXED STATE.
            self.animation = QPropertyAnimation(self.ui.frame_izq, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(minWidth)
            self.animation.setEndValue(extend)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    ################################################################################################

    # -----> DEFAULT ACTION FUNCTION
    def constantFunction(self):
        # -----> DOUBLE CLICK RESULT IN MAXIMISE OF WINDOW
        def maxDoubleClick(stateMouse):
            if stateMouse.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunction.maximize_restore(self))

        # ----> REMOVE NORMAL TITLE BAR
        if True:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.ui.frame_appname.mouseDoubleClickEvent = maxDoubleClick
        else:
            self.ui.frame_close.hide()
            self.ui.frame_max.hide()
            self.ui.frame_min.hide()
            self.ui.frame_drag.hide()

        # -----> RESIZE USING DRAG                                       THIS CODE TO DRAG AND RESIZE IS IN PROTOTYPE.
        # self.sizegrip = QSizeGrip(self.ui.frame_drag)
        # self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        # SINCE THERE IS NO WINDOWS TOP BAR, THE CLOSE MIN, MAX BUTTON ARE ABSENT AND SO THERE IS A NEED FOR THE ALTERNATIVE BUTTONS IN OUR
        # DIALOG BOX, WHICH IS CARRIED OUT BY THE BELOW CODE
        # -----> MINIMIZE BUTTON FUNCTION
        self.ui.bn_min.clicked.connect(lambda: self.showMinimized())

        # -----> MAXIMIZE/RESTORE BUTTON FUNCTION
        self.ui.bn_max.clicked.connect(lambda: UIFunction.maximize_restore(self))

        # -----> CLOSE APPLICATION FUNCTION BUTTON
        self.ui.bn_close.clicked.connect(lambda: APFunction.custom_close(self))

    # ----> BUTTON IN TAB PRESSED EXECUTES THE CORRESPONDING PAGE IN STACKED WIDGET PAGES
    def buttonPressed(self, buttonName):

        index = self.ui.stackedWidget.currentIndex()

        # ------> THIS LINE CLEARS THE BG OF PREVIOUS TABS I.E. FROM THE LITER COLOR TO THE SAME BG COLOR I.E. TO CHANGE THE HIGHLIGHT.
        for each in self.ui.frame_izq.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if buttonName == 'bn_home':
            if self.ui.frame_izq.width() == 80 and index != 0:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
                self.ui.tab.setText("Run Model")
                self.ui.frame_home.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_izq.width() == 160 and index != 1:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_home)
                self.ui.tab.setText("About > Run Model")
                self.ui.frame_home.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_bug':
            if self.ui.frame_izq.width() == 80 and index != 5:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_bug)
                self.ui.tab.setText("Pose Recording")
                self.ui.frame_bug.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_izq.width() == 160 and index != 4:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_bug)
                self.ui.tab.setText("About > Pose Recording")
                self.ui.frame_bug.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_android':
            if self.ui.frame_izq.width() == 80 and index != 7:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_android)
                self.ui.tab.setText("OSC Settings")
                self.ui.frame_android.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST
                UIFunction.androidStackPages(self, "page_contact")

            elif self.ui.frame_izq.width() == 160 and index != 3:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_android)
                self.ui.tab.setText("About > OSC Settings")
                self.ui.frame_android.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        elif buttonName == 'bn_cloud':
            if self.ui.frame_izq.width() == 80 and index != 6:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_cloud)
                self.ui.tab.setText("Gesture Recording")
                self.ui.frame_cloud.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

            elif self.ui.frame_izq.width() == 160 and index != 2:  # ABOUT PAGE STACKED WIDGET
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_about_cloud)
                self.ui.tab.setText("About > Gesture Recording")
                self.ui.frame_cloud.setStyleSheet(
                    "background:rgb(91,90,90)")  # SETS THE BACKGROUND OF THE CLICKED BUTTON TO LITER COLOR THAN THE REST

        # ADD ANOTHER ELIF STATEMENT HERE FOR EXECUTING A NEW MENU BUTTON STACK PAGE.

    ########################################################################################################################

    ########################################################################################################################

    # ----> STACK WIDGET EACH PAGE FUNCTION PAGE FUNCTIONS
    # CODE TO PERFORM THE TASK IN THE STACKED WIDGET PAGE
    # WHAT EVER WIDGET IS IN THE STACKED PAGES ITS ACTION IS EVALUATED HERE AND THEN THE REST FUNCTION IS PASSED.
    def stackPage(self):

        ######### PAGE_HOME #############
        self.ui.home_open_bn.clicked.connect(lambda: APFunction.openBtnClicked(self))
        self.ui.home_close_bn.clicked.connect(lambda: APFunction.closeBtnClicked(self))
        self.ui.home_run_bn.clicked.connect(lambda: APFunction.runBtnClicked(self, self.ui.model_combo_box.currentText(), self.ui.model_combo_box.currentIndex()))
        self.ui.home_cam.frame_counter_signal.connect(lambda: APFunction.updateFrameCounter(self, 'page_home'))
        self.ui.home_cam.update_stats_signal.connect(lambda: APFunction.updateFeatureStats(self))
        self.ui.model_combo_box.currentIndexChanged.connect(lambda: APFunction.updateModel(self))

        ######### PAGE_BUG ##############
        self.ui.bn_bug_start.clicked.connect(lambda: APFunction.startTimerBtn(self, 'page_bug'))
        self.ui.bn_bug_stop.clicked.connect(lambda: APFunction.stopRecordBtn(self, 'page_bug'))
        self.ui.time_bar.timerEnded.connect(lambda: APFunction.timerFinished(self, 'page_bug'))
        self.ui.class_name.returnPressed.connect(lambda: APFunction.returnOnLineEdit(self, 'page_bug'))

        #########PAGE CLOUD #############
        self.ui.bn_cloud_start.clicked.connect(lambda: APFunction.startTimerBtn(self, 'page_cloud'))
        self.ui.bn_cloud_save.clicked.connect(lambda: APFunction.saveGesturesBtn(self))
        self.ui.cloud_time_bar.timerEnded.connect(lambda: APFunction.timerFinished(self, 'page_cloud'))
        self.ui.cloud_cam.frame_counter_signal.connect(lambda: APFunction.updateFrameCounter(self, 'page_cloud'))
        self.ui.bn_add_class.clicked.connect(lambda: APFunction.addClassBtn(self))
        self.ui.line_class_name.returnPressed.connect(lambda: APFunction.returnOnLineEdit(self, 'page_cloud'))
        self.ui.cloud_cam.counter_ended_signal.connect(lambda: APFunction.frameCounterEnded(self))

        #########PAGE ANDROID WIDGET AND ITS STACK ANDROID WIDGET PAGES
        self.ui.bn_android_contact.clicked.connect(lambda: UIFunction.androidStackPages(self, "page_contact"))

        ######ANDROID > PAGE CONTACT >>>>>>>>>>>>>>>>>>>>
        self.ui.bn_android_contact_edit.clicked.connect(lambda: APFunction.editable(self))
        self.ui.bn_android_contact_save.clicked.connect(lambda: APFunction.saveContact(self))

        ##########PAGE: ABOUT HOME #############
        self.ui.text_about_home.setVerticalScrollBar(self.ui.vsb_about_home)
        self.ui.text_about_home.setText(aboutHome)

        ##########PAGE: ABOUT BUG #############
        self.ui.text_about_bug.setVerticalScrollBar(self.ui.vsb_about_bug)
        self.ui.text_about_bug.setText(aboutPoseRec)

        ##########PAGE: ABOUT CLOUD #############
        self.ui.text_about_cloud.setVerticalScrollBar(self.ui.vsb_about_cloud)
        self.ui.text_about_cloud.setText(aboutGestureRec)

        ##########PAGE: ABOUT ANDROID #############
        self.ui.text_about_android.setVerticalScrollBar(self.ui.vsb_about_android)
        self.ui.text_about_android.setText(aboutOsc)

    ################################################################################################################################

    # -----> FUNCTION TO SHOW CORRESPONDING STACK PAGE WHEN THE ANDROID BUTTONS ARE PRESSED: CONTACT, GAME, CLOUD, WORLD
    # SINCE THE ANDROID PAGE AHS A SUB STACKED WIDGET WIT FOUR MORE BUTTONS, ALL THIS 4 PAGES CONTENT: BUTTONS, TEXT, LABEL E.T.C ARE INITIALIZED OVER HERE.
    def androidStackPages(self, page):
        # ------> THIS LINE CLEARS THE BG COLOR OF PREVIOUS TABS
        for each in self.ui.frame_android_menu.findChildren(QFrame):
            each.setStyleSheet("background:rgb(51,51,51)")

        if page == "page_contact":
            self.ui.stackedWidget_android.setCurrentWidget(self.ui.page_android_contact)
            self.ui.tab.setText("OSC Settings")
            self.ui.frame_android_contact.setStyleSheet("background:rgb(91,90,90)")

        # ADD A ADDITIONAL ELIF STATEMENT WITH THE SIMILAR CODE UP ABOVE FOR YOUR NEW SUBMENU BUTTON IN THE ANDROID STACK PAGE.
    ##############################################################################################################


# ------> CLASS WHERE ALL THE ACTION OF TH SOFTWARE IS PERFORMED:
# THIS CLASS IS WHERE THE APPLICATION OF THE UI OR THE BRAIN OF THE SOFTWARE GOES
# UNTIL NOW WE SPECIFIED THE BUTTON CLICKS, SLIDERS, E.T.C WIDGET, WHOSE APPLICATION IS EXPLORED HERE. THOSE FUNCTION WHEN DONE IS
# REDIRECTED TO THIS AREA FOR THE PROCESSING AND THEN THE RESULT ARE EXPORTED.
# REMEMBER THE SOFTWARE UI HAS A FUNCTION WHOSE CODE SHOULD BE HERE
class APFunction:
    # -----> FUNCTION IN ACCOUNT OF CONTACT PAGE IN ANDROID MENU
    def editable(self):
        self.ui.line_android_name.setEnabled(True)
        self.ui.line_android_adress.setEnabled(True)
        self.ui.line_android_org.setEnabled(True)

        self.ui.bn_android_contact_save.setEnabled(True)
        self.ui.bn_android_contact_edit.setEnabled(False)

    # -----> FUNCTION TO SAVE THE MODIFIED TEXT FIELD
    def saveContact(self):
        self.ui.home_cam.ip = self.ui.line_android_name.text()
        self.ui.home_cam.port = int(self.ui.line_android_adress.text())
        self.ui.home_cam.root_address = self.ui.line_android_org.text()
        self.ui.home_cam.client = udp_client.SimpleUDPClient(self.ui.home_cam.ip,  self.ui.home_cam.port)
        self.ui.line_android_name.setEnabled(False)
        self.ui.line_android_adress.setEnabled(False)
        self.ui.line_android_org.setEnabled(False)

        self.ui.bn_android_contact_save.setEnabled(False)
        self.ui.bn_android_contact_edit.setEnabled(True)

    def custom_close(self):
        if self.ui.home_cam.thread.isRunning():
            print('closing video thread')
            self.ui.home_cam.thread.stop()

        if self.ui.bug_cam.thread.isRunning():
            print('closing video thread')
            self.ui.bug_cam.thread.stop()

        if self.ui.cloud_cam.thread.isRunning():
            print('closing video thread')
            self.ui.cloud_cam.thread.stop()

        self.close()

    def openBtnClicked(self):
        print("click open button")
        if not self.ui.home_cam.thread.isRunning():
            self.ui.home_cam.thread.run_flag = True
            self.ui.home_cam.thread.start()

    def closeBtnClicked(self):
        print("click close button")
        if self.ui.home_cam.thread.isRunning():
            self.ui.home_cam.thread.stop()
            if self.ui.home_cam.main_state == 1:
                self.ui.home_cam.main_state = 0

    def runBtnClicked(self, model, model_index):
        self.ui.tab.setText("Running model > " + model)
        self.ui.home_cam.model_index = model_index
        if self.ui.home_cam.main_state == 0:
            if not self.ui.home_cam.thread.isRunning():
                print("Starting video thread")
                self.ui.home_cam.thread.run_flag = True
                self.ui.home_cam.thread.start()

            self.ui.home_cam.main_state = 1

    def updateModel(self):
        self.ui.tab.setText("Selected model > " + self.ui.model_combo_box.currentText())
        self.ui.home_cam.model_index = self.ui.model_combo_box.currentIndex()

    def startTimerBtn(self, page):
        print("starting")
        if page == 'page_bug':
            if self.ui.bug_cam.main_state == 0:
                if not self.ui.bug_cam.thread.isRunning():
                    print("Starting video thread")
                    self.ui.bug_cam.thread.run_flag = True
                    self.ui.bug_cam.thread.start()
                self.ui.bug_cam.main_state = 1

            self.ui.time_bar.thread.start()

        elif page == 'page_cloud':
            if self.ui.cloud_cam.main_state == 0:
                if not self.ui.cloud_cam.thread.isRunning():
                    print("Starting video thread")
                    self.ui.cloud_cam.thread.run_flag = True
                    self.ui.cloud_cam.thread.start()
                self.ui.cloud_cam.main_state = 1

            self.ui.cloud_cam.setEnabled(False)
            self.ui.cloud_time_bar.thread.start()

    def stopRecordBtn(self, page):
        print("stop recording")
        if page == 'page_bug':
            if self.ui.bug_cam.thread.isRunning():
                self.ui.bug_cam.thread.stop()
                if self.ui.bug_cam.main_state == 3:
                    class_name = self.ui.class_name.text()
                    compression_opts = dict(method='zip', archive_name=class_name + '.csv')
                    self.ui.bug_cam.df.to_csv(class_name + '.zip', index=False, compression=compression_opts)
                    self.ui.bug_cam.main_state = 0

            self.ui.bn_bug_stop.setEnabled(False)
            self.ui.bn_bug_start.setEnabled(False)
            self.ui.class_name.clear()
            self.ui.class_name.setEnabled(True)
            self.ui.time_bar.progress_bar.setValue(0)

    def timerFinished(self, page):
        if page == 'page_bug':
            self.ui.bn_bug_stop.setEnabled(True)
            self.ui.bn_bug_start.setEnabled(False)
            self.ui.bug_cam.main_state = 2

        elif page == 'page_cloud':
            self.ui.bn_cloud_start.setEnabled(False)
            self.ui.cloud_cam.main_state = 4
            self.ui.cloud_cam.setEnabled(True)

    def saveGesturesBtn(self):
        print("saving gestures")
        print(np.array(self.ui.cloud_cam.features_dataset).shape)
        print(np.array(self.ui.cloud_cam.labels_dataset))
        print(self.ui.cloud_cam.class_names)

        np.savez_compressed('hand_gestures.npz',
                            x_train=self.ui.cloud_cam.features_dataset,
                            y_train=self.ui.cloud_cam.labels_dataset,
                            class_names=self.ui.cloud_cam.class_names)

        self.ui.line_class_name.clear()
        self.ui.line_class_name.setEnabled(True)
        self.ui.bn_cloud_start.setEnabled(False)
        self.ui.bn_cloud_save.setEnabled(False)

    def addClassBtn(self):
        print(self.ui.line_class_name.text())
        self.ui.line_class_name.setEnabled(False)
        self.ui.bn_cloud_start.setEnabled(True)
        self.ui.bn_add_class.setEnabled(False)
        self.ui.cloud_cam.class_names[len(self.ui.cloud_cam.class_names)] = self.ui.line_class_name.text()

    def returnOnLineEdit(self, page):
        if page == 'page_bug':
            self.ui.bn_bug_start.setEnabled(True)
            self.ui.class_name.setEnabled(False)
        elif page == 'page_cloud':
            self.ui.bn_add_class.setEnabled(True)

    def updateFrameCounter(self, page):
        if page == 'page_home':
            self.ui.home_cam.frame_counter = self.ui.home_cam.frame_counter + 1

        elif page == 'page_cloud':
            self.ui.cloud_cam.frame_counter = self.ui.cloud_cam.frame_counter + 1
            text = 'Frames: ' + str(self.ui.cloud_cam.frame_counter)
            self.ui.count_frames_label.setText(text)

    def frameCounterEnded(self):
        self.ui.cloud_cam.main_state = 1
        self.ui.bn_cloud_start.setEnabled(True)
        self.ui.cloud_cam.setEnabled(False)
        self.ui.cloud_time_bar.progress_bar.setValue(0)
        self.ui.bn_cloud_save.setEnabled(True)

    def updateFeatureStats(self):
        line = ''
        for (k, v) in self.ui.home_cam.model_features.items():
            line += "\n" + k + ": " + str(v)

        self.ui.model_statistics.setText(line)
###############################################################################################################################################################
