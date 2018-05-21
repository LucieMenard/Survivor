# main.move() V2.2
def move() :
    global animat, friction, gravite, background

    # Ajuste la vitesse en X en fonction de la friction
    vx = Animat.getVX(animat)
    vx = vx - vx * friction
    Animat.setVX(animat, vx)

    # Calcule la prochaine position théorique en X
    x = Animat.getX(animat)
    nx = x + vx

    # Récupère la position en Y
    y = Animat.getY(animat)

    # Teste s'il y a un obstacle entre les positions x et nx
    if x < nx: # quand on va de gauche à droite
        while x < nx:
            element = Background.getElement(background, x + 1, y)
            if element != 0:
                Animat.setVX(animat, -vx)
                Animat.setX(animat, x)
                break
            x = x + 1
        if x > nx:
            x = nx

    else: # quand on va de droite à gauche
        while x > nx:
            element = Background.getElement(background, x - 1, y)
            if element != 0:
                Animat.setVX(animat, -vx)
                break
            x = x - 1
        if x < nx :
            x = nx

    # Place l'animat que sa nouvelle position en X
    Animat.setX(animat, x)

    ## Mouvement en Y
    #Animat.setVY(animat, Animat.getVY(animat)*gravite)
    #NY = Animat.getY(animat) + Animat.getVY(animat)
    ## TODO faire detection d'obstacle
