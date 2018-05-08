#-*-coding:utf-8 -*-
#ce module créer notre fond. Il contiendra une chaine de caractére qui representera notre fond
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
    #fond ['fondTableau'] = conversion (chaine)
    
    return fond

def conversion(chaine):
    tableau = []
    nl = []
    for i in chaine :
        for c in i :
            if c == "_" :       # Plafond
                nl.append(1)    
            elif c == "|" :     # Mur gauche ou droite
                nl.append(2)
            elif c== "*":       # Sol ou plateforme
                nl.append(3)
            elif c==" ":        # Case vide
                nl.append(0)
            else :
                print "Erreur dans le fichier fond2.txt : caractère non supporté";
        tableau.append(nl) # La dernière ligne de fond2.txt ne doit pas contenir de retour à la ligne
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
