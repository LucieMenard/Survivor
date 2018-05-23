#-*-coding:utf-8 -*-
#ce module crée notre fond. Il contiendra une chaine de caractères qui representera notre fond
import sys

def create(filename):
    #Création du fond
    fond={ ' map ' : [], ' fondTableau ' : []}

    #Ouverture du fichier
    myfile =  open(filename, 'r' )

    #Charger le contenu
    chaine = myfile.read()   #ou myfile.readlines()

    #Fermer le fichier
    myfile.close()

    #Initialisation des structures
    fond['map'] = chaine
    fond ['fondTableau'] = conversion (chaine)

    return fond

def conversion(chaine):
    #Initialisation des variables locales
    tableau = []
    line = []

    #Parcours de la chaine de caractère éléments par éléments pour la conversion
    for i in chaine :
        #if i == "_" :              # Plafond
            #line.append(1)
        #elif i == "H" :            # Mur gauche
            #line.append(2)
        if i == "*" :               # Sol ou plateforme
            line.append(3)
        elif i == " " :             # Case vide
            line.append(0)
        elif i == "\n" :            # Retour à la ligne (LF)
            tableau.append(line)    # On ajoute la ligne à tableau
            line = []               # On reinitialise la ligne
        elif i == "\r" :            # Sous Windows/Mac, on peut avoir des caractères CR, on les ignore
            pass
        else :                      # Test d'erreur
            print ord(i), ": Erreur dans le fichier fond2.txt : caractère non supporté "
    return tableau

def getChar(fond, x, y):
    print int(round(y)),int(round(x))
    print fond['map'][int(round(y))][int(round(x))]
    return (fond['map'][int(round(y))][int(round(x))])

def setChar(fond, x, y, caractere):
    fond['map'][y][x]= caractere

def getElement(fond, x, y):
    x = int(round(x)) - 1 # arrondi
    y = int(round(y)) - 1
    # on teste s'il s'agit d'un element plus loin que le plafond ou le sol
    if y<= 0 or y>= len(fond['fondTableau']) - 1 :
        return 3
    # on teste s'il s'agit d'un element plus loin que les murs
    if x<= 0 or x >= len(fond['fondTableau'][y]) - 1 :
        return 3

    return fond['fondTableau'][y][x]

def show(fond) :
    #couleur fond
    sys.stdout.write("\033[40m")
    #couleur white
    sys.stdout.write("\033[37m")
    print fond['map']

###test###
fond=create("fond2.txt")
show(fond)
