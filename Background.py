#-*-coding:utf-8 -*-
#ce module créer notre fond. Il contiendra une chaine de caractére qui representera notre fond
import sys

def create(filename):
    # Initialise la structure qui gère le fond
    fond = {
        # map contient la version graphique du fond, c'est juste une chaine avec le contenu du fichier fonds.txt 
        'map': '',
        
        # fondTableau contient le type de chauqe case du fond : 
        # - 0 : c'est vide
        # - 1 : c'est le sol, le plafond ou une plateforme
        # - 2 : c'est le mur de droite ou de gauche
        'fondTableau': []
    }        

    # Ouvre le fichier
    myfile = open(filename, "r")
    
    # Charge le contenu
    # chaine=myfile.readlines()         # Avant : lit le fichier ligne par ligne et retourne une <list> (i.e. "split")
    chaine = myfile.read()              # Après : lit le fichier en un seul coup et retourne une <chaine>
    
    # Ferme le fichier     
    myfile.close()
    
    # Initialise nos structures
    fond['map'] = chaine
    fond['fondTableau'] = conversion(chaine)

    # Ok    
    return fond

def getChar(fond,x,y):
    return (fond['map'][y-1][x-1])
    
def setChar(fond,x,y,number):
    fond['map'][y-1][x-1]=number

def show(fond) : 
    #couleur fond
    sys.stdout.write("\033[40m")
    #couleur white
    sys.stdout.write("\033[37m")
    
    #goto
    for y in range(0,len(fond["map"])):
        for x in range(0,len(fond["map"][y])):
            s="\033["+str(y+1)+";"+str(x+1)+"H"
            sys.stdout.write(s)
            #affiche
            sys.stdout.write(fond["map"][y][x])

def conversion(chaine):
    tableau = []
    nl = []
    for i in chaine :
        for c in i :
            if c == "_" :       # Sol, plafond ou plateforme
                nl.append(1)    
            elif c == "|" :     # Mur gauche ou droite
                nl.append(2)
            elif c== "*":
                nl.append(3)
            else :
                print "Erreur dans le fichier fond.txt : caractère non supporté\n";
                
    tableau.append(nl) # La dernière ligne de fond.txt ne doit pas contenir de retour à la ligne
    
    return tableau
    
###test      
if __name__ : '__main__'

print create("fond.txt")
