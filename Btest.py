#-*-coding:utf-8 -*-
#ce module créer notre fond. Il contiendra une chaine de caractére qui representera notre fond
import sys

def create(filename):
    #creation du fond
    fond={'map':[],'fondTableau':[]}        

    #ouverture fichier
    myfile = open(filename, "r")
    chaine=myfile.readlines()
    myfile.close()
    fond['map']=chaine
    tab = conversion(chaine)
    fond['fondTableau']=tab
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
    print fond['map']

def conversion(chaine):
    tableau=[]
    for i in chaine :
        nl=[]
        for c in i :
            if c == "_" :
                nl.append(1)
            elif c == "|" :
                nl.append(2)
            elif c== "*":
                nl.append(3)
            else :
                nl.append(0)
        tableau.append(nl)
    return tableau
    
###test      
fond=create("fond.txt")
show(fond)
