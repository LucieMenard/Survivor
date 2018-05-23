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
timeStep = 0.1
temps = 0
listeDeBalle=[]
name = "NoName"
friction = 0.01
gravite = 0.5
etat = 0
niveau = 1

#Fonction initialisant les variables
def init():
    global animat, background, temps, listeDeBalle
    #initialisation de la partie
    temps=0.0
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

def askNiveau(): #TODO faire les dessins de niveau
    global niveau, gravite, friction
    image("niveau.txt")
    sys.stdout.write("\033[14;14H") # déplace le curseur en 14,14
    niveau = raw_input("Choisissez votre niveau entre 1 et 3 :")
    if niveau == "1" : # Enib
        gravite = 0.5
        friction = 0.01
        print gravite, friction
    elif niveau == "2": # Lune
        gravite = 0.2
        friction = 0.01
        print gravite, friction
    elif niveau == "3" : # Atlantide
        gravite = 0.5
        friction = 0.07
        print gravite, friction
    else :
        print " erreur de caractère du niveau !"

# Les Interactions
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

# Les mouvements
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
    ## Gestion des collisions
    # Calcul de la prochaine position X et Y théorique par rapport à la vitesse
    dx = vx * timeStep
    dy = vy * timeStep
    nx = x + dx
    ny = y - dy  # Car on a un repère orthonormé inversé
    # Détection d'obstacle à la prochaine position
    if Background.getElement(background, nx, y) == 0 : # rien
        Animat.setX(animat, nx)
    else : #rebond sur un mur
        Animat.setVX(animat, - vx/2)

    if Background.getElement(background, x, ny) == 0 : # rien
        Animat.setY(animat, ny)
    else : # atterrissage sur plafond ou sol ou plateforme
        Animat.setVY(animat, 0)

    return

def moveBalle(balle):
    global friction, gravite, timeStep, background
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
    if Background.getElement(background, nx, y) == 0 : # rien
        Balle.setX(balle, nx)
    else : # rebond sur un mur
        Balle.setVX(balle, -vx)

    if Background.getElement(background, x, ny) == 0 : # rien
        Balle.setY(balle, ny)
    else : # rebon sur le plafond ou une plateforme ou le sol
       Balle.setVY(balle, -vy)

    return

def debug():
    global temps, listeDeBalle, liste

    a = round(temps % 10,1)
    liste.append(a)
    print "a=",a
    print liste
    print len(listeDeBalle)

def contactAnimatBalle():
    global animat, listeDeBalle
    for i in listeDeBalle :
        c = Animat.collisionBalle(animat, i)
        if c == 1 :
            time.sleep(0.7)
            finDeJeu()
        else :
            pass

# Fonctions gérant l'affichage avant le début du jeu
def askname():
    global name
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    sys.stdout.write("\033[15;5H") # déplace le curseur en 1,1
    name = raw_input( "Quel est votre nom : " )

def finDeJeu():
    global temps, name, etat
    ## Sauvegarde du score
    # Récupération des anciens scores
    score = open("score.txt", "r")
    old_score = score.read()
    score.close()
    # Reecriture du fichier avec le nouveau score
    score = open("score.txt", 'w')
    score.write(old_score)
    score.write(str(name)),
    score.write(str("                 ")),
    score.write(str(temps)),
    score.write(str("\n"))
    score.close()

    ## Affichage de l'écran de fond
    # Ouverture des fichiers
    image("ecran de fin de jeu.txt")
    myfileone = open("score.txt", 'r')

    #Chargement des fichiers
    score = myfileone.read()

    # Fermeture des fichiers
    myfileone.close()

    # Lecture des images
    print "                                             ",temps, "secondes"
    print score
    time.sleep(7.0)
    # Etat sert a sortir de la boucle Run()
    etat = 1
    return etat

def ecrans():
    image("accueil.txt")
    time.sleep(4.0)
    image("explication.txt")
    time.sleep(8.0)

def image(filename):
    myfile = open(filename, 'r' )
    image = myfile.read()
    myfile.close()
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    print image

# Fonction gérant le jeu
def show():
    global background, animat, animation, timeStep, listeDeBalle, temps
    #rafraichissement de l'affichage
    #effacer la console
    sys.stdout.write("\033[1;1H") # déplace le curseur en 1,1
    sys.stdout.write("\033[2J") # clear the screen and move to 0,0
    #affichage des différents éléments
    Background.show(background)
    #debug()
    print temps, "secondes"
    Animat.show(animat)
    for i in listeDeBalle :
        Balle.show(i) # Affichage de toutes les balles de la liste
    #deplacement curseur
    sys.stdout.write("\033[1;1H\n") # déplace le curseur en 1,1

def run():
    global timeStep, temps, listeDeBalle, etat
    #Boucle de simulation
    while etat != 1:
        interact()
        move()
        Balle.createBalles(temps, listeDeBalle)
        show()
        time.sleep(timeStep-0.05)
        temps = round(temps + timeStep + 0.05, 1)

def quitGame():
    #restauration parametres terminal
    global old_settings
    #couleur white
    sys.stdout.write("\033[37m")
    sys.stdout.write("\033[40m")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    sys.exit()

###jeux###
#ecrans()
#askname()
#askNiveau()
init()
run()
quitGame()
