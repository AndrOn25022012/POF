#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import sys
from timeUtils import *
import json

#pens (contour) et brushs (fond) globaux
noPen = QPen(Qt.NoPen)
penHourLines = QPen(QColor(214, 205, 188))
penDay = noPen
penRDV = noPen
penSem = noPen


# Brushes
# myBrush = QBrush(QColor(100,0,255))
noBrush = QBrush(Qt.NoBrush)
BrushDay = QBrush(QColor(70,170,169))
BrushBg = QBrush(QColor(236,226,208))
brushRDV = QBrush(QColor(48,116,115))
brushSem = QBrush(QColor(134,216,215))
brushTextSem = QBrush(QColor(236,226,208, 200))
brushTexte = QBrush(Qt.white)
brushCurDay = QBrush(QColor(109,201,106))
brushHourBg = QBrush(QColor(27,42,65))


brushRDVtxt = QBrush(Qt.white) #deprecated
colorRDVtxt = QColor(255,255,255)





class calendrier():




    def __init__(self):

        #currentDateTime 
        self.curDT = QDateTime.currentDateTime()
        self.curD = QDate.currentDate()
        
        self.curMonth = self.curDT.toString('MMMM')
        self.curMonthNum = self.curDT.toString('M')
        self.curDay = self.curDT.toString('dddd')
        self.curDayNum = self.curDT.toString('d')
        self.curWD = self.curD.dayOfWeek()
        self.curYear = self.curDT.toString('yyyy')

        self.dateActuel = Date( int(self.curDayNum),int(self.curMonthNum),int(self.curYear))

        self.items = []
        self.itemQueue = []

        for i in range(-100,100):

            day = CDay(self.dateActuel.addDays(i), BrushDay)
            day.setPos(0,i*280   +   80*((i+self.curWD)//7))
            #           nbjours        nbdimanches
            if(i == 0):
                day.setBrush(brushCurDay)

            if day.day == "Sunday" or day.day == "dimanche":
                rectSem = QGraphicsRectItem(0,0,900,280*7-5+75)
                rectSem.setBrush(brushSem)
                rectSem.setPen(penSem)

                textSem = QGraphicsSimpleTextItem("Sem. du " + str(day.numDay) + " " +str(day.month))
                textSem.setPos(200,10)
                textSem.setScale(4)
                textSem.setZValue(100)
                textSem.setBrush(brushTextSem)
                # textSem.setParentItem(rectSem)

                textSem.setPos(200, i*280 + 80*((i+self.curWD)//7) - 75 )
                self.items.append(textSem)
                rectSem.setPos(0,i*280 + 80*((i+self.curWD)//7) - 75 )

                self.items.append(rectSem)
                #self.items.append(textSem)

            self.items.append(day)
            

        self.tablRDV = []
        self.importSaveJSON('saved data.txt')
        #self.importFileCSV("importCal.txt")
        for RDV in self.tablRDV:
            nbj=-RDV.date.daysTo(self.dateActuel)
            if(RDV.unsetPos == True):
                RDV.setPos(2, nbj* 280   +    80*((nbj+self.curWD)//7)   +    20 +10*RDV.time.toHours())
                RDV.unsetPos = False
            else:
                RDV.setPos(RDV.sX,nbj * 280   +    80*((nbj+self.curWD)//7)   +    20 +10*RDV.time.toHours())

            #RDV.setPos(2,-RDV.date.daysTo(self.dateActuel) * 280 + 20 +10*RDV.time.toHours())
            #self.items.append(RDV)
            #print("appened")
        





    def AddRDVPrint(self,data):
        print(data)



    def importSaveJSON(self, filename):
        with open(filename) as json_file:  
            data = json.load(json_file)
            for p in data:
                date = Date(p['date']['jour'], p['date']['mois'], p['date']['annee'])
                time = Time(p['time']['heure'], p['time']['minute'])
                duree = Time(p['duree']['heure'], p['duree']['minute'])
                if(p.get('sX') and p.get('sY')):
                    X = float(p.get('sX'))
                    Y = float(p.get('sY'))
                    self.addRDVInit(p['name'],date,time,duree,X,Y)
                else:
                    self.addRDVInit(p['name'],date,time,duree)
            #print(self.tablRDV)

    def importFileCSV(self, fileName):
        file = open(fileName, "r")
        lines = file.readlines()
        for i in lines:
            pair = True
            if len(i) == 0:
                continue
            print(str(len(i)))
            for char in range(0, len(i)-1):
                if i[char] == '"' and pair==True:
                    pair=False
                elif i[char] == '"' and pair == False:
                    pair=True
                if i[char] == ',' and pair == False:
                    i = i[:char] + i[(char+1):]

            i = i.split(',')
            dateL = i[1].split('/')
            date = Date(int(dateL[0]), int(dateL[1]), int(dateL[2]))
            timeL = i[2].split(':')
            time = Time(int(timeL[0]),int(timeL[1]))
            finL = i[3].split(':')
            diffH = int(finL[0])-int(timeL[0])
            diffM = int(finL[1])-int(timeL[1])
            if diffM < 0:
                diffH = diffH + diffM/60
                diffM = 0
            duree = Time(diffH,diffM)
            self.addRDVInit(i[0],date,time,duree)
        
    def addOneRDV(self, titre, date, time, duree):
        if titre == "\"Techniques de Gestion APPLICATION\"":
            f = 1
        if duree.toHours() == 0:
            print("Erreur: événement" + titre + date.toString() +": durée non définie")
            return
        newRDV = RDV(titre, date, time, duree)
        newRDV.setPos(2,-newRDV.date.daysTo(self.dateActuel) * 280 + 20 +10*newRDV.time.toHours())
        self.tablRDV.append(newRDV)
        self.items.append(newRDV)
        self.itemQueue.append(newRDV)

    def addRDVInit(self, titre, date, time, duree, X = None, Y = None):
        if titre == "\"Techniques de Gestion APPLICATION\"":
            f = 1
        if duree.toHours() == 0:
            print("Erreur: événement" + titre + date.toString() +": durée non définie")
            return
        newRDV = RDV(titre, date, time, duree, X, Y)
        self.tablRDV.append(newRDV)
        self.items.append(newRDV)

    def getItemQueue(self):
        result = self.itemQueue[0]
        self.itemQueue = []
        return result







class CDay(QGraphicsRectItem):



    def __init__(self, DT, brush = None):
        super().__init__()

        if brush == None:
            brush = myBrush
        
        self.items = []
        
        self.DT = DT
        self.day = DT.jourSem
        self.numDay = DT.jour
        self.month = DT.moisTxt
        self.year = DT.annee

        self.setRect(0,0,500,275)
        self.setPos(0,0)
        self.setBrush(brush)
        self.setPen(penDay)

        for i in range(0,25):
            line = QGraphicsLineItem(0,i*10+20,2000,i*10+20)
            line.setPen(penHourLines)
            txtHeure = QGraphicsSimpleTextItem(str(i) + " h00")
            txtHeure.setPos(-12,i*10+18)
            txtHeure.setScale(0.3)
            txtHeure.setBrush(brushTexte)
            txtHeure.setZValue(100)
            self.items.append(line)
            self.items.append(txtHeure)

        self.texte = QGraphicsSimpleTextItem()
        self.texte.setBrush(brushTexte)
        self.texte.setPos(10,0)
        self.texte.setScale(0.9)
        self.texte.setText("{} {} {} {}".format((self.day),(self.numDay),(self.month),(self.year)))
        self.texte.setZValue(100)
        self.items.append(self.texte)     

        self.rectSide = QGraphicsRectItem(-15,0,15,275)
        self.rectSide.setBrush(brushHourBg)
        self.rectSide.setPen(noPen)
        self.items.append(self.rectSide)
        for i in self.items:
            i.setParentItem(self)







class RDV(QGraphicsRectItem): # les dates sont censées etre des class:Date et les time, duree des class:Time


    def __init__(self, name, date, time, duree, X = None, Y = None):
        super().__init__()
        if(X == None and Y == None ):
            self.unsetPos = True
            self.setPos(0,200)
        else:
            self.sX = X
            self.sY = Y
            self.setPos(X,Y)
            self.unsetPos = False
        self.duree = duree.toHours()
        self.setRect(5,0,100,self.duree*10)
        self.texte = QGraphicsTextItem()
        self.texte.setDefaultTextColor(colorRDVtxt)
        self.texte.setPos(10,0)
        self.texte.setScale(0.5)
        self.name = name
        self.date = date
        self.time = time
        self.duree = duree
        self.texte.setPlainText(self.name)
        self.texte.setTextWidth(180)
        self.setBrush(brushRDV)
        self.setPen(penRDV)
        self.texte.setParentItem(self)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

    def itemChange(self, change, value):
        #super(RDV, self).itemChange(change, value)
        if(change == QGraphicsItem.ItemPositionChange ):
            self.sX = value.x()
            self.sY = value.y()
        return value



