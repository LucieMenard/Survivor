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
friction=0.15  #TODO choisir valeur pour friction ( valeur cohèrente, je la garde ? )
gravite=1 #9.81 #TODO trouver valeur
nx=0
ny=0
dx=0
dy=0
vx=0
vy=0
cases =0
px=0
py=0
element=0

def init():
    global animat, background, timeStep, balle, temps         #TODO faire le askname

    #initialisation de la partie
    timeStep=0.2
    temps=0.1

    # creation des élèments du jeu
    #le fond
    background = Background.create("fond2.txt")
    #l animat
    animat=Animat.create(24, 20)
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
    #gestion des evenement clavier
    #si une touche est appuyee
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
    global nx, ny, dx, dy, vx, vy, cases, px, py, element

    # Inialisation des variables
    x = Animat.getX(animat)
    y = Animat.getY(animat)
    vx = Animat.getVX(animat)
    vy = Animat.getVY(animat)

    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    vx = vx - vx * friction
    vy = vy - vy * gravite
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
            # Si différent de 0, alors présence d'obstacle : pas de déplacement possible à cette position
            a = Animat.collisionBord(animat, background)
            if a == 1 or 3:
                Animat.setVY(animat, - Animat.getVY(animat) )
            elif a == 2 :
                Animat.setVX(animat, - Animat.getVX(animat) )
            elif a == 0 :
                pass # Vérification
            else :
                print "error 407 : caractère non supporté"
            return # déplacement impossible

    # Déplacement
    Animat.setX(animat, nx)
    Animat.setY(animat, ny)

    return



def contactBalleAnimat():
    #c2 == 1 : #TODO contact animat/balle = finir le jeux
    pass
    return

def createBalles():
    global balle, listeDeBalle, temps
    vitesseX=[1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    vitesseY=[1.0,2.0,2.5,3.0,3.5,4.0,4.5]
    if temps % 30 == 0 :
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

def debug():
    global animat, background
    global timeStep, nx, ny, dx, dy, vx, vy, cases, px, py, element, temps

    x = Animat.getX(animat)
    y = Animat.getY(animat)
    #vx = Animat.getVX(animat)
    #vy = Animat.getVY(animat)
    #element = Background.getElement(background, x, y)

    print "temps=", temps

    print "x=", round(x, 2),
    print "y=", round(y, 2)

    print "vx=", round(vx, 2),
    print "vy=", round(vy, 2),
    print " | dx=", round(dx, 2),
    print "dy=", round(dy, 2)

    print "nx=", round(nx, 2),
    print "ny=", round(ny, 2)

    print "element=", element
    #print "nx=",round(nx,2),"ny=",round(ny,2),"dx=",round(dx,2),"dy=",round(dy,2),"vx=",round(vx,2),"vy=",round(vy,2),"cases=",cases,"px=",round(px,2),"py=",round(py,2)

def show():
    global background, animat, animation, timeStep, balle

    #rafraichissement de l'affichage

    #effacer la console
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0

    #affichage des different element
    Background.show(background)

    #debug()

    Animat.show(animat)
    Balle.show(balle)

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
