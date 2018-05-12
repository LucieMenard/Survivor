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
animat=None
background=None
timeStep=None
balle= None
temps=0
listeDeBalle=[]
friction = 0.05  #TODO choisir valeur pour friction #TODO faire les 3 modes de jeux
gravite = 0.4    #TODO choisir une  valeur

#pour la fonction debug()
nx=0
ny=0
dx=0
dy=0
vx=0
vy=0
cases =0
px=0
py=0

def init():
    global animat, background, timeStep, temps         #TODO faire le askname

    #initialisation de la partie
    timeStep=0.2
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

def move():
    global animat, friction, gravite, timeStep, background
    global nx, ny, dx, dy, vx, vy, cases, px, py

    # Inialisation des variables
    x = Animat.getX(animat)
    y = Animat.getY(animat)
    vx = Animat.getVX(animat)
    vy = Animat.getVY(animat)

    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    vx = vx - vx * friction
    vy = vy - gravite # avant : vy - vy * gravite
    Animat.setVX(animat, vx)
    Animat.setVY(animat, vy)

    # Calcul de la prochaine position X et Y théorique par rapport à la vitesse
    dx = vx * timeStep
    dy = vy * timeStep
    nx = x + dx
    ny = y - dy  # Car on a un repère orthonormé inversé

    # Détection d'obstacle à la prochaine position
    if Background.getElement(background, nx, ny) != 0 :
        if Background.getElement(background, px, py) != 0 :
            # Si diffèrent de 0, alors présence d'obstacle : pas de déplacement possible à cette position
            a = Animat.collisionBord(animat, background)
            if a == 1 :
                Animat.setVY(animat, - Animat.getVY(animat) )
            elif a == 2 :
                Animat.setVX(animat, - Animat.getVX(animat) )
            elif a == 0 :
                pass # Pour pas que l'on ai le message d'erreur
            elif a == 3 :
                Animat.setVY(animat, 0) # Pas de rebond sur le sol : on arrète la chute mais pas les déplacements latéraux
            else :
                print "error 407 : caractère non supporté"
            return # déplacement impossible

    # Déplacement
    Animat.setX(animat, nx)
    Animat.setY(animat, ny)

    return

def contactBalleAnimat():
    global animat, listeDeBalle
    ax = Animat.getX(animat)
    ay = Animat.getY(animat)
    for i in listeDeBalle :
        bx = Balle.getX(i)
        by = Balle.getY(i)
        if ay == by :
            if ax == bx :
                # TODO faire la fonction : afficher écran de fin + score
                quitGame()
            else :
                pass
        else :
            pass

def debug():
    global animat, background
    global timeStep, nx, ny, dx, dy, vx, vy, cases, px, py, temps

    x = Animat.getX(animat)
    y = Animat.getY(animat)

    print "temps=", temps
    print "x=", round(x, 2),
    print "y=", round(y, 2)
    print "vx=", round(vx, 2),
    print "vy=", round(vy, 2),
    print " | dx=", round(dx, 2),
    print "dy=", round(dy, 2)
    print "nx=", round(nx, 2),
    print "ny=", round(ny, 2)

def show():
    global background, animat, animation, timeStep, listeDeBalle

    #rafraichissement de l'affichage

    #effacer la console
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0

    #affichage des différents éléments
    Background.show(background)

    debug()

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
