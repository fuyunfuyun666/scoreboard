from PyQt5 import QtWidgets,QtGui,QtCore
import sys
from ui import Ui_MainWindow
from scoreboard import scoreboard

class ScoreboardWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ScoreboardWindow,self).__init__()

        self.t1=[]
        self.t2=[]
        self.t3=[]
        self.clock=0

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        # 设置表头内容
        header1=["iusse","read","execution","write"]
        # header2=["LD F6 34,R2",'LD F2 45,R3','MULT F0 F2,F4',\
        #     'SUBD F8 F6,F2','DIVD F10 F0,F6','ADDD F6 F8,F2']
        self.ui.table1.setHorizontalHeaderLabels(header1)
        # self.ui.table1.setVerticalHeaderLabels(header2)
        self.ui.table1.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        header3=["busy","op","Fi","Fj",'Fk','Qj','Qk','Rj','Rk']
        header4=['Integer','Mult1','Mult2','Add','Divide']
        self.ui.table2.setHorizontalHeaderLabels(header3)
        self.ui.table2.setVerticalHeaderLabels(header4)
        self.ui.table2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        header5=['F0','F2','F4','F6','F8','F10']
        header6=['item']
        self.ui.table3.setHorizontalHeaderLabels(header5)
        self.ui.table3.setVerticalHeaderLabels(header6)
        self.ui.table3.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ui.button1.clicked.connect(self.click_next_step)
        self.ui.button_run.clicked.connect(self.run_all)
        self.ui.button_reset_current.clicked.connect(self.reset_current_run)
        self.ui.button_run_to.clicked.connect(self.run_to_step)
        self.ui.button_load.clicked.connect(self.load_instructions)
        self.ui.button_load_fromtxt.clicked.connect(self.load_instructions_fromtxt)

    def load_instructions_fromtxt(self):
        instructions = []
        # 初始化这个实例，设置一些基本属性
        dlg = QtWidgets.QFileDialog(directory='./',filter="*.txt")
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setFilter(QtCore.QDir.Files)
        # 当选择器关闭的时候
        if dlg.exec_():
            # 拿到所选择的的文本
            filenames = dlg.selectedFiles()
            # 读取文本内容设置到TextEdit当中来
            # print(filenames)#可以选择多个文件，返回的是一个list
            f = open(filenames[0], 'r')
            with f:
                x=f.readlines()
                # print(x)
                # .strip('\n').split('\n')
                for i in x:
                    i = i.strip()
                    if i:
                        i_list = i.split(',')
                        if len(i_list) == 4:
                            i_list.append(2)
                            i_list.append(0)
                            instructions.append(i_list)
                        elif len(i_list) == 5:
                            i_list[4] = int(i_list[4])
                            i_list.append(0)
                            instructions.append(i_list)
                        else:
                            instructions=[]
                            break
        if instructions:
            self.t1, self.t2, self.t3 = scoreboard(instructions)
            self.ui.table1.setRowCount(len(instructions))
            header_row=[(','.join(i[0:4]))for i in instructions]
            self.ui.table1.setVerticalHeaderLabels(header_row)
            QtWidgets.QMessageBox.information(self, '提示', '代码加载成功', QtWidgets.QMessageBox.Yes)
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "指令读入错误或者文件中没有代码，请重新加载",
                                          QtWidgets.QMessageBox.Yes)

    def load_instructions(self):
        instructions=self.read_instructions()
        if instructions:
            self.t1, self.t2, self.t3 = scoreboard(instructions)
            self.ui.table1.setRowCount(len(instructions))
            header_row=[(','.join(i[0:4]))for i in instructions]
            self.ui.table1.setVerticalHeaderLabels(header_row)
            QtWidgets.QMessageBox.information(self, '提示', '代码加载成功', QtWidgets.QMessageBox.Yes)

    def run_to_step(self):
        if self.t1==[]:
            QtWidgets.QMessageBox.warning(self,'警告','当前面板没有代码，请点击加载代码',QtWidgets.QMessageBox.Yes)
        else:
            step=self.ui.step_to.text()
            if step=='':
                QtWidgets.QMessageBox.information(self, "提示", '请输入步数', QtWidgets.QMessageBox.Yes)
            else:
                step=int(step)
                if step>len(self.t1):
                    QtWidgets.QMessageBox.information(
                        self, "提示", "输入的步数"+str(step)+"大于当前代码运行的最大步数，请重新输入", QtWidgets.QMessageBox.Yes
                    )
                elif step==self.clock:
                    QtWidgets.QMessageBox.information(
                        self, "提示", "已经运行到"+str(step)+"步，请重新输入步数", QtWidgets.QMessageBox.Yes
                    )
                else:
                    self.clock=0
                    self.ui.table1.clearContents()
                    self.ui.table2.clearContents()
                    self.ui.table3.clearContents()
                    for i in range(step):
                        self.update_table()

    def reset_current_run(self):
        self.clock=0
        self.ui.table1.clearContents()
        self.ui.table2.clearContents()
        self.ui.table3.clearContents()
        self.ui.step_to.setText('')

    def read_instructions(self):
        result=[]
        x=self.ui.instructions.toPlainText().strip('\n').split('\n')
        for i in x:
            i=i.strip()
            i_list=i.split(',')
            if len(i_list)==4:
                i_list.append(2)
                i_list.append(0)
                result.append(i_list)
            elif len(i_list)==5:
                i_list[4]=int(i_list[4])
                i_list.append(0)
                result.append(i_list)
            else:
                QtWidgets.QMessageBox.warning(self,"警告","指令输入错误"+str(i),
                                              QtWidgets.QMessageBox.Yes)
                return []

        return result

    def run_all(self):
        if len(self.t1)==0:
            QtWidgets.QMessageBox.warning(self, '警告', '当前面板没有代码，请点击加载代码', QtWidgets.QMessageBox.Yes)
        else:
            clock=self.clock
            if clock>=len(self.t1):
                QtWidgets.QMessageBox.information(self, "提示", "代码运行完成，如果需要请重新开始",
                                                  QtWidgets.QMessageBox.Yes)
            else:
                while clock<len(self.t1):
                    self.update_table()
                    clock+=1

    def update_table(self):
        clock = self.clock
        if clock < len(self.t1):
            count = 0
            while count < len(self.t1[clock]):
                if self.t1[clock][count][0]:
                    a = QtWidgets.QTableWidgetItem(str(self.t1[clock][count][0]))
                    a.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.table1.setItem(count, 0, a)
                if self.t1[clock][count][1]:
                    a = QtWidgets.QTableWidgetItem(str(self.t1[clock][count][1]))
                    a.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.table1.setItem(count, 1, a)
                if self.t1[clock][count][2]:
                    a = QtWidgets.QTableWidgetItem(str(self.t1[clock][count][2]))
                    a.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.table1.setItem(count, 2, a)
                if self.t1[clock][count][3]:
                    a = QtWidgets.QTableWidgetItem(str(self.t1[clock][count][3]))
                    a.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.ui.table1.setItem(count, 3, a)
                count += 1

            for i, item in enumerate(self.t2[clock][0]):
                a = QtWidgets.QTableWidgetItem(str(item))
                a.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.table2.setItem(0, i, a)
            for i, item in enumerate(self.t2[clock][1]):
                a = QtWidgets.QTableWidgetItem(str(item))
                a.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.table2.setItem(1, i, a)
            for i, item in enumerate(self.t2[clock][2]):
                a = QtWidgets.QTableWidgetItem(str(item))
                a.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.table2.setItem(2, i, a)
            for i, item in enumerate(self.t2[clock][3]):
                a = QtWidgets.QTableWidgetItem(str(item))
                a.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.table2.setItem(3, i, a)
            # if self.t2[clock]['Divide'][0]:
            for i, item in enumerate(self.t2[clock][4]):
                a = QtWidgets.QTableWidgetItem(str(item))
                a.setTextAlignment(QtCore.Qt.AlignCenter)
                self.ui.table2.setItem(4, i, a)

            a = QtWidgets.QTableWidgetItem(str(self.t3[clock]['F0']))
            a.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.table3.setItem(0, 0, a)
            a = QtWidgets.QTableWidgetItem(str(self.t3[clock]['F2']))
            a.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.table3.setItem(0, 1, a)
            a = QtWidgets.QTableWidgetItem(str(self.t3[clock]['F4']))
            a.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.table3.setItem(0, 2, a)
            a = QtWidgets.QTableWidgetItem(str(self.t3[clock]['F6']))
            a.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.table3.setItem(0, 3, a)
            a = QtWidgets.QTableWidgetItem(str(self.t3[clock]['F8']))
            a.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.table3.setItem(0, 4, a)
            a = QtWidgets.QTableWidgetItem(str(self.t3[clock]['F10']))
            a.setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.table3.setItem(0, 5, a)

            self.ui.text3.setText(str(clock + 1))
            self.clock += 1
        else:
            QtWidgets.QMessageBox.information(self, "提示", "代码运行完成，如果需要请重新开始",
                                          QtWidgets.QMessageBox.Yes)

    def click_next_step(self):
        if self.t1==[]:
            QtWidgets.QMessageBox.warning(self,'警告','当前面板没有代码，请点击加载代码',QtWidgets.QMessageBox.Yes)
        else:
            self.update_table()


if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    widget=ScoreboardWindow()
    widget.setWindowTitle('Scoreboard Algorithm')
    widget.show()
    sys.exit(app.exec_())