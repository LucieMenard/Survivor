# -*-coding: utf-8 -*-
#Ce module sert à la création des balles
import sys
import random
import Background

# Création d'une balle
def create(Vx,Vy) :
    return {'x':78,'y':2,'vitesseX':Vx,'vitesseY':Vy, }

def createBalles(temps):
    global listeDeBalle
    vitesseX=[-4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.5, 1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
    vitesseY=[-4.5, -4.0, -3.5, -3.0, -2.5, -2.0, -1.5, -1.0, -0.5, 0.5, 1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
    if temps % 10 == 0 :  # Apparition d'une balle toute les 10 secondes
        # CHoix des vitesses
        vx=random.choice(vitesseX)
        vy=random.choice(vitesseY)
        # Création de la balle
        balle=Balle.create(vx,vy)
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

def droite(balle) :
    setX(balle,getX(balle)+1)
    return
def gauche(balle) :
    setX(balle,getX(balle)-1)
    return

# Fonctions bougant les balles
def vitesses(balle, gravite, friction, timeStep):
    # Initialisation des variables
    x = getX(balle)
    y = getY(balle)
    vx = getVX(balle)
    vy = getVY(balle)

    # Applications des accélérations
    vx = vx + friction * timeStep
    setVX(balle, vx)
    vy = vy + gravite * timeStep
    setVY(balle, vy)

def moveBalle(balle, timeStep) :
    # Changement de position
    x = getX(balle)
    y = getY(balle)
    vx = getVX(balle)
    vy = getVY(balle)
    nx = x + vx * timeStep
    ny = y + vy * timeStep
    return nx, ny

def moveB(balle, background, timeStep):
    global friction, gravite
    #global nx, ny, dx, dy, vx, vy, cases, px, py

    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    vitesses(balle, timeStep)

    # Initialisation des variables
    x = getX(animat)
    y= getY(animat)
    nx, ny = moveBalle(balle, timeStep)

    # Calcul de la fonction affine : y = cd * x + o
    cd = (ny - y) / (nx - x)        # Calcul du coefficient directeur de la fontion
    o = y - cd * x                  # Calcul de l'ordonnée à l'origine

    # Calcul des positions intermediaires
    xint = x
    while xint <= nx :
        yint = cd * xint + o
        #Détection d'obstacle
        if Background.getElement(background, xint, yint) != 0 :
        # Si diffèrent de 0, alors présence d'obstacle : pas de déplacement possible à cette position
            a = collisionBord(balle, background)
            if a == 0 :
                pass # Pour que l'on ai pas le message d'erreur avec une case vide

            elif a == 1 :    #collision contre le plafond
                setVY(balle, - getVY(balle))
                setX(balle, xint)
                setY(balle, yint)

            elif a == 2 :   #collision contre le mur gauche
                setVX(balle, - getVX(balle))
                setX(balle, xint + 1)
                setY(balle, yint + 1)

            elif a == 3 :   #collision contre le sol ou une plateforme
                setVY(balle, 0) # Pas de rebond sur le sol : on arrète la chute mais pas VX
                setX(balle, xint)
                setY(balle, yint - 1) # TODO pb si on aborde la plateforme par le bas

            elif a == 4 :   #collisin contre le mur droit
                setVX(balle, - getVX(balle))
                setX(balle, xint - 1)
                setY(balle, yint + 1)

            else :
                print "error 407 : caractère non supporté"
            return # déplacement impossible : on sort de la fonction move()

        else :
            # Déplacement
            setX(balle, nx)
            setY(balle, ny)

        xint = xint + 1
    return

#def accelerationVX(balle) :
    #setVX(balle, getVX(balle) + 10)

#def decelerationVX(balle) :
    #setVX(balle, getVX(balle) - 10)

#Fonction affichant les balles
def show(balle) :
    #on se place a la position de la balle dans le terminal
    x=str(int(getX(balle)))
    y=str(int(getY(balle)))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)

    #couleur fond noire
    sys.stdout.write("\033[40m")

    #affichage de l animat
    sys.stdout.write("o")

# Fonction gerant les collisions des balles avec les bords
def collisionBord(balle, fond) :
    x = int( getX(balle) )
    y = int( getY(balle) )
    a = fond['fondTableau'][y][x]
    return a

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
