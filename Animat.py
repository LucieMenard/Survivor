#-*-coding:utf-8 -*-
#Ce module sert à la création du personnage du joueur
import sys
import Background
import Balle


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
friction = 0.05  #TODO choisir valeur pour friction #TODO faire les 3 modes de jeux
gravite = 0.4    #TODO choisir une  valeur

# Création de l'Animat : le personnage que l'utilisateur va bouger
def create(x, y) :
    return {'x':x,'y':y,'vitesseX':0,'vitesseY':0}

# Accesseurs et Mutateurs
def getX(animat) :
    return animat['x']
def setX(animat, number) :
    animat['x'] = number

def getY(animat) :
    return animat['y']
def setY(animat, number) :
    animat['y'] = number

def getVX(animat):
    return animat['vitesseX']
def setVX(animat,number):
    animat['vitesseX']=number

def getVY(animat):
    return animat['vitesseY']
def setVY(animat, number):
    animat['vitesseY']=number

# Fonctions gerant les impulsions
def accelerationVX(animat) :
    setVX(animat, getVX(animat) + 1)

def decelerationVX(animat) :
    setVX(animat, getVX(animat) - 1)

def accelerationVY(animat) :
    setVY(animat, getVY(animat) + 4)  #TODO choisir valeur pour la poussée que l'on donne lors du saut

# Fonctions gérant les mouvements
def vitesses(animat, timeStep):
    global gravite, friction

    # Initialisation des variables
    x = getX(animat)
    y = getY(animat)
    vx = getVX(animat)
    vy = getVY(animat)

    # Applications des accélérations
    vx = vx + friction * timeStep
    setVX(animat, vx)
    vy = vy + gravite * timeStep
    setVY(animat, vy)

def moveAnimat(animat, timeStep) :
    # Changement de position
    x = getX(animat)
    y = getY(animat)
    vx = getVX(animat)
    vy = getVY(animat)
    nx = x + vx * timeStep
    ny = y + vy * timeStep
    return nx, ny

def moveA(animat, background, timeStep) :
    global friction, gravite
    #global nx, ny, dx, dy, vx, vy, cases, px, py

    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    vitesses(animat, timeStep)

    # Initialisation des variables
    x = getX(animat)
    y = getY(animat)
    nx, ny = moveAnimat(animat, timeStep)

    # Calcul de la fonction affine : y = cd * x + o
    cd = (ny - y) / (nx - x)        # Calcul du coefficient directeur de la fontion
    o = y - cd * x                  # Calcul d el'ordonnée à l'origine

    # Calcul des positions intermediaires
    xint = round(x)
    while xint <= nx :
        yint = cd * xint + o
        #Détection d'obstacle
        a = Background.getElement(background, xint, yint)
        if a == 0 :
            # Déplacement
            setX(animat, nx)
            setY(animat, ny)

        elif a == 1 :     #collision contre le plafond
            setVY(animat, - getVY(animat))
            setX(animat, xint)
            setY(animat, yint)

        elif a == 2 :   #collision contre le mur gauche
            setVX(animat, - getVX(animat))
            setX(animat, xint + 1)
            setY(animat, yint + 1)

        elif a == 3 :   #collision contre le sol ou une plateforme
            setVY(animat, 0) # Pas de rebond sur le sol : on arrète la chute mais pas les déplacements latéraux
            setX(animat, xint)
            setY(animat, yint - 1) # TODO pb si on aborde la plateforme par le bas

        elif a == 4 :   #collisin contre le mur droit
            setVX(animat, - Animat.getVX(animat))
            setX(animat, xint - 1)
            setY(animat, yint + 1)

        else :
            print "error 407 : caractère non supporté"
        return # déplacement impossible : on sort de la fonction move()

        xint = xint + 1
    return

def debug(animat):
    global timeStep, nx, ny, dx, dy, vx, vy, cases, px, py

    x = getX(animat)
    y = getY(animat)

    print "x=", round(x, 2),
    print "y=", round(y, 2)
    print "vx=", round(vx, 2),
    print "vy=", round(vy, 2),
    print " | dx=", round(dx, 2),
    print "dy=", round(dy, 2)
    print "nx=", round(nx, 2),
    print "ny=", round(ny, 2)

#Fonction affichant l'animat
def show(animat) :
    #on se place a la position de l animat dans le terminal
    x=str(int(getX(animat)))
    y=str(int(getY(animat)))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)

    #affichage de l animat
    sys.stdout.write("X")

# Fonctions qui gère les collisions
def collisionBalle(animat,balle) :
    x=Balle.getX(balle)
    y=Balle.getY(balle)
    if getY(animat) == y :
        if getX(animat) == x :
            b=1
        else :
            b=0
    else :
        b=0
    return b

###test###
test=create(1,1)
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
balle={'x':78,'y':2,'vitesseX':8.0,'vitesseY':8.0, 'acceleration':()}
collisionBalle(test, balle)

background = Background.create("fond2.txt")
moveA(test, background, 0.2)
