# -*- coding: utf-8 -*-
#modules externes
import sys
import os
import time
import select
import tty 
import termios
import random

#modules internes
import Animat
import Balle
import Background

#interaction clavier
old_settings = termios.tcgetattr(sys.stdin)

#donnee du jeu
animat=None
background=None 
timeStep=None
balle= None
temps=0
listeDeBalle=[]

def init():
    global animat, background, timeStep, balle, temps         #TODO faire le askname
    
    #initialisation de la partie	
    timeStep=0.2
    temps=0.1
    
    # creation des élèments du jeu
    #le fond
    background = Background.create("fond2.txt")
    #l animat
    animat=Animat.create(20)
    #balle
    balle=Balle.create(3.0,3.0)
    # interaction clavier
    tty.setcbreak(sys.stdin.fileno()) 
    
    #effacer la console
    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[2J")

def isData():
    #recuperation evenement clavier
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def interact():
    global temps
    #gestion des evenement clavier
    #si une touche est appuyee
    if isData():
        c = sys.stdin.read(1)
        if c == '\x1b':         # x1b is ESC
            quitGame()
        elif c=='q' :
            Animat.gauche(animat)
        elif c=='d' :
            Animat.droite(animat)
        elif c=='\x20' : #x20 est espace 
            Animat.sauter(animat,temps)
            
def move():
    #déplacement de l'animat
    if Animat.collisionBord(animat,background) == 1 :
        rebondissementsAPlafond()
    elif Animat.collisionBord(animat,background) == 2 :
        rebondissementsAMur()
    elif Animat.collisionBord(animat,background) == 3 :
        rebondissementsASol()
    else:
        chuteAnimat()
    
    #déplacement des balles
    global listeDeBalle
    for i in listeDeBalle :
            if Balle.collisionBord(i,background) == 1 :
                rebondissementsBPlafond()
            elif Balle.collisionBord(i,background) == 2 :
                rebondissementsBMur()
            elif Balle.collisionBord(i,background) == 3 :
                rebondissementsBSol()
            else:
                chuteBalle()
    
    #contact Animat et Balle
    contactBalleAnimat()

def rebondissementsAPlafond():
    #rebondissements contre le plafond
    Balle.setVY(animat, -Balle.getVY(animat))
    
def rebondissementsAMur():
    #rebondissements contre le mur
    Balle.setVX(animat, -Balle.getVX(animat))
def rebondissementsASol():
    Animat.setVX(animat,0)
    Animat.setVY(animat,0)
    #TODO si on est en fin de chute alors plus de mvt donc juste passe
def chuteAnimat():
        #TODO faire la chute
    #Animat.setVY(animat,Animat.getVY(animat)+temps*(-9.81) )  #9.81 la gravité
    #Animat.setX(animat,Animat.getX(animat)+Animat.getVX(animat)*temps)
    #Animat.setY(animat,Animat.getY(animat)+Animat.getVY(animat)*temps)
    pass

def contactBalleAnimat():
    #c2 == 1 : #TODO contact animat/balle = finir le jeux
    pass

def rebondissementsBMur():
    return
def rebondissementsBPlafond():
    return
def rebondissementsBSol():
    return
def chuteBalle():
    return

def createBalles():
    global balle, listeDeBalle, temps
    vitesseX=[1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    vitesseY=[1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    if temps %30 == 0 :
        vx=random.choice(vitesseX)
        vy=random.choice(vitesseY)
        balle=Balle.create(vx,vy)
        direction=[0,1]      #0: droite, 1: gauche 
        d=random.choice(direction)
        if d==0 :
            Balle.droite(balle)
        elif d==1 :
            Balle.gauche(balle)
        listeDeBalle.append(balle)
    return
    
def show():
    global background, animat, animation, timeStep, balle

    #rafraichissement de l'affichage
    
    #effacer la console
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0

    #affichage des different element
    Background.show(background)
    Animat.show(animat)
    Balle.show(balle)
    
    #Animation.show(animation,timeStep)
    
    #restoration couleur 
    #sys.stdout.write("\033[37m")
    #sys.stdout.write("\033[40m")

    #deplacement curseur
    sys.stdout.write("\033[1;1H\n") # déplace le curseur en 1,1

def run():
    global timeStep, temps
    #Boucle de simulation
    while 1: #TODO faire l'écran de fin + affichage du temps qui passe
        interact()
        move()
        createBalles()
        show()
        time.sleep(timeStep)
    temps = temps + timeStep
    
        
def quitGame():
    #restoration parametres terminal
    global old_settings
    #couleur white
    sys.stdout.write("\033[37m")
    sys.stdout.write("\033[40m")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    sys.exit()
        
###jeux###
init()
#try:
run()
#finally:
quitGame()


