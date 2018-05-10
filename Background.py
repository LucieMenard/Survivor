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
        if i == "_" :               # Plafond
            line.append(1)
        elif i == "|" :             # Mur gauche ou droite
            line.append(2)
        elif i == "*" :             # Sol ou plateforme
            line.append(3)
        elif i == " " :             # Case vide
            line.append(0)
        elif i == "\n" :            # Retour à la ligne (LF)
            tableau.append(line)    # On ajoute la ligne à tableau
            line = []               # On reinitialise la ligne
        elif i == "\r" :            # Sous Windows/Mac, on peut avoir des caractères CR, on les ignore
            pass
        else :              # Test d'erreur
            print ord(i), ": Erreur dans le fichier fond2.txt : caractère non supporté "

    return tableau

def getChar(fond,x,y):
    return (fond['map'][y-1][x-1])
def setChar(fond,x,y,number):
    fond['map'][y-1][x-1]=number

def show(fond) : 
    #couleur fond
    sys.stdout.write("\033[40m")
    #couleur white
    sys.stdout.write("\033[37m")
    
    ##goto
    #for y in range(0,len(fond['map'])):
        #for x in range(0,len(fond['map'][y])):
            ##position
            #s="\033["+str(y+1)+";"+str(x+1)+"H"
            #sys.stdout.write(s)
            ##affichage
            #sys.stdout.write(fond['map'][y][x])
    print fond['map']
  
###test###
fond=create("fond2.txt")
show(fond)
