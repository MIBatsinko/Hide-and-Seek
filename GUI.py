from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QMessageBox, QLabel
from steg import Stegano
from unsteg import Unstegano


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(800,620)
        self.setupUi(self)
        self.show()
        self.s = Stegano()
        self.uns = Unstegano()
        self.toolButton.clicked.connect(self.open_cont)
        self.toolButton_2.clicked.connect(self.open_sec)
        self.toolButton_7.clicked.connect(self.savePath)
        self.pushButton.clicked.connect(self.hide)
        self.toolButton_5.clicked.connect(self.open_steg)
        self.toolButton_6.clicked.connect(self.open_key)
        self.toolButton_8.clicked.connect(self.savePath2)
        self.pushButton_2.clicked.connect(self.unhide)
        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(True)
        self.statusBar.showMessage('Enter the path to files')

    def open_cont(self):
        self.cont_name = QFileDialog.getOpenFileName(self, "Open container", "", "(*.bmp)")[0]
        self.lbl_string_1.setText(self.cont_name)
        if self.empty_path():
            pixmap = QtGui.QPixmap(self.cont_name)
            w = self.lbl_img_1.width()
            h = self.lbl_img_1.height()
            self.lbl_img_1.setPixmap(pixmap.scaled(w, h))
            self.s.open_container(self.cont_name)
            self.label_3.setText("Max size of data to hide: " + self.s.max_size() + " bytes")

    def open_sec(self):
        self.sec_name = QFileDialog.getOpenFileName(self, "Open secret")[0]
        self.lbl_string_2.setText(self.sec_name)
        self.error_length_str_2()

        if self.empty_path_str_2():
            self.label_33.setText("Size of the secret file:" + self.s.secret_size() + " bytes")
            self.error_hide_button()
        else:
            self.statusBar.showMessage('Input error')
            self.lbl_string_2.setText("Open other file")


    def savePath(self):
        self.out_name = QFileDialog.getSaveFileName(self, "Save stego")[0]
        self.lbl_string_3.setText(self.out_name + ".bmp")
        self.error_hide_button()

    def hide(self):
        self.statusBar.showMessage('Waiting...')
        self.s.steg(self.out_name)
        self.result_img()
        self.statusBar.showMessage('Done!')

    def result_img(self):
        pixmap = QtGui.QPixmap(self.out_name)
        w = self.lbl_img_2.width()
        h = self.lbl_img_2.height()
        self.lbl_img_2.setPixmap(pixmap.scaled(w, h))

    def open_steg(self):
        self.steg_name = QFileDialog.getOpenFileName(self, "Open container", "", "(*.bmp)")[0]
        self.lbl_string_4.setText(self.steg_name)
        if self.steg_name:
            self.uns.open_container(self.steg_name)
            self.error_unhide_button()

    def open_key(self):
        self.key_name = QFileDialog.getOpenFileName(self, "Open key", "", "(*.stg)")[0]
        self.lbl_string_5.setText(self.key_name)
        if self.key_name:
            self.uns.open_key(self.key_name)
            self.error_unhide_button()

    def savePath2(self):
        self.out_name_2 = QFileDialog.getSaveFileName(self, "Save secret")[0]
        self.lbl_string_6.setText(self.out_name_2)
        self.error_unhide_button()

    def unhide(self):
        self.statusBar.showMessage('Waiting...')
        self.uns.unsteg()
        self.uns.save_output(self.out_name_2)
        self.statusBar.showMessage('Done!')

    def empty_path(self):
        if self.lbl_string_1.text() == "":
            return 0
        else:
            return 1

    def empty_path_str_2(self):
        if self.lbl_string_2.text() == "":
            return 0
        elif self.lbl_string_1.text() == "":
            return 0
        else:
            return 1

    def error_length_str_2(self):
        if self.lbl_string_2.text() == "":
            return 0
        elif self.lbl_string_1.text() == "":
            return 0
        elif self.s.open_secret(self.sec_name) == 0:
            QMessageBox.critical(self, "Too big file", "The secret file is too big for this container!",
                                 QMessageBox.Ok, QMessageBox.Ok)
            return 0
        else:
            return 1

    def error_length_str_3(self):
        if self.lbl_string_5.text() == "":
            return 0
        elif self.lbl_string_4.text() == "":
            return 0
        elif self.lbl_string_6.text() == "":
            return 0
        else:
            return 1

    def error_hide_button(self):
        if self.error_length_str_2() and int(self.s.max_size()) > int(self.s.secret_size()):
            if self.lbl_string_3.text() != ".bmp" and self.lbl_string_3.text() != "":
                self.pushButton.setEnabled(True)
            return 1

    def error_unhide_button(self):
        if self.error_length_str_3():
            self.pushButton_2.setEnabled(True)
            return 1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 620)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 801, 571))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.toolButton = QtWidgets.QToolButton(self.tab)
        self.toolButton.setGeometry(QtCore.QRect(530, 20, 27, 22))
        self.toolButton.setObjectName("toolButton")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(30, 20, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.toolButton_2 = QtWidgets.QToolButton(self.tab)
        self.toolButton_2.setGeometry(QtCore.QRect(530, 50, 27, 22))
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton_7 = QtWidgets.QToolButton(self.tab)
        self.toolButton_7.setGeometry(QtCore.QRect(530, 80, 27, 22))
        self.toolButton_7.setObjectName("toolButton_7")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(30, 80, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setGeometry(QtCore.QRect(340, 160, 121, 361))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.frame_3 = QtWidgets.QFrame(self.tab)
        self.frame_3.setGeometry(QtCore.QRect(160, 80, 351, 21))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_3.setObjectName("frame_3")
        self.lbl_string_3 = QtWidgets.QLabel(self.frame_3)
        self.lbl_string_3.setGeometry(QtCore.QRect(5, 0, 341, 16))
        self.lbl_string_3.setText("")
        self.lbl_string_3.setObjectName("label_16")
        self.frame_4 = QtWidgets.QFrame(self.tab)
        self.frame_4.setGeometry(QtCore.QRect(160, 50, 351, 21))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_4.setObjectName("frame_4")
        self.lbl_string_2 = QtWidgets.QLabel(self.frame_4)
        self.lbl_string_2.setGeometry(QtCore.QRect(5, 0, 341, 16))
        self.lbl_string_2.setText("")
        self.lbl_string_2.setObjectName("label_15")
        self.frame_5 = QtWidgets.QFrame(self.tab)
        self.frame_5.setGeometry(QtCore.QRect(160, 20, 351, 21))
        self.frame_5.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_5.setObjectName("frame_5")
        self.lbl_string_1 = QtWidgets.QLabel(self.frame_5)
        self.lbl_string_1.setGeometry(QtCore.QRect(5, 0, 341, 16))
        self.lbl_string_1.setText("")
        self.lbl_string_1.setObjectName("label_14")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(600, 10, 181, 131))
        font = QtGui.QFont()
        font.setPointSize(27)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.frame = QtWidgets.QFrame(self.tab)
        self.frame.setGeometry(QtCore.QRect(0, 520, 401, 21))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(20, 0, 91, 21))
        self.label_11.setObjectName("label_11")
        self.frame_7 = QtWidgets.QFrame(self.tab)
        self.frame_7.setGeometry(QtCore.QRect(410, 160, 381, 351))
        self.frame_7.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_7.setLineWidth(2)
        self.frame_7.setObjectName("frame_7")
        self.lbl_img_2 = QtWidgets.QLabel(self.frame_7)
        self.lbl_img_2.setGeometry(QtCore.QRect(10, 10, 361, 331))
        self.lbl_img_2.setText("")
        self.lbl_img_2.setScaledContents(True)
        self.lbl_img_2.setObjectName("label_18")
        self.frame_6 = QtWidgets.QFrame(self.tab)
        self.frame_6.setGeometry(QtCore.QRect(10, 160, 381, 351))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_6.setLineWidth(2)
        self.frame_6.setObjectName("frame_6")
        self.lbl_img_1 = QtWidgets.QLabel(self.frame_6)
        self.lbl_img_1.setGeometry(QtCore.QRect(10, 10, 361, 331))
        self.lbl_img_1.setText("")
        self.lbl_img_1.setScaledContents(True)
        self.lbl_img_1.setObjectName("label_17")
        self.frame_2 = QtWidgets.QFrame(self.tab)
        self.frame_2.setGeometry(QtCore.QRect(400, 520, 401, 21))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_12 = QtWidgets.QLabel(self.frame_2)
        self.label_12.setGeometry(QtCore.QRect(20, 0, 141, 21))
        self.label_12.setObjectName("label_12")
        self.frame_12 = QtWidgets.QFrame(self.tab)
        self.frame_12.setGeometry(QtCore.QRect(20, 110, 271, 31))
        self.frame_12.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setLineWidth(1)
        self.frame_12.setMidLineWidth(0)
        self.frame_12.setObjectName("frame_12")
        self.frame_112 = QtWidgets.QFrame(self.tab)
        self.frame_112.setGeometry(QtCore.QRect(300, 110, 260, 31))
        self.frame_112.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_112.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_112.setLineWidth(1)
        self.frame_112.setMidLineWidth(0)
        self.frame_112.setObjectName("frame_112")
        self.label_3 = QtWidgets.QLabel(self.frame_12)
        self.label_3.setGeometry(QtCore.QRect(10, 0, 251, 31))
        self.label_3.setObjectName("label_3")
        self.label_33 = QtWidgets.QLabel(self.frame_112)
        self.label_33.setGeometry(QtCore.QRect(10, 0, 251, 31))
        self.label_33.setObjectName("label_33")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(30, 20, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(30, 50, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setGeometry(QtCore.QRect(30, 80, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.frame_8 = QtWidgets.QFrame(self.tab_2)
        self.frame_8.setGeometry(QtCore.QRect(130, 20, 341, 21))
        self.frame_8.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_8.setObjectName("frame_8")
        self.lbl_string_4 = QtWidgets.QLabel(self.frame_8)
        self.lbl_string_4.setGeometry(QtCore.QRect(5, 0, 331, 16))
        self.lbl_string_4.setText("")
        self.lbl_string_4.setObjectName("label_5")
        self.frame_9 = QtWidgets.QFrame(self.tab_2)
        self.frame_9.setGeometry(QtCore.QRect(130, 80, 341, 21))
        self.frame_9.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_9.setObjectName("frame_9")
        self.lbl_string_6 = QtWidgets.QLabel(self.frame_9)
        self.lbl_string_6.setGeometry(QtCore.QRect(5, 0, 331, 16))
        self.lbl_string_6.setText("")
        self.lbl_string_6.setObjectName("label_13")
        self.toolButton_5 = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_5.setGeometry(QtCore.QRect(490, 20, 27, 22))
        self.toolButton_5.setObjectName("toolButton_5")
        self.toolButton_8 = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_8.setGeometry(QtCore.QRect(490, 80, 27, 22))
        self.toolButton_8.setObjectName("toolButton_8")
        self.frame_10 = QtWidgets.QFrame(self.tab_2)
        self.frame_10.setGeometry(QtCore.QRect(130, 50, 341, 21))
        self.frame_10.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_10.setObjectName("frame_10")
        self.lbl_string_5 = QtWidgets.QLabel(self.frame_10)
        self.lbl_string_5.setGeometry(QtCore.QRect(5, 0, 331, 16))
        self.lbl_string_5.setText("")
        self.lbl_string_5.setObjectName("label_6")
        self.toolButton_6 = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_6.setGeometry(QtCore.QRect(490, 50, 27, 22))
        self.toolButton_6.setObjectName("toolButton_6")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(560, 10, 221, 131))
        font = QtGui.QFont()
        font.setPointSize(27)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(20, 170, 757, 364))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("source\steg.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setOpenExternalLinks(False)
        self.label_4.setObjectName("label_4")
        self.frame_11 = QtWidgets.QFrame(self.tab_2)
        self.frame_11.setGeometry(QtCore.QRect(10, 160, 775, 381))
        self.frame_11.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setLineWidth(3)
        self.frame_11.setMidLineWidth(0)
        self.frame_11.setObjectName("frame_11")
        self.tabWidget.addTab(self.tab_2, "")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(-3, 170, 801, 20))
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        # menubar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuLanguage = QtWidgets.QMenu(self.menuSettings)
        self.menuLanguage.setObjectName("menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setObjectName("action_Exit")
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.actionDocumentation.triggered.connect(self.open_doc)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout.triggered.connect(self.open_about)
        self.actionEnglish = QtWidgets.QAction(MainWindow)
        self.actionEnglish.setObjectName("actionEnglish")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open_doc(self):
        self.doc = Documentation()

    def open_about(self):
        self.about = About()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hide and Seek"))
        self.label_2.setText(_translate("MainWindow", "Secret file:"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "Image container:"))
        self.toolButton_2.setText(_translate("MainWindow", "..."))
        self.toolButton_7.setText(_translate("MainWindow", "..."))
        self.label_9.setText(_translate("MainWindow", "Output image:"))
        self.pushButton.setText(_translate("MainWindow", "Hide!"))
        self.label_11.setText(_translate("MainWindow", "Original image"))
        self.label_12.setText(_translate("MainWindow", "Steganographic image"))
        self.label_3.setText(_translate("MainWindow", "Max size of data to hide:"))
        self.label_33.setText(_translate("MainWindow", "Size of the secret file:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Hide"))
        self.label_7.setText(_translate("MainWindow", "Steg image:"))
        self.label_8.setText(_translate("MainWindow", "Key:"))
        self.label_10.setText(_translate("MainWindow", "Output file:"))
        self.toolButton_5.setText(_translate("MainWindow", "..."))
        self.toolButton_8.setText(_translate("MainWindow", "..."))
        self.toolButton_6.setText(_translate("MainWindow", "..."))
        self.pushButton_2.setText(_translate("MainWindow", "Unhide!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Unhide"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


class About(object):
    def __init__(self, parent=None):
        super().__init__()
        self.Form = QtWidgets.QWidget()
        self.setupUi(self.Form)
        self.Form.show()

    def setupUi(self, Form):
        Form.setObjectName("About")
        Form.resize(602, 505)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 10, 585, 491))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 563, 471))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("About", "About"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">About</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#000000;\">Hide and Seek</span></a><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; text-decoration: underline; color:#000000;\"> - is a software product that embeds in an image format .bmp file that you want to hide.</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; color:#000000;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; color:#000000;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#000000;\">Author: </span></a><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; text-decoration: underline; color:#000000;\">Maks Batsinko</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#000000;\">Email: </span></a><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; text-decoration: underline; color:#000000;\">batsinko.m@donnu.edu.ua</span></a></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#000000;\">Version: </span></a><a href=\"http://cs.viateam.ru/monitoring/csgo-servera-hide-and-seek-hns\"><span style=\" font-size:11pt; text-decoration: underline; color:#000000;\">1.0</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; font-weight:600; color:#000000;\"><br /></p></body></html>"))


class Documentation(QLabel):
    def __init__(self, parent=None):
        super().__init__()
        self.Form = QtWidgets.QWidget()
        self.setupUi(self.Form)
        self.Form.show()

    def setupUi(self, Form):
        Form.setObjectName("Documentation")
        Form.resize(602, 505)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(10, 10, 585, 491))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 563, 471))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Documentation", "Documentation"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600;\">Instruction</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; text-decoration: underline;\">How to hide file:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1. Specify the path to the container.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">2. Specify the path to the file that you want to hide.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">3. Specify the path where you want to save the filled container</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">4. Click “Hide!”</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:600;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; text-decoration: underline;\">How to unhide file:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:11pt; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">To decrypt your hidden file you need to perform these actions on another tab:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">1. Specify the path to the filled container.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">2. Specify the path to the key file.</span></p></body></html>"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
