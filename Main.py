#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys
from calendrier_fond import *
import fbchat
from fbchat.models import *
from getpass import getpass


import json

RestrictedHorizontaly = True

# #comment test commit from vscode
# noPen = QPen(QColor(100,0,255,0))
# myBrush = QBrush(QColor(100,0,255))
# noBrush = QBrush(QColor(100,0,250,0))

# dayColor = QBrush(QColor(48,114,172))


def jsonDefault(GraphW):
        return GraphW.__dict__

# class Communicate(QObject):
#     addRDV = pyqtSignal(str)

class Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.MW = MainW(self)
        self.setCentralWidget(self.MW)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        editMenu = menubar.addMenu('&Edit')
        
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAct.setShortcut('Esc')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        fileMenu.addAction(exitAct)

        saveAct = QAction('Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('save application')
        saveAct.triggered.connect(lambda: self.MW.Graph.jsonSave())

        fileMenu.addAction(saveAct)

        delAct = QAction('Delete', self)
        delAct.setShortcut('Del')
        delAct.setStatusTip('Delete event')
        delAct.triggered.connect(lambda: self.MW.Graph.scene.delEvent())
        
        editMenu.addAction(delAct)

        

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('~~-=# P  O  F #=-~~')    
        self.setWindowIcon(QIcon('pof.png')) 
        self.show()
        self.MW.show()



class MainW(QWidget):

    def __init__(self, Parent):
        super().__init__(Parent)
        
        self.initUI()
    
    # simpleSig = pyqtSignal()
    # c = Communicate()
    # GSIGNAL = False
        
    def initUI(self):
        
        self.Graph = GraphW(self)


        
        # self.c.addRDV.connect(self.Graph.cal.AddRDVPrint)
        
        # self.simpleSig.connect(self.simpleSlot)
        #self.GSIGNAL.connect(self.thisIsLocal)
        

        self.Menu = MenuW(self)#, self.simpleSig )
        # self.Menu.simpleSig2.connect(self.simpleSlot)


        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.Graph, *(1,1))
        self.grid.addWidget(self.Menu, *(1,2))

        #self.move(300, 150)
        self.Menu.show()
        self.Graph.show()
        self.show()

    
    # def simpleSlot(argumentInutile):
    #     print("hello")
    #     self.GSIGNAL = True
        #self.AddRDVDialog()

    # def thisIsLocal():
    #     self.AddRDVDialog()

    #@staticmethod
    def AddRDVDialog(Selfe):
        print("hello2")

        dialog = RDVDialog(parent = Selfe)
        dialog.exec_()
        data = dialog.return_strings()
        Selfe.Graph.cal.addOneRDV(data[0],data[1], data[2], data[3])
        Selfe.Graph.scene.addItem(Selfe.Graph.cal.getItemQueue())
        # map(str, [self.q1Edit.text(), self.q2Edit.text()])

    def EditRDV(Selfe):
        try:
            RDV = Selfe.Graph.scene.selectedItems()[0]
        except IndexError:
            print("Pas de RDV sélectionné")
            return

        dialog = RDVDialogEdit(RDV, parent = Selfe)
        dialog.exec_()
        data = dialog.return_strings()
        Selfe.Graph.cal.addOneRDV(data[0],data[1], data[2], data[3])
        Selfe.Graph.scene.addItem(Selfe.Graph.cal.getItemQueue())
        Selfe.Graph.scene.removeItem(RDV)





class MenuW(QWidget):

    # simpleSig2 = pyqtSignal()
    
    def __init__(self, Parent):#, simplSig):
        self.Parent = Parent
        super().__init__(self.Parent)
        self.initUI(self.Parent)#, simplSig)
        
    def initUI(self, Parent):#, simplSig):
        self.grid = QGridLayout()
        self.setLayout(self.grid)
 
        """ names = ['Ajout RDV', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']
        
        positions = [(i,j) for i in range(5) for j in range(4)]
        
        for position, name in zip(positions, names):
            
            if name == '':
                continue
            button = QPushButton(name)
            button.clicked.connect(lambda: self.buttonClicked())
            self.grid.addWidget(button, *position) """
        
        button = QPushButton("Ajout RDV")
        button.clicked.connect(lambda: self.addRDV())
        self.grid.addWidget(button, 1,1)

        button2 = QPushButton("Edit RDV")
        button2.clicked.connect(lambda: self.EditRDV())
        self.grid.addWidget(button2, 1,2)

        button3 = QPushButton("Export PDF")
        button3.clicked.connect(lambda: self.exportPDF())
        self.grid.addWidget(button3, 2,1)

        #self.move(300, 150)
        self.show()


    def addRDV(self):
        self.Parent.AddRDVDialog()
    
    def EditRDV(self):
        self.Parent.EditRDV()

    def exportPDF(self):
        self.Parent.Graph.exportPDF()




        
class GraphW(QGraphicsView):
    def __init__(self, Parent):
        super().__init__(Parent)
        self.initUI()
    
    def initUI(self):
        self.scene = aScene()
        pen = QPen(Qt.red)
        self.scene.setBackgroundBrush(BrushBg)
        self.setScene(self.scene)
        shadowRect = QGraphicsRectItem(-40000,0,80000,1)
        shadowRect.setPen(noPen)
        shadowRect.setBrush(noBrush)
        self.rectangle = QGraphicsRectItem(30,10,50,50)
        self.scene.addItem(shadowRect) # dessine le rectangle
        self.scene.addItem(self.rectangle)
        #self.scene.addText()
        self.setFocusPolicy(Qt.WheelFocus)
        self.setRenderHints(QPainter.Antialiasing)
        self.S_Pressed = False
        self.middlePressed = False
        self.rightPressed = False
        """ button = QPushButton('Hello !')
        button.clicked.connect(lambda: self.hello())
        self.scene.addWidget(button) """
    
        self.cal = calendrier()
        for i in self.cal.items:
            self.scene.addItem(i)
        """ button = QPushButton('Hello !')
        button.clicked.connect(lambda: self.hello())
        self.scene.addWidget(button)  """

    def addRDV(name, date, time, duree):
        self.cal.AddRDV(name, date, time, duree)

    def jsonSave(self):
        items = self.scene.items()
        RDVs = []
        for item in items:
            if type(item) == RDV:
                RDVs.append(item)
        jsonScene = json.dumps(RDVs, default = jsonDefault, indent=4)
        file= open("saved data.txt","w+")
        file.write(jsonScene)
        file.close()

        """ grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self., 1, 0, 50, 1)
        
        self.setLayout(grid)  """

    #lorsque j'affiche un bouton, permet au clic de pop une fenetre 'hello'
        
    def hello(self):
        reply = QMessageBox()
        reply.setText("hello!!!")
        reply.exec_()

    #override de la fonction premier plan pour dessiner des items flottants au dessus de la partie zoomable
    def drawForeground(self, painter, rect):
        #super(GraphW, self).drawForeground( painter, rect)
        #painter.resetTransform()
        button = QPushButton('Hello !')
        button.clicked.connect(lambda: self.hello())
        #self.rectangle.setPos(rect.x() +10 , rect.y() + 10 )
        #button.setPos(100,100)
        #self.scene.addWidget(button)
        #self.scene.addItem(rectangle)

            
    #overrides des fonctions de gestion d'évents (l'héritage est commenté pour wheel car un scroll s'ajoute au zoom sinon)

    def wheelEvent(self, event):
        #super(GraphW, self).wheelEvent(event)
        self.newScale(event.angleDelta().y(), 1.15)

    def keyPressEvent(self, event):
        super(GraphW, self).keyPressEvent(event)
        if event.key() == Qt.Key_S:
            self.S_Pressed = True
            QApplication.setOverrideCursor(Qt.OpenHandCursor)

    def keyReleaseEvent(self, event):
        super(GraphW, self).keyReleaseEvent(event)
        if event.key() == Qt.Key_S:
            self.S_Pressed = False
            QApplication.setOverrideCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        super(GraphW, self).mousePressEvent(event)
        self._dragPos = event.pos()
        if event.button() == Qt.MidButton:
            self.middlePressed = True
        if event.button() == Qt.RightButton:
            self.rightPressed = True
        self.lastPoint = event.pos()
        
    def mouseReleaseEvent(self, event):
        super(GraphW, self).mouseReleaseEvent(event)
        if event.button() == Qt.MidButton:
            self.middlePressed = False
        if event.button() == Qt.RightButton:
            self.rightPressed = False

    def mouseMoveEvent(self, event):
        super(GraphW, self).mouseMoveEvent(event)
        if True: #self.S_Pressed:
            newPos = event.pos()

            if self.middlePressed:
                diff = newPos - self._dragPos
                self._dragPos = newPos
                QApplication.setOverrideCursor(Qt.ClosedHandCursor)
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
                self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
                event.accept()
            """ if self.rightPressed:
                diff = newPos - self._dragPos
                self._dragPos = newPos
                QApplication.setOverrideCursor(Qt.SizeAllCursor)
                self.newScale(diff.x(), 1.01) """

    def newScale(self, operator, factor):
        if operator > 0:
            self.scale(factor, factor)
        if operator < 0:
            self.scale(1.0/factor, 1.0/factor)

    def exportPDF(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPaperSize(QPrinter.A4);
        printer.setOrientation( QPrinter.Portrait )
        printer.setOutputFormat( QPrinter.PdfFormat )
        printer.setOutputFileName( "/home/vince/Bureau/test.pdf" )
        painter = QPainter();
        #printDialog = QPrintDialog(printer, self)
        if (painter.begin(printer)):#printDialog.exec() == QDialog.Accepted):
            width = wWeek * 1.1 #self.scene.itemsBoundingRect().width()
            totHeight = self.scene.itemsBoundingRect().height() // 2 - 500
            pHeight = 1.5 * width
            nPages = totHeight // pHeight
            for i in range(0, int(nPages)):
                target = QRectF(-50,-50 + pHeight*i,width, pHeight)
                renderedPage = self.scene.render(painter, QRectF(0,0,0,0), target )
                printer.newPage()
            
            #painter.drawPixmap(768, 1024, screen)
            painter.end()
        

        # no_of_friends = int(raw_input("Number of friends: ")) 
        # for i in xrange(no_of_friends): 
        #     name = str(raw_input("Name: ")) 
        #     friends = client.getUsers(name)  # return a list of names 
        #     friend = friends[0] 
        #     
        #     
        #     if sent: 
        #         print("Message sent successfully!")

        # self.render(painter);



        

class RDVDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(parent)
        self.Parent = parent
        super().__init__(self.Parent)
        self.initUI(parent)
        
        
    def initUI(self, parent):
        grid = QGridLayout(parent)
        grid.setSpacing(3)

        self.edit_1 = QTextEdit()
        grid.addWidget(QLabel('Titre'), 1, 0)
        grid.addWidget(self.edit_1, 1, 1)

        #   add layout for second widget
        self.edit_2 = QLineEdit()
        grid.addWidget(QLabel('Date'), 2, 0)
        grid.addWidget(self.edit_2, 2, 1)

        #   add layout for widget 3
        self.edit_3 = QLineEdit()
        grid.addWidget(QLabel('Heure'), 3, 0)
        grid.addWidget(self.edit_3, 3, 1)

        #   add layout for widget 4
        self.edit_4 = QLineEdit()
        grid.addWidget(QLabel('Durée'), 4, 0)
        grid.addWidget(self.edit_4, 4, 1)

        apply_button = QPushButton('Apply')#, self)
        apply_button.clicked.connect(self.close)

        grid.addWidget(apply_button, 6, 3)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.show()

    def return_strings(self):
        #   Return list of values. It need map with str (self.lineedit.text() will return QString)
        #mappe = map(str, [self.edit_1.text(), self.edit_2.text(), self.edit_3.text(), self.edit_4.text()])
        
        Name = str(self.edit_1.toPlainText())
        
        listDate = list(map(int,str(self.edit_2.text()).split("/")))
        if listDate[2]<100 :
            listDate[2] = listDate[2] + 2000
        date = Date(listDate[0],listDate[1], listDate[2])

        listTime = list(map(int,str(self.edit_3.text()).split("h")))
        time = Time(listTime[0], listTime[1])

        listTime = list(map(int,str(self.edit_4.text()).split("h")))
        duree = Time(listTime[0], listTime[1])

        return [Name, date, time, duree]




class RDVDialogEdit(QDialog):
    def __init__(self, leRDV, parent = None):
        QDialog.__init__(parent)
        self.Parent = parent
        super().__init__(self.Parent)
        self.initUI(parent, leRDV)
    
    def initUI(self, parent, leRDV):
        grid = QGridLayout(parent)
        grid.setSpacing(3)

        self.edit_1 = QTextEdit()
        self.edit_1.setText(leRDV.name)
        grid.addWidget(QLabel('Titre'), 1, 0)
        grid.addWidget(self.edit_1, 1, 1)

        #   add layout for second widget
        self.edit_2 = QLineEdit()
        self.edit_2.setText(leRDV.date.toString())
        grid.addWidget(QLabel('Date'), 2, 0)
        grid.addWidget(self.edit_2, 2, 1)

        #   add layout for widget 3
        self.edit_3 = QLineEdit()
        self.edit_3.setText(str(leRDV.time.toString()))
        grid.addWidget(QLabel('Heure'), 3, 0)
        grid.addWidget(self.edit_3, 3, 1)

        #   add layout for widget 4
        self.edit_4 = QLineEdit()
        self.edit_4.setText(str(leRDV.duree.toString()))
        grid.addWidget(QLabel('Durée'), 4, 0)
        grid.addWidget(self.edit_4, 4, 1)

        apply_button = QPushButton('Apply')#, self)
        apply_button.clicked.connect(self.close)

        grid.addWidget(apply_button, 6, 3)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.show()
 
    def return_strings(self):
        #   Return list of values. It need map with str (self.lineedit.text() will return QString)
        #mappe = map(str, [self.edit_1.text(), self.edit_2.text(), self.edit_3.text(), self.edit_4.text()])
        
        Name = str(self.edit_1.toPlainText())
        
        listDate = list(map(int,str(self.edit_2.text()).split("/")))
        if listDate[2]<100 :
            listDate[2] = lisDate[2] + 2000
        date = Date(listDate[0],listDate[1], listDate[2])

        listTime = list(map(int,str(self.edit_3.text()).split("h")))
        time = Time(listTime[0], listTime[1])

        listTime = list(map(int,str(self.edit_4.text()).split("h")))
        duree = Time(listTime[0], listTime[1])

        return [Name, date, time, duree]




    #@staticmethod
    """ def get_data(parent=None):
        dialog = AddRDVDialog(parent)
        dialog.exec_()
        return dialog.return_strings()
 """

class aScene(QGraphicsScene):
    def __init__(self, parent = None):
        self.Parent = parent
        super().__init__(self.Parent)
        self.lastPoint = QPointF(0,0)
        self.mousePressed = False
    
    def mousePressEvent(self, event):
        super(aScene, self).mousePressEvent(event)
        self.lastPoint =QPointF(event.pos().x() ,event.scenePos().y() - event.pos().y())
        self.mousePressed = True
        #print("m")

    def mouseReleaseEvent(self, event):
        super(aScene, self).mouseReleaseEvent(event)
        self.mousePressed = False
    
    def mouseMoveEvent(self, event):
        #super(aScene, self).mouseMoveEvent(event)
        if RestrictedHorizontaly and self.mousePressed: # boolean to trigger weather to restrict it horizontally 
            x = event.scenePos().x() - self.lastPoint.x()
            y = self.lastPoint.y() #+ event.pos().y()
            for item in self.selectedItems():
                item.setPos(QPointF(x,y))# which is the QgraphicItem that you have or selected before
                #print("x: " + str(event.pos().x())+ " y : " + str(y))

    def delEvent(self):
        for item in self.selectedItems():
            self.removeItem(item)
            print("deleted")







#boucle principale
if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = Test()
    sys.exit(app.exec_())
    

