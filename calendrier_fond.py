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
myPen = QPen(QColor(100,0,255),Qt.NoPen)
myBrush = QBrush(QColor(100,0,255))




class calendrier():




    def __init__(self):

        #currentDateTime 
        self.curDT = QDateTime.currentDateTime()
        self.curD = QDate.currentDate()
        
        self.curMonth = self.curDT.toString('MMMM')
        self.curMonthNum = self.curDT.toString('M')
        self.curDay = self.curDT.toString('dddd')
        self.curDayNum = self.curDT.toString('d')
        self.curYear = self.curDT.toString('yyyy')

        self.dateActuel = Date( int(self.curDayNum),int(self.curMonthNum),int(self.curYear))

        self.items = []
        self.itemQueue = []

        for i in range(-100,100):

            day = CDay(self.dateActuel.addDays(i))
            day.setPos(0,i*280)
            if(i == 0):
                day.setBrush(Qt.green)

            if day.day == "Monday" or day.day == "lundi":
                rectSem = QGraphicsRectItem(0,0,800,280*7-5)
                rectSem.setBrush(Qt.yellow)

                textSem = QGraphicsSimpleTextItem("Sem. du " + str(day.numDay) + " " +str(day.month))
                textSem.setPos(200,10)
                textSem.setScale(4)
                textSem.setParentItem(rectSem)

                rectSem.setPos(0,i*280)

                self.items.append(rectSem)
                #self.items.append(textSem)

            self.items.append(day)
            

        self.tablRDV = []
        self.importSaveJSON('saved data.txt')
        #self.importFileCSV("importCal.txt")
        for RDV in self.tablRDV:
            if(RDV.unsetPos == True):
                RDV.setPos(2,-RDV.date.daysTo(self.dateActuel) * 280 + 20 +10*RDV.time.toHours())
                RDV.unsetPos = False
            else:
                RDV.setPos(RDV.sX,-RDV.date.daysTo(self.dateActuel) * 280 + 20 +10*RDV.time.toHours())

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

        self.setRect(0,0,150,275)
        self.setPos(0,0)
        self.setBrush(brush)
        self.setPen(myPen)

        for i in range(0,23):
            line = QGraphicsLineItem(0,i*10+20,200,i*10+20)
            txtHeure = QGraphicsSimpleTextItem(str(i) + " h00")
            txtHeure.setPos(-12,i*10+18)
            txtHeure.setScale(0.3)
            self.items.append(line)
            self.items.append(txtHeure)

        self.texte = QGraphicsSimpleTextItem()
        self.texte.setBrush(Qt.black)
        self.texte.setPos(0,0)
        self.texte.setScale(0.9)
        self.texte.setText("{} {} {} {}".format((self.day),(self.numDay),(self.month),(self.year)))
        self.items.append(self.texte)        

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
        self.texte = QGraphicsSimpleTextItem()
        self.texte.setBrush(Qt.black)
        self.texte.setPos(0,0)
        self.texte.setScale(0.5)
        self.name = name
        self.date = date
        self.time = time
        self.duree = duree
        self.texte.setText(self.name)
        self.setBrush(Qt.red)
        self.setPen(myPen)
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



