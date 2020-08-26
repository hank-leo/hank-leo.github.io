import pandas as pd
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import MainFunc

class AddUi(QWidget):
    def __init__(self,path=None):
        super(AddUi, self).__init__()
        self.init_ui()
 
    def init_ui(self):
        self.resize(500, 350)
        self.setWindowTitle('新增部分')
        self.btn = QPushButton('返回主页', self)
        self.btn.setGeometry(150, 150, 100, 50)
        self.btn.clicked.connect(self.slot_btn_function)

    def slot_btn_function(self):
        self.hide()
        self.f = MainFunc.MainWindow()
        self.f.show()