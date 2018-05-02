# -*-coding: utf-8 -*-
#Ce module sert à la création des balles
import sys

def create(Vx,Vy) :
    balle={'x':78,'y':2,'vitesseX':Vx,'vitesseY':Vy, 'acceleration':()}
    return balle
    
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
    global dt
    setVY(balle, getVY(balle)+dt*9.81)  #9.81 la valeur peut changer pour que ce soit plus réaliste
    setX(balle, getX(balle)+getVX(balle)*dt)
    setY(balle,getY(balle)+getVY(balle)*dt)

def show(balle) : 

    #on se place a la position de la balle dans le terminal
    x=str(int(getX(balle)))
    y=str(int(getY(balle)))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    
    #couleur fond noire
    sys.stdout.write("\033[40m")

    #affichage de l animat
    sys.stdout.write("O\n")
    
def collisionBord(balle,fond) :
    fondTableau = fond['fondTableau']
    for i in fondTableau :
        if i == 0:  
            c3=0
        elif i == 1 :
            c3=1
        else:
            c3=2
    return c3


###test      
if __name__ : '__main__'
balle1=create(4.0,3.0)
print balle1
