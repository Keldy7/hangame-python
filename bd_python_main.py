import turtle
import sqlite3
import random

conn=sqlite3.connect('baseDonnees.db')

cur=conn.cursor()




cur.execute("CREATE TABLE IF NOT EXISTS JOUEUR(Id TEXT PRIMARY KEY, Nom TEXT, Password  TEXT, Score INT)") #création de la table JOUEUR avec ses colonnes
conn.commit()
cur.execute("CREATE TABLE IF NOT EXISTS PARTIE(Id_part INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, Niveau TEXT, Mot TEXT, Victoire TEXT, Id TEXT, FOREIGN KEY(Id) REFERENCES JOUEUR(Id))") #création de la table PARTIE avec ses colonnes
conn.commit()

from bd_python_class import*
from bd_python_fonction import*

#programme principal

 




i=0
print("\n\n\n               LE JEU DU PENDU       \n\n\nKOUAKOU Gnamien Serge-Patrick et Kouassy Besse vous disent:\nBienvenue dans le jeu du pendu!\n\n\n")

pen = turtle.Turtle()   
    # oeil
def eye(col, rad):
    pen.down()
    pen.fillcolor(col)
    pen.begin_fill()
    pen.circle(rad)
    pen.end_fill()
    pen.up()
 

# desiner visage
pen.fillcolor('yellow')
pen.begin_fill()
pen.circle(70)
pen.end_fill()
pen.up()
 
# dessiner oeil
pen.goto(-40, 120)
eye('white', 15)
pen.goto(-37, 125)
eye('black', 5)
pen.goto(40, 120)
eye('white', 15)
pen.goto(40, 125)
eye('black', 5)
 
# dessiner nez
pen.goto(0, 75)
eye('black', 8)
 
# dessiner bouche
pen.goto(-40, 85)
pen.down()
pen.right(90)
pen.circle(40, 180)
pen.up()
turtle.bye() 

print("Le but du jeu est simple: deviner toutes les lettres qui doivent composer un mot, éventuellement avec un nombre limité de tentatives et des thèmes fixés à l'avance. A chaque fois que le joueur devine une lettre, celle-ci est affichée.Dans le cas contraire, il lui restera moins de tentatives pour la suite. Le joueur perd la partie s'il ne lui reste plus de tentative.\n \n\n   Bonne chance!!!\n\n\n")




while((i!='1' )and (i!='2')):
    i=(input("tapez 1 pour inscription ou 2 pour connexion  :"))


if (i=='2'):
    joueur=connexion.connect()
if (i=='1'):
    inscription.inscript()
    joueur=connexion.connect()



joueur.jouerpartie(joueur.Id)
finpartie(joueur)





cur.close()
conn.close()
