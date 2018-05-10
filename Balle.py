# -*-coding: utf-8 -*-
#Ce module sert à la création des balles
import sys

def create(Vx,Vy) :
    return {'x':78,'y':2,'vitesseX':Vx,'vitesseY':Vy, 'acceleration':()}
    
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
    
def getAcceleration(balle):
    return balle['acceleration']
def setAcceleration(balle,number):
    balle['acceleration']=number  
    
def droite(balle) :
    setX(balle,getX(balle)+1)
    return
def gauche(balle) :
    setX(balle,getX(balle)-1)
    return

def sauter(balle):   #TODO choisir si je le met or not
    global temps
    setVY(balle, getVY(balle)+temps*9.81)  #9.81 la valeur peut changer pour que ce soit plus réaliste
    setX(balle, getX(balle)+getVX(balle)*temps)
    setY(balle,getY(balle)+getVY(balle)*temps)

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
    
def collisionBord(balle,fond) :
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
