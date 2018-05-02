#-*-coding:utf-8 -*-
#Ce module sert à la création du personnage du joueur
import sys
import Background
import Balle

def create(y) :
    animat={'x':2,'y':y,'vitesseX':3.0,'vitesseY':4.0,'acceleration':()}
    return animat
        
def getX(animat) :
    return animat['x']
def setX(animat,number) :
    animat['x']=number
    
def getY(animat) :
    return animat['y']
def setY(animat,number) :
    animat['y']=number
    
def droite(animat) :
    setX(animat,getX(animat)+1)

def gauche(animat) :
    setX(animat,getX(animat)-1)

def sauter(animat,temps):  #TODO pb avec le saut : vitesse en y en qq sorte pas prise en compte
    setVY(animat,getVY(animat)+temps*(-9.81) )  #9.81 la gravité
    setX(animat,getX(animat)+getVX(animat)*temps)
    setY(animat,getY(animat)+getVY(animat)*temps)  #0.1 est dt 

def getVX(animat):
    return animat['vitesseX']
def setVX(animat,number):
    animat['vitesseX']=number

def getVY(animat):
    return animat['vitesseY']
def setVY(animat,number):
    animat['vitesseY']=number

def show(animat) : 
    #on se place a la position de l animat dans le terminal
    x=str(int(getX(animat)))
    y=str(int(getY(animat)))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)

    #affichage de l animat
    sys.stdout.write("X")

def collisionBord(animat,fond) :
    fondTableau = fond['fondTableau']
    for i in fondTableau :
        if i == 1:  
            c1=1
        elif i== 2:
            c1=2
        elif i == 3 :
            c1=3
        else:
            c1=0
    return c1
    
def collisionBalle(animat,balle) :
    a=Balle.getX(balle)
    b=Balle.getY(balle)
    if getY(animat) == b:   #remplacer 1 par la condition
        if getX(animat) == a :
            c2=1
        else :
            c2=0
    else :
        c2=0
    return c2
    
    
###test      
if __name__ : '__main__'
test=create(1)
print test


