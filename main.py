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
    
    # creation des elements du jeu
    #le fond
    background = Background.create("fond2.txt")
    #l animat
    animat=Animat.create(20) #len(background)est ce que je peux faire un len pour ça 
    #balle
    balle=Balle.create(3.0,4.0)
    # interaction clavier
    tty.setcbreak(sys.stdin.fileno()) 
    
    #effacer la console
    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[2J")

def isData():
    #recuperation evenement clavier
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def interact():
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
            Animat.sauter(animat)
            
def move():
    global animat, balle, background, listeDeBalle, temps
    
    #déplacement animat 
    c1=Animat.collisionBord(animat,background)
    c2=Animat.collisionBalle(animat,balle)
    #je veux que mon animat ne bouge tout seul que si c'est une chute. Sinon il ne bouge que par rapport à l'interact donc pas besoin de gerer ca.
    
    if c1 == 1 :  #plafond  
        Balle.setVY(animat, -Balle.getVY(animat))  #collision faite finir rebondissements
        pass
    
    elif c1 == 2 : #mur
        Balle.setVX(animat, -Balle.getVX(animat))  #collision faite finir rebondissements
        pass
    
    elif  c1 == 3 : #plateforme ou sol
        #si on est en fin de chute alors plus de mvt donc juse pass
        pass
    elif c2 == 1 : #TODO contact animat/balle
        pass
    
    else : #TODO faire la chute
        setVY(animat,getVY(animat)+temps*(-9.81) )  #9.81 la gravité
        setX(animat,getX(animat)+getVX(animat)*temps)
        setY(animat,getY(animat)+getVY(animat)*temps)
        

    
    
    
    #TODO déplacement balle
    c3=Balle.collisionBord(balle, background)
    if c3==1 :
        for i in listeDeBalle :#faire les rebondissements
            #Balle.setVX(i,
            pass
    else :
        for i in listeDeBalle :
            setX(i,getX(i)+getVX(i)*temps)
            setY(i,getY(i)+getVY(i)*temps)
            #TODO faire les mouvements de la balle

def createBalles():
    global balle, listeDeBalle

    vitesseX=[1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    vitesseY=[1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    if dt %30 == 0 :
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
#   sys.stdout.write("\033[37m")
#   sys.stdout.write("\033[40m")

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


