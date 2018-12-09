#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
import sys

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

def nbDimancheEntre(date, nbJours):
    return (nbJours+date.jourSemNum+1)//7

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



class Date():
    def __init__(self, jour, mois, annee):
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.moisTxt = listMois[mois-1]
        
        if self.jour == 6 and self.mois == 8 and self.annee == 1993:
            self.jourSem = "vendredi"
            self.jourSemNum = 4
        else: 
            self.jourSemNum = ( -self.daysTo(Date(6,8,1993))+4 ) % 7
            self.jourSem = listJours[self.jourSemNum]
            

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
        if(plizAddJ<0):
            annee = self.annee + plizAddJ//325
            plizAddJ = plizAddJ - self.daysTo(Date(self.jour, self.mois, annee))

        else:
            annee = self.annee

        jour = self.jour
        mois = self.mois
        
        result = self
        jrAjoutes = 0
        #ajout des jours restant dans le mois
        if(plizAddJ > nbJMois(mois, annee) - jour):
            jrAjoutes = jrAjoutes + nbJMois(mois, annee) - jour
            jour = 0
            mois = mois + 1
            if mois == 13:
                mois =1
                annee= annee+1

        else: #si il reste trop de jours dans le mois on augmente juste jour, puis return
            return Date(jour + plizAddJ, mois, annee)
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
            return Date(jour, mois, annee)

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
        return Date(jour, mois, annee)


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

       
    

class Time():
    def __init__(self, heure, minute):
        self.heure = heure
        self.minute = minute

    def __add__(self, other):
        heure = self.heure + other.heure
        minute = self.minute + other.minute
        if minute > 0:
            heure = heure + minute // 60
            minute = minute % 60
        result = Time( heure, minute )
        return result

    def __sub__(self, other):
        heure = self.heure - other.heure
        minute = self.minute - other.minute
        if minute < 0:
            heure = heure + (minute / 60)
        result = Time( heure, minute )
        return result
    
    def toHours(self):
        return self.heure + self.minute/60

    def toString(self):
        return str(self.heure) + "h" + str(self.minute)


