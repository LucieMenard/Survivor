#-*-coding:utf-8 -*-
#Ce module sert à la création du personnage du joueur
import sys
import Background
import Balle

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
    setVY(animat, getVY(animat) + 6)  #TODO choisir valeur pour la poussée que l'on donne lors du saut

#Fonction affichant l'animat
def show(animat) :
    #on se place a la position de l animat dans le terminal
    x=str(int(getX(animat)))
    y=str(int(getY(animat)))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    #affichage de l animat
    sys.stdout.write("\033[31m") # texte en rouge
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
