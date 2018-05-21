# Version 1.2 du main.move()
def move():
    #déplacement de l'animat
    if Animat.collisionBord(animat,background) == 1 :
        rebondissementsAPlafond()
    elif Animat.collisionBord(animat,background) == 2 :
        rebondissementsAMur()
    elif Animat.collisionBord(animat,background) == 3 :
        rebondissementsASol()
    else:
        chuteAnimat()

    #déplacement des balles
    global listeDeBalle
    for i in listeDeBalle :
            if Balle.collisionBord(i,background) == 1 :
                rebondissementsBPlafond()
            elif Balle.collisionBord(i,background) == 2 :
                rebondissementsBMur()
            elif Balle.collisionBord(i,background) == 3 :
                rebondissementsBSol()
            else:
                chuteBalle()

    #contact Animat et Balle
    contactBalleAnimat()

def rebondissementsAPlafond():
    #rebondissements contre le plafond
    Balle.setVY(animat, -Balle.getVY(animat))

def rebondissementsAMur():
    #rebondissements contre le mur
    Balle.setVX(animat, -Balle.getVX(animat))
def rebondissementsASol():
    Animat.setVX(animat,0)
    Animat.setVY(animat,0)
    #TODO si on est en fin de chute alors plus de mvt donc juste passe
def chuteAnimat():
        #TODO faire la chute
    #Animat.setVY(animat,Animat.getVY(animat)+temps*(-9.81) )  #9.81 la gravité
    #Animat.setX(animat,Animat.getX(animat)+Animat.getVX(animat)*temps)
    #Animat.setY(animat,Animat.getY(animat)+Animat.getVY(animat)*temps)
    pass

def rebondissementsBMur():
    return
def rebondissementsBPlafond():
    return
def rebondissementsBSol():
    return
def chuteBalle():
