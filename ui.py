# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)

        self.text_t1=QtWidgets.QLabel(self.centralwidget)
        self.text_t1.setGeometry(QtCore.QRect(30,30,180,25))
        self.text_t1.setText("指令状态表")
        self.text_t2 = QtWidgets.QLabel(self.centralwidget)
        self.text_t2.setGeometry(QtCore.QRect(660, 30, 180, 25))
        self.text_t2.setText("部件状态表")
        self.text_t3 = QtWidgets.QLabel(self.centralwidget)
        self.text_t3.setGeometry(QtCore.QRect(30, 330, 180, 25))
        self.text_t3.setText("寄存器状态表")
        font.setBold(True)
        self.text_t1.setFont(font)
        self.text_t2.setFont(font)
        self.text_t3.setFont(font)
        font.setBold(False)

        self.instructions=QtWidgets.QTextEdit(self.centralwidget)
        self.instructions.setGeometry(QtCore.QRect(700,400,600,300))
        self.instructions.setPlaceholderText('请输入指令，指令之间使用逗号作为分隔符，每条指令占一行。'
                                             '\n指令的格式为：'
                                             '\nop, des, src1, src2, clock'
                                             '\n其中clock为指令的执行周期，可省略使用默认周期。例如\n'
                                             'MULT,F0,F2,F4,10 或者 MULT,F0,F2,F4')
        self.instructions.setText('LD,F6,34,R2,1\n'
                                    'LD,F2,45,R3,1\n'
                                    'MULT,F0,F2,F4,10\n'
                                    'SUBD,F8,F6,F2,2\n'
                                    'DIVD,F10,F0,F6,40\n'
                                    'ADDD,F6,F8,F2,2')
        self.instructions.setFont(font)

        self.button1=QtWidgets.QPushButton(self.centralwidget)
        self.button1.setGeometry(QtCore.QRect(20,500,200,40))
        self.button1.setText('下一步')
        self.button1.setFont(font)

        self.button_run = QtWidgets.QPushButton(self.centralwidget)
        self.button_run.setGeometry(QtCore.QRect(240, 500, 200, 40))
        self.button_run.setText('全部运行')
        self.button_run.setFont(font)

        self.button_run_to = QtWidgets.QPushButton(self.centralwidget)
        self.button_run_to.setGeometry(QtCore.QRect(20, 570, 200, 40))
        self.button_run_to.setText('跳到')
        self.button_run_to.setFont(font)
        self.step_to=QtWidgets.QLineEdit(self.centralwidget)
        self.step_to.setGeometry(QtCore.QRect(220, 570, 220, 40))
        self.step_to.setValidator(QtGui.QIntValidator(1,1000000))
        # self.button_run_to.setText('run to')
        self.step_to.setFont(font)
        self.step_to.setPlaceholderText('输入数字1~1000000')

        self.button_reset_current = QtWidgets.QPushButton(self.centralwidget)
        self.button_reset_current.setGeometry(QtCore.QRect(20, 640, 200, 40))
        self.button_reset_current.setText('重置运行')
        self.button_reset_current.setFont(font)

        self.button_load = QtWidgets.QPushButton(self.centralwidget)
        self.button_load.setGeometry(QtCore.QRect(240, 640, 200, 40))
        self.button_load.setText('加载代码')
        self.button_load.setFont(font)

        self.button_load_fromtxt = QtWidgets.QPushButton(self.centralwidget)
        self.button_load_fromtxt.setGeometry(QtCore.QRect(20, 700, 200, 40))
        self.button_load_fromtxt.setText('从文本文件加载代码')
        self.button_load_fromtxt.setFont(font)

        # self.text1 = QtWidgets.QLabel(self.centralwidget)
        # self.text1.setGeometry(QtCore.QRect(300, 700, 320, 30))
        # self.text1.setObjectName("text1")
        # self.text1.setFont(font)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 450, 180, 20))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.text2 = QtWidgets.QLabel(self.widget)
        self.text2.setObjectName("text2")
        self.text2.setFont(font)

        self.horizontalLayout.addWidget(self.text2)
        self.text3 = QtWidgets.QLabel(self.widget)
        self.text3.setEnabled(True)
        self.text3.setObjectName("text3")
        self.text3.setFont(font)
        self.horizontalLayout.addWidget(self.text3)

        self.table1 = QtWidgets.QTableWidget(self.centralwidget)
        self.table1.setGeometry(QtCore.QRect(20, 60, 600, 260))
        self.table1.setObjectName("table1")
        self.table1.setColumnCount(4)
        # self.table1.setRowCount(6)
        # self.table1.setShowGrid(False)

        self.table2 = QtWidgets.QTableWidget(self.centralwidget)
        self.table2.setGeometry(QtCore.QRect(650, 60, 800, 260))
        self.table2.setObjectName("table2")
        self.table2.setColumnCount(9)
        self.table2.setRowCount(5)

        self.table3 = QtWidgets.QTableWidget(self.centralwidget)
        self.table3.setGeometry(QtCore.QRect(20, 360, 600, 70))
        self.table3.setObjectName("table3")
        self.table3.setColumnCount(6)
        self.table3.setRowCount(1)

        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 874, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.text1.setText(_translate("MainWindow", "减法2周期，乘法3周期，除法4周期"))
        self.text2.setText(_translate("MainWindow", "Current clock:"))
        self.text3.setText(_translate("MainWindow", "0"))