# -*- coding: utf-8 -*-

# Importation des modules externes
import sys
import os
import time
import select
import tty
import termios
import random

# Importation des modules internes
import Animat
import Balle
import Background

# Interaction clavier
old_settings = termios.tcgetattr(sys.stdin)

# Donnee du jeu
animat = None
background = None
timeStep = 0.2
balle= None
temps = 0
listeDeBalle=[]


def init():
    global animat, background, timeStep, temps         #TODO faire le askname

    #initialisation de la partie
    temps=0.1

    # Creation des élèments du jeu
    # Pas de création de balle ici car déja fait avec la fonction createBalles()
    # le fond
    background = Background.create("fond2.txt")
    # l animat
    animat=Animat.create(10, 2)

    # Interaction clavier
    tty.setcbreak(sys.stdin.fileno())

    # Effacer la console
    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[2J")

def isData():
    # Récuperation évènement clavier
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def interact():
    # Gestion des evenement clavier
    # Si une touche est appuyee, renvoie True
    if isData():
        c = sys.stdin.read(1)
        if c == '\x1b':                 # x1b is ESC
            quitGame()
        elif c == 'q' or c == 'Q':
            Animat.decelerationVX(animat)
        elif c == 'd' or c == "D":
            Animat.accelerationVX(animat)
        elif c == '\x20' : #x20 est espace
            Animat.accelerationVY(animat)

def move() :
    global timeStep, animat, listeDeBalle
    Animat.moveA(animat, background, timeStep)
    for i in listeDeBalle :
        Balle.moveB(i, background, timeStep)
    contactBalleAnimat()

def contactBalleAnimat():
    global animat, listeDeBalle
    ax = Animat.getX(animat)
    ay = Animat.getY(animat)
    for i in listeDeBalle :
        c = Animat.contactBalleAnimat(animat, i)
        if c == 1 :
            finDeJeu()
        else :
            pass

def welcome():
    myfile =  open("accueil.txt", 'r' )
    image = myfile.read()
    myfile.close()
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    print image

def explication():
    myfile = open("explication.txt", 'r')
    image = myfile.read()
    myfile.close()
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    print image

def finDeJeu():
    global temps
    myfile = open("ecran de fin de jeu.txt", 'r')
    image = myfile.read()
    myfile.close()
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    print image
    print "                            ", temps, "secondes"
    time.sleep(7.0)

def ecrans():
    welcome()
    time.sleep(4.0)
    explication()
    time.sleep(8.0)

def show():
    global background, animat, animation, timeStep, listeDeBalle, temps

    #rafraichissement de l'affichage

    #effacer la console
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0

    #affichage des différents éléments
    Background.show(background)

    Animat.debug(animat)
    print temps, "secondes"

    Animat.show(animat)

    for i in listeDeBalle :
        Balle.show(i) # Affichage de toutes les balles de la liste

    #restoration couleur
    #sys.stdout.write("\033[37m")
    #sys.stdout.write("\033[40m")

    #deplacement curseur
    sys.stdout.write("\033[1;1H\n") # déplace le curseur en 1,1

def run():
    global timeStep, temps
    #Boucle de simulation
    while 1: #TODO faire l'écran de fin + affichage du temps qui passe pour V2
        interact()
        move()
        Balle.createBalles(temps)
        show()
        contactBalleAnimat()
        time.sleep(timeStep)
        temps = temps + timeStep

def quitGame():
    finDeJeu()
    #restoration parametres terminal
    global old_settings
    #couleur white
    sys.stdout.write("\033[37m")
    sys.stdout.write("\033[40m")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    sys.exit()

###jeux###
#ecrans()
init()
#try:
run()
#finally:
quitGame()
