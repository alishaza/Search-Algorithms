import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget , QPushButton , QVBoxLayout , QGridLayout
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton , QErrorMessage , QMessageBox
from PyQt5.QtCore import QSize
from queue import PriorityQueue
import time
import os
from RandomPath import random_path_Generator , Clear_Screen

class start_end():
    def __init__(self):
        self.start=None
        self.end=None

class TimeLabel(QLabel):
    def __init__(self):
        super(TimeLabel, self).__init__()
        self.show()

class buttoms(QPushButton):
    def __init__(self , color , col , row, combo , stat):
        super(buttoms, self).__init__()
        self.size()
        # colors backtrack , red , green , gray , yellow
        self.colorstat=color
        self.visiting=False
        self.setMinimumSize(QSize(30,20))
        self.setStyleSheet("background-color : %s;" % color)
        #end and start = stat obj
        self.stat=stat
        self.column = col
        self.row=row
        self.combo=combo
        self.clicked.connect(self.btn_clicked)
        # for A* Algorithm
        # f=h+g
        self.g_cost=float('inf')
        self.f_cost=float('inf')

    # for comparison
    def __lt__(self, other):
        return True


    def btn_clicked (self) :
        Clickedbtn=self.sender()
        color=self.combo.currentText()
        if (self.stat.start==None and color=="green"):
             # zamani ke taze shoro be entekahb mishe
             Clickedbtn.setStyleSheet("background-color : %s;"%color )
             self.stat.start=Clickedbtn
             Clickedbtn.colorstat = color
             Clickedbtn.setStyleSheet("background-color : %s"%color)

        if (self.stat.end==None and color=="red"):
            # zamani ke taze shoro be entekahb mishe
            Clickedbtn.setStyleSheet("background-color : %s;" % color)
            self.stat.end = Clickedbtn
            Clickedbtn.colorstat = color
            Clickedbtn.setStyleSheet("background-color : %s" % color)

        if (self.stat.start!=None and color=="green"):
            #entekhab ghabli ro pak mikone va oon ro white mikone
            self.stat.start.setStyleSheet("background-color : white")
            self.stat.start.colorstat = "white"
            self.stat.start = Clickedbtn

            #entekhab jadid ro jay gozin mikone va oon ro ba rang morede nazar poor mikone
            Clickedbtn.setStyleSheet("background-color : %s;" % color)
            Clickedbtn.colorstat = color
            Clickedbtn.setStyleSheet("background-color : %s" % color)

        if (self.stat.end != None and color == "red"):
            #entekhab ghabli ro pak mikone va oon ro white mikone
            self.stat.end.setStyleSheet("background-color : white")
            self.stat.end.colorstat = "white"
            self.stat.end=Clickedbtn

            #entekhab jadid ro jay gozin mikone va oon ro ba rang morede nazar poor mikone
            Clickedbtn.setStyleSheet("background-color : %s;" % color)
            Clickedbtn.colorstat = color
            Clickedbtn.setStyleSheet("background-color : %s" % color)

        else :
            # dar baghie halat mohem nist chand ta rang gray ya white darim
            Clickedbtn.setStyleSheet("background-color : %s;" % color)
            Clickedbtn.colorstat = color
            Clickedbtn.setStyleSheet("background-color : %s" % color)


class cell_color(QComboBox):
    def __init__(self):
        super(cell_color, self).__init__()
        self.addItem("green")
        self.addItem("red")
        self.addItem("gray")
        self.addItem("white")


class Algorithm(QComboBox):
    def __init__(self):
        super(Algorithm, self).__init__()
        self.addItem("DFS")
        self.addItem("BFS")
        self.addItem("A*")

class Simple_Text(QLabel):
    def __init__(self , text):
         super(Simple_Text, self).__init__()
         self.setText(text)
        
class opennode_text(QLabel):
    def __init__(self):
        super(opennode_text, self).__init__()

class Export_to_CSV(QPushButton):
    def __init__(self , cal_btn_info):
        super(Export_to_CSV, self).__init__()
        self.setText("Export to CSV")
        self.cal_btn_info=cal_btn_info
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
        try :
            if os.path.exists('output.csv'):
               os.remove('output.csv')
            file=open("output.csv" , 'a' )
            file.writelines("Time order,Open nodes,Algorithm\n")
            for index in self.cal_btn_info:
                file.writelines("%s,"%index[0]+"%s"%index[1]+",%s\n"%index[2])
        except:
            pass






class Calculate_Button(QPushButton):
    def __init__(self , algorithm  , buttonlist , start_end_buttons , timelabel , OP_nodes_label):
        super(Calculate_Button, self).__init__()
        # For CSV file
        self.Output_to_CSV=[]

        self.setText("calculate")
        self.clicked.connect(self.find_path)
        self.algorithm , self.buttonlist , self.start_end_buttons = (algorithm , buttonlist , start_end_buttons)
        # counter for Search walk
        self.count=0
        #Queue for BFS
        self.queue=[]

        #Opened Nodes
        self.opened_nodes=0
        self.OP_nodes_label=OP_nodes_label

        #label for time order
        self.timelabel=timelabel


    def __getitem__(self, index):
        return self.Output_to_CSV[index]


    def find_path(self):
        for i in range(1, 21):
            for j in range(1, 31):
                if i == 1 or j == 30 or i == 20 or j == 1:
                    pass
                else:
                    if self.buttonlist[j][i].colorstat != "red" and self.buttonlist[j][i].colorstat != "green" and self.buttonlist[j][i].colorstat != "gray" :
                        self.buttonlist[j][i].colorstat = "white"
                        self.buttonlist[j][i].visiting = False
                        self.buttonlist[j][i].f_cost = float('inf')
                        self.buttonlist[j][i].g_cost = float('inf')
                        self.buttonlist[j][i].setText("")
                        self.buttonlist[j][i].setStyleSheet("background-color : white;")
                        self.count=0
                        self.queue=[]
                    else :
                        self.buttonlist[j][i].f_cost = float('inf')
                        self.buttonlist[j][i].g_cost = float('inf')
                        self.buttonlist[j][i].visiting = False
                        self.buttonlist[j][i].setText("")
                        self.buttonlist[j][i].setText("")


        s_time = time.time()

        algo=self.algorithm.currentText()

        if self.start_end_buttons.start != None and self.start_end_buttons.end!=None :
            if algo == "DFS" :
                self.DFS(self.start_end_buttons.start , self.start_end_buttons.end)
            if algo == "BFS" :
                self.BFS(self.start_end_buttons.start , self.start_end_buttons.end )
            if algo == "A*" :
                self.AStar(self.start_end_buttons.start , self.start_end_buttons.end)

            e_time = time.time()
            total_time = e_time - s_time
            self.timelabel.setText("Approximate time :%s ms" % format(total_time, ".3f"))
            self.OP_nodes_label.setText("open nodes : %s"%self.opened_nodes)

            self.Output_to_CSV.append((total_time , self.opened_nodes , algo))
            # Restart
            self.opened_nodes = 0

        else :
            error_dialog = QMessageBox()
            error_dialog.about(self,"Error","You must define the start and end points")


    def DFS(self , current , end ):
        self.count+=1
        self.opened_nodes+=1

        current_column = current.column
        current_row=current.row
        #up down right left node diogniose
        upnode = self.buttonlist[ current_column][current_row-1 ]
        downnode = self.buttonlist[current_column] [current_row + 1]
        rightnode= self.buttonlist[current_column + 1][ current_row ]
        leftnode= self.buttonlist[current_column -1][current_row ]

        #leftnode.setStyleSheet("background-color : blue;")
        if current == end :
            self.count=0
            return True
        #if upnode.visiting == False and upnode.colorstat != "black" :
        if upnode.visiting == False and upnode.colorstat != "gray" and upnode.colorstat != "green" :
            if upnode.colorstat !="red" :
                upnode.colorstat = "yellow"
                upnode.visiting=True
                upnode.setStyleSheet("background-color : yellow")
                upnode.setText("%s"%self.count)

            if self.DFS(upnode,end) :
                self.count = 0
                return True

        if rightnode.visiting == False and rightnode.colorstat != "gray" and rightnode.colorstat != "green" :
            if rightnode.colorstat !="red" :
                rightnode.colorstat = "yellow"
                rightnode.visiting=True
                rightnode.setStyleSheet("background-color : yellow")
                rightnode.setText("%s"%self.count)

            if self.DFS(rightnode,end) :
                self.count = 0
                return True

        if downnode.visiting == False and downnode.colorstat != "gray" and downnode.colorstat != "green":
            if downnode.colorstat != "red":
                downnode.colorstat = "yellow"
                downnode.visiting = True
                downnode.setStyleSheet("background-color : yellow")
                downnode.setText("%s"%self.count)

            if self.DFS(downnode, end) :
                self.count = 0
                return True

        if leftnode.visiting == False and leftnode.colorstat != "gray" and leftnode.colorstat != "green":
            if leftnode.colorstat != "red":
                leftnode.colorstat = "yellow"
                leftnode.visiting = True
                leftnode.setStyleSheet("background-color : yellow")
                leftnode.setText("%s"%self.count)

            if self.DFS(leftnode, end) :
                self.count = 0
                return True
        if current != self.start_end_buttons.start :
            current.setStyleSheet("background-color : #EFDECD;")
        self.count-=1
        current.setText("")
        if self.count == 0 :
            error_dialog = QMessageBox()
            error_dialog.about(self,"Error","No Path were found!")




    def BFS(self , current , end):

        self.count+=1
        Start=current
        ReversePath={}

        if ( self.count == 1 ) :
          self.buttonlist[current.column][current.row].visiting=True
          self.queue.append(current)

        while self.queue :
            self.count+=1
            self.opened_nodes+=1

            current = self.queue.pop(0)

            if current !=Start :
                current.setStyleSheet("background-color : #EFDECD;")

            current_column = current.column
            current_row = current.row
            # up down right left node diogniose
            upnode = self.buttonlist[current_column][current_row - 1]
            downnode = self.buttonlist[current_column][current_row + 1]
            rightnode = self.buttonlist[current_column + 1][current_row]
            leftnode = self.buttonlist[current_column - 1][current_row]


            if current == end :
                break
            elif leftnode == end :
                ReversePath[leftnode] = current
                break
            elif rightnode == end :
                ReversePath[rightnode] = current
                break
            elif upnode == end :
                ReversePath[upnode] = current
                break
            elif downnode == end :
                ReversePath[downnode] = current
                break

            # up right down left
            if upnode.visiting == False and upnode.colorstat != "gray":
                if upnode.colorstat != "red":
                    upnode.colorstat = "yellow"
                    upnode.visiting = True

                    self.queue.append(upnode)
                    ReversePath[upnode] = current



            if rightnode.visiting == False and rightnode.colorstat != "gray":
                if rightnode.colorstat != "red":
                    rightnode.colorstat = "yellow"
                    rightnode.visiting = True

                    self.queue.append(rightnode)
                    ReversePath[rightnode]=current

            if downnode.visiting == False and downnode.colorstat != "gray":
                if downnode.colorstat != "red":
                    downnode.colorstat = "yellow"
                    downnode.visiting = True

                    self.queue.append(downnode)
                    ReversePath[downnode] = current

            if leftnode.visiting == False and leftnode.colorstat != "gray":
                if leftnode.colorstat != "red":
                    leftnode.colorstat = "yellow"
                    leftnode.visiting = True

                    self.queue.append(leftnode)
                    ReversePath[leftnode] = current

        RealPath={}
        cell= end
        count=0
        Path=[]

        while cell!=Start :
            try :
                RealPath[ReversePath[cell]]=cell
            except KeyError :
                error_dialog = QMessageBox()
                error_dialog.about(self,"Error","No Path were found!")
                return False
            cell = ReversePath[cell]
        for button in RealPath :
            if button != Start :
                Path.append(button)
                button.colorstat="yellow"
                button.setStyleSheet("background-color : yellow;" )

        for button in reversed(Path) :
            count += 1
            button.setText("%s" % count)




    def h(self , cell1 , cell2  ):
        x1,y1 = cell1.column , cell1.row
        x2, y2 = cell2.column, cell2.row

        return abs(x1-x2) + abs(y2-y1)



    def AStar(self , current , end ):


        Start=current

        current.g_cost=0
        current.f_cost=self.h(current , end)
        Queue=PriorityQueue()
        #Priority Queue = f_cost , h_cost , current node(start node)
        Queue.put((self.h(current,end)+0 ,self.h(current,end) , current ))


        ReversePath = {}
        while not Queue.empty() :
            current=Queue.get()[2]
            self.opened_nodes+=1

            current_column = current.column
            current_row = current.row
            # up down right left node diogniose
            upnode = self.buttonlist[current_column][current_row - 1]
            downnode = self.buttonlist[current_column][current_row + 1]
            rightnode = self.buttonlist[current_column + 1][current_row]
            leftnode = self.buttonlist[current_column - 1][current_row]

            if current == end :
                break
            if upnode.colorstat != "gray":
                temp_g_cost=current.g_cost+1
                temp_f_cost= temp_g_cost+self.h(upnode , end)

                if temp_f_cost < upnode.f_cost :
                    upnode.f_cost = temp_f_cost
                    upnode.g_cost= temp_g_cost
                    Queue.put((temp_f_cost  , self.h(upnode , end) , upnode))
                    #upnode.setStyleSheet("background-color : #EFDECD;")
                    ReversePath[upnode]=current


            if downnode.colorstat != "gray":
                temp_g_cost = current.g_cost + 1
                temp_f_cost = temp_g_cost + self.h(downnode, end)

                if temp_f_cost < downnode.f_cost:
                    downnode.f_cost = temp_f_cost
                    downnode.g_cost = temp_g_cost
                    Queue.put((temp_f_cost,  self.h(downnode , end), downnode))
                    ReversePath[downnode]=current


            if rightnode.colorstat != "gray":
                temp_g_cost = current.g_cost + 1
                temp_f_cost = temp_g_cost + self.h(rightnode, end)

                if temp_f_cost < rightnode.f_cost:
                    rightnode.f_cost= temp_f_cost
                    rightnode.g_cost = temp_g_cost
                    Queue.put((temp_f_cost, self.h(rightnode , end), rightnode))
                    ReversePath[rightnode]=current


            if leftnode.colorstat != "gray":
                temp_g_cost = current.g_cost + 1
                temp_f_cost = temp_g_cost + self.h(leftnode, end)

                if temp_f_cost < leftnode.f_cost:
                    leftnode.f_cost = temp_f_cost
                    leftnode.g_cost = temp_g_cost
                    Queue.put((temp_f_cost, self.h(leftnode , end), leftnode))
                    ReversePath[leftnode]=current
            if current !=end and current != Start :
                current.setStyleSheet("background-color : #EFDECD;")

        RealPath={}
        cell= end
        count=0
        Path=[]

        while cell!=Start :
            try :
                RealPath[ReversePath[cell]]=cell
            except KeyError:
                error_dialog = QMessageBox()
                error_dialog.about(self,"Error","No Path were found!")
                return False

            cell=ReversePath[cell]
        for button in RealPath :
            if button != Start :
                Path.append(button)
                button.colorstat="yellow"
                button.setStyleSheet("background-color : yellow;" )

        for button in reversed(Path) :
            count += 1
            button.setText("%s" % count)





class MainWindow(QMainWindow):
    def __init__(self):

        stat=start_end()
        self.ButtonList = self.ArrayConstruction()
        app = QApplication(sys.argv)
        win = QWidget()
        grid = QGridLayout()


        self.combocolor = cell_color()
        self.algo_choise=Algorithm()


        for i in range(1, 21):
            for j in range(1, 31):
                if i == 1 or j == 30 or i ==20 or j == 1 :
                    btn=buttoms("gray" , j , i , self.combocolor , stat)
                    grid.addWidget(btn, i, j)
                    grid.setSpacing(0)
                    self.ButtonList[j][i] = btn
                else :
                    btn = buttoms("white" , j , i , self.combocolor, stat)
                    grid.addWidget(btn, i, j)
                    grid.setSpacing(0)
                    self.ButtonList[j][i]=btn

        self.cal_time = TimeLabel()
        self.OP_nodes = opennode_text()
        self.cal_btn = Calculate_Button(self.algo_choise , self.ButtonList , stat, self.cal_time , self.OP_nodes)



        grid.addWidget(Simple_Text("color select :"), 21, 1 , 4 ,2)
        grid.addWidget(self.combocolor, 21 , 4 ,4 ,2 )
        grid.addWidget(Simple_Text("choose algorithm :"), 21, 8 , 4 ,3 )
        grid.addWidget(self.algo_choise, 21, 12, 4 , 2 )
        grid.addWidget(self.cal_btn, 21, 18 , 4 , 3 )
        grid.addWidget(self.cal_time, 21, 25 , 4 ,6)

        grid.addWidget(random_path_Generator(buttonlist=self.ButtonList), 25, 1 , 3 ,3)
        grid.addWidget(Clear_Screen(buttonlist=self.ButtonList), 25, 4, 3, 3)
        grid.addWidget(self.OP_nodes, 25, 25 , 4 ,6)
        grid.addWidget(Export_to_CSV(cal_btn_info=self.cal_btn), 25, 7 , 4 ,6)




        win.setLayout(grid)
        win.setGeometry(100, 100, 200, 100)
        win.setWindowTitle("AI Project - Ali Shazaei")
        win.show()
        sys.exit(app.exec_())


    def ArrayConstruction (self) :
        ListOfButtons = [[1 for j in range(21)] for i in range(31)]
        return ListOfButtons








if __name__ == '__main__':
    MainWindow()



