# main.move() V3:
    # Préparation de la trajectoire
    cases = int( max( abs(nx - x), abs(ny - y) ) )  #abs() : donne la valeur absolue

    # Empecher la division par 0
    if cases == 0 :
        return

    # Calcul des micros déplacements par rapport à notre temps
    dx = (vx * timeStep) / cases   #passage d'une vitesse en (case par seconde) en (case par dt)
    dy = (vy * timeStep) / cases

    # Calcul des positions intermédiaires
    for i in range( 0, cases + 1 ) :
        px = x + i * dx
        py = y - i * dy
        if Background.getElement(background, px, py) != 0 :
            # Si différent de 0, alors présence d'obstacle : pas de déplacement possible à cette position
            a = Animat.collisionBord(animat, background)
            if a == 1 or 3:
                Animat.setVY(animat, - Animat.getVY(animat) )
            elif a == 2 :
                Animat.setVX(animat, - Animat.getVX(animat) )
            elif a == 0 :
                pass # Vérification
            else :
                print "error 407 : caractère non supporté"
            break #les rebonds fonctionnent
        # Déplacement de l'animat a la derniere position sans obstacle
        Animat.setX(animat, px)
        Animat.setY(animat, py)
