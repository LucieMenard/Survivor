#-*-coding:utf-8 -*-
#ce module créer notre fond. Il contiendra une chaine de caractére qui representera notre fond
import sys

def  create ( filename ):
    # création du fond
    fond = { ' map ' : [], ' fondTableau ' : []}        
    # ouverture fichier
    myfile =  open(filename, "r" )
    chaine = myfile.readlines ()
    monfichier.close ()
    fond[ ' map ' ] = chaine
    fond[ ' fondTableau ' ] = conversion (chaine)
    return fond

def  getChar( fond , x , y ):
     return (fond [ ' map ' ] [y - 1 ] [x - 1 ])
    
def  setChar ( fond , x , y , nombre ):
    fond [ ' map ' ] [y - 1 ] [x - 1 ] = nombre

def  show( fond ):
    # couleur fond
    sys.stdout.write ("\ 033 [40m ")
    # couleur blanc
    sys.stdout.write ("\ 033 [37m ")
    
    # goto
    for y in range( 0 , len (fond [" carte "])):
        for x in range( 0 , len (fond [" map "] [y])):
            s = " \ 033 [ " + str (y + 1 ) + " ; " + str (x + 1 ) + " H "
            sys.stdout.write (s)
             # affiche
            sys.stdout.write (fond [" map "] [y] [x])

def conversion(chaine):
    tableau = []
    for i in chaine:
        nl = []
        for c in i:
            if c == "_" :
                nl.append(1)
            elif c ==  "|" :
                nl.append(2)
            elif c == "*" :
                nl.append(3)
            else :
                nl.appendw  (0)
        tableau.append (nl)
    return tableau
    
###test###      
create ( " fond2.txt " )
