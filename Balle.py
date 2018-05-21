# -*-coding: utf-8 -*-
#Ce module sert à la création des balles
import sys
import random
import Background
import math

# Création d'une balle
def create(Vx,Vy) :
    return {'x':78,'y':2,'vitesseX':Vx,'vitesseY':Vy, }

def createBalles(temps, listeDeBalle):
    vitesseX=[-4.5,-4.0,-3.5,-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0.5,1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    vitesseY=[-4.5,-4.0,-3.5,-3.0,-2.5,-2.0,-1.5,-1.0,-0.5,0.5,1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    a = temps % 10
    #print "temps=", temps,"                             ", "a=",a, "       ", len(listeDeBalle)
    if round(a,1)  == 0.1 :  # Apparition d'une balle toute les 10 secondes
        # Choix des vitesses
        vx=random.choice(vitesseX)
        vy=random.choice(vitesseY)
        # Création de la balle
        balle=create(vx,vy)
        # Ajout de la balle à la liste de toute les balles
        listeDeBalle.append(balle)
    return

# Accesseurs et Mutateurs
def getX(balle) :
    return balle['x']
def setX(balle,number) :
    balle['x']=number

def getY(balle) :
    return balle['y']
def setY(balle,number) :
    balle['y']=number

def getVX(balle):
    return balle['vitesseX']
def setVX(balle,number):
    balle['vitesseX']=number

def getVY(balle):
    return balle['vitesseY']
def setVY(balle,number):
    balle['vitesseY']=number

#Fonction affichant les balles
def show(balle) :
    #on se place a la position de la balle dans le terminal
    x=str(int(getX(balle)))
    y=str(int(getY(balle)))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    #couleur fond noire
    sys.stdout.write("\033[33m") # texte en jaune
    #affichage de l animat
    sys.stdout.write("o")

###test###
test=create(3.0,5.0)
setX(test,7)
setY(test,3)
setVX(test,8)
setVY(test,6)
result = getX(test)
if 7 != result:
    print "erreur, getX() devrait retourner 7, pas ", result
result = getY(test)
if 3 != result:
    print "erreur, getY() devrait retourner 3, pas ", result
result = getVX(test)
if 8.0 != result:
    print "erreur, getVX() devrait retourner 8.0, pas ", result
result = getVY(test)
if 6.0 != result:
    print "erreur, getVY() devrait retourner 6.0, pas ", result
print "test contient : ", test
print "fin des tests"
