import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QPushButton , QVBoxLayout , QGridLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton , QErrorMessage , QMessageBox
from PyQt5.QtCore import QSize
from PyQt5 import QtCore , QtGui
from queue import PriorityQueue
import time

class random_path_Generator(QPushButton) :
    def __init__(self , buttonlist):
        super(random_path_Generator, self).__init__()
        self.setText("Generate a Path")
        self.buttonlist=buttonlist
        self.clicked.connect(self.on_clicked)

        self.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}"
                           "QPushButton"
                           "{"
                           "background-color : lightblue;"
                           "}"
                           "QPushButton::pressed"
                           "{"
                           "background-color : yellow;"
                           "}"
                           )

    def on_clicked (self) :
        self.unixtime=int(time.time())
        for i in range(1, 21):
            for j in range(1, 31):
                if i == 1 or j == 30 or i == 20 or j == 1:
                    pass
                else:
                    if self.buttonlist[j][i].colorstat != "red" and self.buttonlist[j][i].colorstat != "green" and self.buttonlist[j][i].colorstat != "gray":
                        randtime=(self.unixtime*i*j)%100
                        if randtime > 65 :
                            self.buttonlist[j][i].colorstat = "gray"
                            self.buttonlist[j][i].visiting = False
                            self.buttonlist[j][i].f_cost = float('inf')
                            self.buttonlist[j][i].g_cost = float('inf')
                            self.buttonlist[j][i].setText("")
                            self.buttonlist[j][i].setStyleSheet("background-color : gray;")
                            self.count = 0
                            self.queue = []
                        else :
                            self.buttonlist[j][i].colorstat = "white"
                            self.buttonlist[j][i].visiting = False
                            self.buttonlist[j][i].f_cost = float('inf')
                            self.buttonlist[j][i].g_cost = float('inf')
                            self.buttonlist[j][i].setText("")
                            self.buttonlist[j][i].setStyleSheet("background-color : white;")
                            self.count = 0
                            self.queue = []


                    elif self.buttonlist[j][i].colorstat != "red" and self.buttonlist[j][i].colorstat != "green"  :
                        self.buttonlist[j][i].colorstat = "white"
                        self.buttonlist[j][i].visiting = False
                        self.buttonlist[j][i].f_cost = float('inf')
                        self.buttonlist[j][i].g_cost = float('inf')
                        self.buttonlist[j][i].setText("")
                        self.buttonlist[j][i].setStyleSheet("background-color : white;")
                        self.count = 0
                        self.queue = []


class Clear_Screen(QPushButton):
    def __init__(self , buttonlist):
        super(Clear_Screen, self).__init__()
        self.setText("Clear Screen")
        self.buttonlist=buttonlist
        self.clicked.connect(self.on_clicked)
        self.setStyleSheet("QPushButton::hover"
                             "{"
                             "background-color : lightgreen;"
                             "}"
                           "QPushButton"
                           "{"
                           "background-color : lightblue;"
                           "}"
                           "QPushButton::pressed"
                           "{"
                           "background-color : yellow;"
                           "}"
                           )

    def on_clicked(self):
        for i in range(1, 21):
            for j in range(1, 31):
                if i == 1 or j == 30 or i == 20 or j == 1:
                    pass
                else:
                    if self.buttonlist[j][i].colorstat != "red" and self.buttonlist[j][i].colorstat != "green":
                        self.buttonlist[j][i].colorstat = "white"
                        self.buttonlist[j][i].visiting = False
                        self.buttonlist[j][i].f_cost = float('inf')
                        self.buttonlist[j][i].g_cost = float('inf')
                        self.buttonlist[j][i].setText("")
                        self.buttonlist[j][i].setStyleSheet("background-color : white;")
                        self.count = 0
                        self.queue = []


