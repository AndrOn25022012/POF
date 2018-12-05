#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import sys
#pens (contour) et brushs (fond) globaux
myPen = QPen(QColor(48,114,171),Qt.NoPen)
myBrush = QBrush(QColor(48,114,171)) #3072ab
dayColor = QBrush(QColor(48,114,171))

listMois = "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split()
listNumJoursDef = []
for i in "31 28 31 30 31 30 31 31 30 31 30 31".split(): listNumJoursDef.append(int(i))
listNumJCumulDef = []
prec = 0
for i in listNumJoursDef:
    listNumJCumulDef.append(i+prec)
    prec = i + prec
listNumJoursBisxt = []
for i in "31 29 31 30 31 30 31 31 30 31 30 31".split(): listNumJoursBisxt.append(int(i))
listNumJCumulBisxt = []
prec = 0
for i in listNumJoursBisxt:
    listNumJCumulBisxt.append(i+prec)
    prec = i + prec

listJours = "lundi mardi mercredi jeudi vendredi samedi dimanche".split()

def nbJMois(mois, annee):
    if isBisxt(annee):
        return listNumJoursBisxt[mois-1]
    else:
        return listNumJoursDef[mois-1]

def nbJMoisCumul(mois, annee):
    if mois == 0:            #le mois 0 est considéré comme le début d'année
        return 0
    if isBisxt(annee):
        return listNumJCumulBisxt[mois-1]
    else:
        return listNumJCumulDef[mois-1]

def nbJAn(annee):
    if isBisxt(annee):
        return listNumJCumulBisxt[11]
    else:
        return listNumJCumulDef[11]

def isBisxt( annee ):
    if(annee%400 == 0):
        return True
    elif(annee%100 == 0):
        return False
    elif(annee%4 == 0):
        return True
    else:
        return False



class date():
    def __init__(self, jour, mois, annee):
        self.jour = jour
        self.mois = mois
        self.annee = annee
        if self.jour == 6 and self.mois == 8 and self.annee == 1993:
            self.jourSem = "vendredi"
        else: 
            self.jourSem = listJours[ ( daysTo(date(6,8,1993))+4 ) % 7 ]

    def toString(self):
        return(str(self.jour) +"/"+ str(self.mois) +"/"+ str(self.annee))

    def daysTo(self, other):
        
        if(self.supThan(other)):  #si la différence est négative, on retourne -(distance opposée)
            return - other.daysTo(self)

        result = 0

        if other.annee == self.annee:  # si les années sont les mêmes:
            if other.mois - self.mois > 1:
                for mois in range(self.mois+1,other.mois):#                    jours des mois intermédiaires
                    result = result + nbJMois(mois,self.annee)
            if other.mois == self.mois:
                result = result + other.jour - self.jour#                        cas meme mois
                return result
            else:
                result = result + ( nbJMois(self.mois,self.annee)-self.jour)#    jours restant dans le mois self
                result = result + other.jour#                                    jours passés dans le mois other
                return result                             
        
        else:  # Si les annees sont differentes:

            if other.annee - self.annee > 1:#                                             jours des annees intermediaires
                for annee in range(self.annee+1, other.annee):             
                    result = result + nbJAn(annee)
            
            #                                                                             jours restant annee self
            result = result + nbJMois(self.mois,self.annee) - self.jour#                  jours restant mois self
            result = result + nbJAn(self.annee) - nbJMoisCumul(self.mois, self.annee)#    jours restant sur les mois suivants de l'annee self
            #                                                                             jours passes annee other
            result = result + nbJMoisCumul(other.mois-1, other.annee)#                    jours passés sur les mois précédents
            result = result + other.jour

            return result
    
    def addDays(self, plizAddJ ):
        jour = self.jour
        mois = self.mois
        annee = self.annee
        result = self
        jrAjoutes = 0
        #ajout des jours restant dans le mois
        if(plizAddJ >= nbJMois(mois, annee) - jour):
            jrAjoutes = jrAjoutes + nbJMois(mois, annee) - jour
            jour = 0
            mois = mois + 1
            if mois == 13:
                mois =1
                annee= annee+1

        else: #si il reste trop de jours dans le mois on augmente juste jour, puis return
            return date(jour + plizAddJ, mois, annee)
        #ajout des jours restant dans l'annee
        if(plizAddJ > jrAjoutes + nbJAn(annee) - nbJMoisCumul((mois - 1) % 12, annee)):
            jrAjoutes = jrAjoutes + nbJAn(annee) - nbJMoisCumul((mois - 1) % 12, annee)
            annee = annee + 1
            mois = 1
        else: #si il reste trop de jours dans l'annee on augmente les mois puis jours, puis return
            while plizAddJ - jrAjoutes > nbJMois(mois,annee):
                jrAjoutes = jrAjoutes + nbJMois(mois,annee)
                mois = mois + 1
            jour = jour + plizAddJ - jrAjoutes
            return date(jour, mois, annee)

        mois = 1
        #ajout des jours annees interm ?
        while plizAddJ - jrAjoutes > nbJAn(annee):
            jrAjoutes = jrAjoutes + nbJAn(annee)
            annee = annee + 1
        
        #ajout des jours derniere annee ?
        #   -ajout des mois derniere annee
        while plizAddJ - jrAjoutes > nbJMois(mois, annee):
            jrAjoutes = jrAjoutes + nbJMois(mois, annee)
            mois = mois + 1
        #   -ajout des jours dernier mois
        jour = plizAddJ - jrAjoutes
        return date(jour, mois, annee)


    def supThan(self,other):
        if(self.annee > other.annee):
            return True
        elif(self.annee == other.annee):
            if(self.mois > other.mois):
                return True
            elif(self.mois == other.mois):
                if(self.jour > other.jour):
                    return True
                else:
                    return False

    def Equals(self, other):
        if(self.annee == other.annee and self.mois == other.mois and self.jour == other.jour):
            return True
        else:
            return False

       
    

class time():
    def __init__(self, heure, minute):
        self.heure = heure
        self.minute = minute

    def __add__(self, other):
        heure = self.heure + other.heure
        minute = self.minute + other.minute
        if minute > 0:
            heure = heure + minute // 60
            minute = minute % 60
        result = time( heure, minute )
        return result

    def __sub__(self, other):
        heure = self.heure - other.heure
        minute = self.minute - other.minute
        if minute < 0:
            heure = heure + (minute / 60)
        result = time( heure, minute )
        return result
    
    def toHours(self):
        return self.heure + self.minute/60





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

        self.dateActuel = date( int(curDayNum),int(curMonthNum),int(curYear))

        self.items = []

        for i in range(-100,100):

            day = CDay(date(self.dateActuel.addDays(i)))
            day.setPos(0,i*280)
            if(i == 0):
                day.setBrush(dayColor)

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
        self.importFile("importCal.txt")
        for RDV in self.tablRDV:
            RDV.setPos(2,-RDV.date.daysTo(self.dateActuel) * 280 + 20 +10*RDV.time.toHours())
            self.items.append(RDV)




    def importFile(self, fileName):
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
            date = date(int(dateL[2]), int(dateL[1]), int(dateL[0]))
            timeL = i[2].split(':')
            time = time(int(timeL[0]),int(timeL[1]))
            finL = i[3].split(':')
            diffH = int(finL[0])-int(timeL[0])
            diffM = int(finL[1])-int(timeL[1])
            if diffM < 0:
                diffH = diffH + diffM/60
                diffM = 0
            duree = QTime(diffH,diffM)
            self.addRDV(i[0],date,time,duree)
        print(self.tablRDV)
        
    def addRDV(self, titre, date, time, duree):
        if titre == "\"Techniques de Gestion APPLICATION\"":
            f = 1
        if duree.toString('h') == '':
            print("Erreur: événement" + titre + date.toString('dd/MM/yy') +": durée non définie")
            return
        newRDV = RDV(titre, date, time, duree)
        self.tablRDV.append(newRDV)







class CDay(QGraphicsRectItem):



    def __init__(self, DT, brush = None):
        super().__init__()

        if brush == None:
            brush = myBrush
        
        self.items = []
        
        self.DT = DT
        self.day = DT.jourSem
        self.numDay = DT.jour
        self.month = DT.mois
        self.year = DT.annee

        self.setRect(0,0,150,275)
        self.setPos(0,0)
        self.setBrush(brush)
        self.setPen(myPen)

        for i in range(0,23):
            line = QGraphicsLineItem(0,i*10+20,5,i*10+20)
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







class RDV(QGraphicsRectItem): # les dates sont censées etre des class:date et les time, duree des class:time

    def __init__(self, name, date, time, duree):
        super().__init__()
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
        self.setPos(10,0)
        self.setBrush(Qt.red)
        self.setPen(myPen)
        self.texte.setParentItem(self)

