# main.move() V4.2
def move():
    global animat, friction, gravite, timeStep, background
    global nx, ny, dx, dy, vx, vy, cases, px, py

    # Inialisation des variables
    x = Animat.getX(animat)
    y = Animat.getY(animat)
    vx = Animat.getVX(animat)
    vy = Animat.getVY(animat)

    # Application de la friction et de la gravité sur les vitesses pour qu'elles diminuent
    vx = vx - vx * friction
    vy = vy - gravite # avant : vy - vy * gravite
    Animat.setVX(animat, vx)
    Animat.setVY(animat, vy)

    # Calcul de la prochaine position X et Y théorique par rapport à la vitesse
    dx = vx * timeStep
    dy = vy * timeStep
    nx = x + dx
    ny = y - dy  # Car on a un repère orthonormé inversé

    # Détection d'obstacle à la prochaine position
    if Background.getElement(background, px, py) != 0 :
        # Si diffèrent de 0, alors présence d'obstacle : pas de déplacement possible à cette position
        a = Animat.collisionBord(animat, background)
        if a == 1 :
            Animat.setVY(animat, - Animat.getVY(animat) )
        elif a == 2 :
            Animat.setVX(animat, - Animat.getVX(animat) )
        elif a == 0 :
            pass # Pour pas que l'on ai le message d'erreur
        elif a == 3 :
            Animat.setVY(animat, 0) # Pas de rebond sur le sol : on arrète la chute mais pas les déplacements latéraux
        else :
            print "error 407 : caractère non supporté"
        return # déplacement impossible

    # Déplacement
    Animat.setX(animat, nx)
    Animat.setY(animat, ny)

    return
