# -*- coding: utf-8 -*-
# Importation des modules externes
import sys #TODO mettre de la couleur
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
timeStep = 0.1
temps = 0
listeDeBalle=[]
name = ""
friction = 0.01   #TODO faire les 3 modes de jeux
gravite = 0.5

#pour la fonction debug()
nx=0
ny=0
dx=0
dy=0

def init():
    global animat, background, timeStep, temps
    #initialisation de la partie
    temps=0.1

    # Creation des élèments du jeu
    # Pas de création de balle ici car déja fait avec la fonction createBalles()
    # le fond
    background = Background.create("fond2.txt")
    # l'animat
    animat = Animat.create(2, 19)

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
    global listeDeBalle, friction, gravite, timeStep, background
    moveAnimat()
    for i in listeDeBalle :
        moveBalle(i)
    contactAnimatBalle()

def moveAnimat():
    global animat, friction, gravite, timeStep, background
    # Inialisation des variables
    x = Animat.getX(animat)
    y = Animat.getY(animat)
    vx = Animat.getVX(animat)
    vy = Animat.getVY(animat)
    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    vx = vx - vx * friction
    vy = vy - gravite # avant : vy - vy * gravite
    # Limiter les vitesses
    if vx > 7.0 :
        vx = 7.0
    elif vx < -7.0 :
        vx = -7.0
    if vy > 7.0 :
        vy = 7.0
    elif vy < -7.0 :
        vy = -7.0
    # Changement des vitesses
    Animat.setVX(animat, vx)
    Animat.setVY(animat, vy)
    # Calcul de la prochaine position X et Y théorique par rapport à la vitesse
    dx = vx * timeStep
    dy = vy * timeStep
    nx = x + dx
    ny = y - dy  # Car on a un repère orthonormé inversé
    # Détection d'obstacle à la prochaine position
    if Background.getElement(background, round(nx+1), round(y)) == 3 : #mur
        Animat.setVX(animat, - Animat.getVX(animat)/2)
        Animat.setX(animat, x)
        Animat.setY(animat, ny)
    if Background.getElement(background, round(x), round(ny)) == 3 : #plafond ou sol ou plateforme
        Animat.setVY(animat, 0)
        Animat.setX(animat, nx)
        Animat.setY(animat, y)
    else :
        # Déplacement
        Animat.setX(animat, nx)
        Animat.setY(animat, ny)
    return

def moveBalle(balle):
    global friction, gravite, timeStep, background
    global nx, ny, dx, dy
    # Inialisation des variables
    x = Balle.getX(balle)
    y = Balle.getY(balle)
    vx = Balle.getVX(balle)
    vy = Balle.getVY(balle)
    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    #vx = vx - vx * friction
    vy = vy - gravite
    if vx > 7.0 :
        vx = 7.0
    elif vx < -7.0 :
        vx = -7.0
    if vy > 7.0 :
        vy = 7.0
    elif vy < -7.0 :
        vy = -7.0
    Balle.setVX(balle, vx)
    Balle.setVY(balle, vy)
    # Calcul de la prochaine position X et Y théorique par rapport à la vitesse
    dx = vx * timeStep
    dy = vy * timeStep
    nx = x + dx
    ny = y - dy  # Car on a un repère orthonormé inversé
    # Détection d'obstacle à la prochaine position
    if Background.getElement(background, round(nx), round(y)) == 3 : #mur #avant nx+1
        Balle.setVX(balle, -vx)
        Balle.setX(balle, x)
        Balle.setY(balle, ny)
    if Background.getElement(background, round(x), round(ny)) == 3 : #plafond ou sol ou plateforme
        Balle.setVY(balle,  -vy) # avant Balle.getVY(balle)
        Balle.setX(balle, nx)
        Balle.setY(balle, y)
    else :
        # Déplacement
        Balle.setX(balle, nx)
        Balle.setY(balle, ny)
    return

def debug():
    global listeDeBalle
    global temps, nx, ny, dx, dy

    x = Balle.getX(listeDeBalle[0])
    y = Balle.getY(listeDeBalle[0])
    vx = Balle.getVX(listeDeBalle[0])
    vy = Balle.getVY(listeDeBalle[0])

    print "x=", int(x),
    print "y=", int(y)
    print "vx=", round(vx, 1),
    print "vy=", round(vy, 1),
    print " | dx=", round(dx, 1),
    print "dy=", round(dy, 1)
    print "nx=", round(nx, 1),
    print "ny=", round(ny, 1)

def contactAnimatBalle():
    global animat, listeDeBalle
    for i in listeDeBalle :
        c = Animat.collisionBalle(animat, i)
        if c == 1 :
            finDeJeu()
        else :
            pass

def askname():
    global name
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    sys.stdout.write("\033[15;5H") # déplace le curseur en 1,1
    name = input( "Entrer votre nom avec des guillemets : " )

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
    global temps, name

    # Sauvegarde du score
    score = open("score.txt", "r")
    old_score = score.read()
    score.close()
    score = open("score.txt", 'w')

    score.write(old_score)
    score.write(str(name)),
    score.write(str("                 ")),
    score.write(str(temps)),
    score.write(str("\n"))
    score.close()

    # Affichage de l'écran de fond
    # Ouverture des fichiers
    myfileone = open("score.txt", 'r')
    myfile = open("ecran de fin de jeu.txt", 'r')

    #Chargement des fichiers
    image = myfile.read()
    score = myfileone.read()

    # Fermeture des fichiers
    myfile.close()
    myfileone.close()

    ## Affichage
    #sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    #sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    #print image
    #print "                            ", temps, "secondes"
    #print score
    #time.sleep(7.0)

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
    #debug()
    #print len(listeDeBalle)
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
    global timeStep, temps, listeDeBalle
    #Boucle de simulation
    while 1:
        interact()
        move()
        Balle.createBalles(temps, listeDeBalle)
        show()
        contactAnimatBalle()
        time.sleep(timeStep-0.05)
        temps = round(temps + timeStep + 0.05, 1)

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
ecrans()
askname()
init()
#try:
run()
#finally:
quitGame()
