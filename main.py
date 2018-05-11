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
friction=0.05  #TODO choisir valeur pour friction ( valeur cohèrente, je la garde ? )
gravite=0 #9.81 #TODO trouver valeur
nx=0
ny=0
dx=0
dy=0
vx=0
vy=0
cases =0

def init():
    global animat, background, timeStep, balle, temps         #TODO faire le askname

    #initialisation de la partie
    timeStep=0.2
    temps=0.1

    # creation des élèments du jeu
    #le fond
    background = Background.create("fond2.txt")
    #l animat
    animat=Animat.create(30, 11)
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
    global nx, ny, dx, dy, vx, vy, cases

    # Inialisation des variables
    x = Animat.getX(animat)
    y = Animat.getY(animat)
    vx = Animat.getVX(animat)
    vy = Animat.getVY(animat)

    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    vx = vx - vx * friction
    vy = vy - vy * gravite      # Car repère orthonormé inversé

    # Calcul de la prochaine position X et Y par rapport à la vitesse
    nx = round(x + vx)
    ny = round(y - vy)

    # Préparation de la trajectoire
    cases = int( max( abs(nx - x), abs(ny - y) ) )  #abs() : donne la valeur absolue

    # Empecher la division par 0
    if cases == 0 :
        return

    # Calcul des micros déplacements par rapport à notre temps
    dx = round( vx / cases )
    dy = round( vy / cases )

    # Calcul des positions intermédiaires
    for i in range( 0, cases + 1 ) :
        px = round( x + i * dx )
        py = round( y - i * dy )
        print "px=", px, "py=", py
        sys.exit()
        if Background.getElement(background, px, py) != 0 :
            # Si different de 0, alors présence d'obstacle : pas de déplacement possible à cette position

            break # TODO rebond

        # Déplacement de l'animat a la derniere position sans obstacle
        Animat.setX(animat, px)
        Animat.setY(animat, py)
    #Animat.setY(animat, NY)

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
    global timeStep, nx, ny, dx, dy, vx, vy, cases

    x = Animat.getX(animat)
    y = Animat.getY(animat)
    vx = Animat.getVX(animat)
    vy = Animat.getVY(animat)
    element = Background.getElement(background, x, y)

    print "x=", round(x, 2),
    print "y=", round(y, 2),
    print "vx=", round(vx, 2),
    print "vy=", round(vy, 2),
    print "element=", element
    print "nx=",nx,"ny=",ny,"dx=",dx,"dy=",dy,"vx=",vx,"vy=",vy,"cases=",cases

def show():
    global background, animat, animation, timeStep, balle

    #rafraichissement de l'affichage

    #effacer la console
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0

    #affichage des different element
    Background.show(background)

    debug()

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
