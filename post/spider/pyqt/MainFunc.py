import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import CutPart
import UpdatePart
import SubPart
import AddPart

#主窗口
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.excel_file=None
        self.csv_file=None
        self.setWindowTitle("对比工具表操作")

        self.cwd = os.getcwd() # 获取当前程序文件位置
        self.resize(500,300)   # 设置窗体大小

        #Excel文件
        self.ExcelEdit = QLineEdit(self)
        self.chooseExcel = QPushButton(self)  
        self.chooseExcel.setObjectName("chooseExcel")  
        self.chooseExcel.setText("选取Excel文件")
        self.chooseExcel.clicked.connect(self.chooseExcelClick)

        #CSV文件
        self.CSVEdit = QLineEdit(self)
        self.chooseCSV = QPushButton(self)
        self.chooseCSV.setObjectName("chooseCSV")
        self.chooseCSV.setText("选取CSV文件")
        self.chooseCSV.clicked.connect(self.chooseCSVClick)

        #更新部分
        self.update = QPushButton('更新部分')
        self.update.clicked.connect(self.onUpdateClick)

        #新增部分
        self.add = QPushButton('新增部分')
        self.add.clicked.connect(self.onAddClick)

        #减少部分
        self.sub = QPushButton('减少部分')
        self.sub.clicked.connect(self.onSubClick)

        #退出程序        
        self.quit = QPushButton("退出")
        # 将信号与槽关联
        self.quit.clicked.connect(self.onQuitClick)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.quit)

        #布局
        gridLayout = QGridLayout()
        gridLayout.addWidget(QLabel("Excel表路径:"),1,0)
        gridLayout.addWidget(self.ExcelEdit,1,1)
        gridLayout.addWidget(self.chooseExcel,1,2)
        gridLayout.addWidget(QLabel("old文档路径:"),2,0)
        gridLayout.addWidget(self.CSVEdit,2,1)
        gridLayout.addWidget(self.chooseCSV,2,2)
        gridLayout.addWidget(self.update,3,1)
        gridLayout.addWidget(self.add,4,1)
        gridLayout.addWidget(self.sub,5,1)
        gridLayout.addWidget(self.quit,6,2)
        self.setLayout(gridLayout)

    #选Excel文件按钮
    def chooseExcelClick(self):
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,  
                                    "选取文件",  
                                    self.cwd, # 起始路径 
                                    "Excel Files (*.xlsm);;Text Files (*.txt)")   # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            print("\n取消选择")
            return
        self.excel_file=fileName_choose

        print("\n你选择的文件为:")
        print(fileName_choose)
        print("文件筛选器类型: ",filetype)
        self.ExcelEdit.setText(fileName_choose)

    #选CSV文件按钮
    def chooseCSVClick(self):
        files, filetype = QFileDialog.getOpenFileNames(self,  
                                    "多文件选择",
                                    self.cwd, # 起始路径 
                                    "CSV Files (*.csv);;Text Files (*)")  

        if len(files) == 0:
            print("\n取消选择")
            return
        print("\n你选择的文件为:")
        print(files)
        self.csv_file=files
        print("文件筛选器类型: ",filetype)
        self.CSVEdit.setText(str(files))

    #更新按钮
    def onUpdateClick(self,):
        # self.hide()
        self.s = UpdatePart.UpdateUi()
        self.s.show()

    #新增按钮
    def onAddClick(self):
        # self.hide() #隐藏主窗口
        self.s = AddPart.AddUi(self.excel_file)
        self.s.show()

    #减少按钮
    def onSubClick(self):
        # self.hide()
        self.s = SubPart.SubUi(self.excel_file,self.csv_file)
        self.s.show()

    #退出应用程序
    def onQuitClick(self):
        sender = self.sender()
        app = QApplication.instance()
        app.quit()

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()