
import sqlite3
import random
import dico_francais as dico
from unicodedata import normalize
def asciize(s):  #fonction qui enleve les accents
    return normalize("NFKD",s).encode("ascii", "ignore").decode("ascii")

conn=sqlite3.connect('baseDonnees.db')

cur=conn.cursor()




class Joueur:                                            #Création de la classe joueur et initiation des attributs
    def __init__(self, Nom, Password, Id,score):
        self.Id=Id 
        self.Nom=Nom
        self.Password=Password
        self.score=score
        self.succ=0    #cette variable va nous permettre de compter les victoires successives du joueur
        

    def jouerpartie(self, Id):                               #définition de la méthode jouer
        niv=0                                                #on initialise le niveau, le nombre de caractères du mot et le nombre de vie qui varieront en fonction du niveau
        nbc=0
        pvie=0
        lt=""
        print("\n\t Nouvelle partie")
        while((niv!='1') and (niv!='2') and (niv!='3')):
            niv=(input("Sélectionnez un niveau:\n\n 1- pour facile 2- pour moyen et 3 pour difficile  :"))    #choix de niveau et tconséquences

        if (niv=='1'):
            nbcp=0
            nbcg=6
            pvie=10
            vic=10
            lose=5
            
        if (niv=='2'):
            nbcp=6
            nbcg=10
            pvie=7
            vic=100
            lose=50
            
        if (niv=='3'):
            nbcp=10
            nbcg=26
            vic=500
            lose=100
            pvie=5

        m=random.choice(dico.dico_fr)               #choix aléatoire du mot 
        while((len(m)>nbcg) or (len(m)<=nbcp)):
            m=random.choice(dico.dico_fr)
        m=asciize(m)

        L=len(m)-2                                 #on remplace par pointillé tous les caractères du mot sauf le premier et le dernier
        affichage=m[0]+("_ ")*L+m[-1]
        print("Début de la partie")                                               

                                             
        while(pvie>0):                      #code du jeu du pendu : le mot caché est devoilé au fur et à mesure que les lettres sont trouvées
            print(affichage)
            print("Il vous reste {} points de vie".format(pvie))
            proposition=input("Proposez une lettre  :")
            proposition.lower
            
            affichage=list(affichage)          #si la lettre proposée est dans le mot, elle se dévoile
            if proposition in m:
                print("Bien joué\n\n\n\n")
                for i in range(0,len(m)):
                    if proposition==m[i]:
                        affichage[i]=proposition
            else:                             #si une mauvaise lettre est choisie, le joueur perd un point de vie
                pvie-=1
                print("Désolé, Cette lettre n'est pas dans le mot\n\n\n")

            affichage="".join(affichage)
            if ("_" not in affichage):        #le joueur gagne, il est alors récompensé
                
                print("Bravoo! Vous avez gagné la partie\n\n")
                tpl=(self.Id,niv,m, "OUI")
                cur.execute("INSERT INTO PARTIE(Id, Niveau, Mot, Victoire)  VALUES(?,?,?,?)",tpl)  #on enregistre la partie dans notre base
                conn.commit()
                print("Vous gagnez {} ECO".format(vic))
                print("Le mot à deviner était {}".format(m))
                self.score+=vic
                self.succ+=1   #incrémentation car le joueur a une victoire succesives de plus
                if(self.succ==5):
                    print("Félicitations!! Vous recevez 20 ECO pour avoir enchainé 5 victoires consécutives")
                    self.score+=20
                if(self.succ==7):
                    print("Félicitations!! Vous recevez 50 ECO pour avoir enchainé 7 victoires consécutives")
                    self.score+=50
                if(self.succ==10):
                    print("Félicitations!! Vous recevez 100 ECO pour avoir enchainé 10 victoires consécutives")
                    self.score+=100
                    
                break

        if  (pvie)==0:
            print("Vous avez perdu la partie\n\n")   #le joueur perd la partie, il perd aussi des points
            tpl=(self.Id,niv,m, "NON")
            cur.execute("INSERT INTO PARTIE(Id, Niveau, Mot, Victoire)  VALUES(?,?,?,?)",tpl)  #on enregistre la partie dans notre base
            conn.commit()
            print("Vous perdez {} ECO".format(lose))
            print("Le mot à deviner était {}".format(m))
            
            self.score-=lose
            self.succ=0  #annulation car le joueur vient de perdre

        sql='UPDATE JOUEUR SET Score = ? WHERE Id = ? '  #on met à jour le score dans la base de données
        value=(self.score, self.Id)
        cur.execute(sql,value)
        conn.commit()
        print("Votre score total est de {} ECO :\n\n".format(self.score))
        



class inscription():

  def inscript():                               #fonction inscription   on permet à un nouveau joueur de se faire enregistrer

    print("Inscription\n")   #on demande les infos du joueur à s'inscrire
    nom=input("Entrez votre nom  :")
    mot_passe=input("créez un mot de passe et mémorisez-le!! :")
    
    Id=int(input("Entrez votre numéro de téléphone:"))            #le numéro de téléphone étant personnel, est chosi pour identifier le joueur
    tuId=(Id,)
    cur.execute("SELECT Id FROM JOUEUR WHERE Id=?",tuId)
    pnone=cur.fetchone()
    while(pnone!=None):                                           #on verifie que le numéro entré n'est pas déja dans notre base de donnée
        print("Cet numero est déja l'identifiant d'un joueur")
        Id=int(input("Entrez votre numéro de téléphone:"))
        tuId=(Id,)
        cur.execute("SELECT Id FROM JOUEUR WHERE Id=?",tuId)
        pnone=cur.fetchone()
        
    joueur=Joueur(nom, mot_passe, Id,0)
    a=(joueur.Id, joueur.Nom, joueur.Password, joueur.score)    
    cur.execute("INSERT INTO JOUEUR VALUES(?,?,?,?)",a)         #le joueur est désormais inscrit
    conn.commit()
    print("Votre ID est {}".format(Id))



class connexion:        #classe connexion  qui favorise la connexion à la BD 

 def connect():            #methode connect  on donne acces à un joueur déja inscrit
    print("\n\t Connexion \n")
    
    ID=int(input("Entrez votre ID  :"))
    tu=(ID,)
    cur.execute("SELECT Nom FROM JOUEUR WHERE Id=?",tu)
    a=cur.fetchone()
    while(a==None):                                 #on verifie que ce joueur est déja enregistré
        print("Cet ID n'est pas reconnu")
        ID=(input("Entrez votre ID  :"))
        tu=(ID,)
        cur.execute("SELECT Nom FROM JOUEUR WHERE Id=?",tu)
        a=cur.fetchone()
        
    a=''.join(a)
    b=a
    print("Bienvenue", a)
    mot_passe=input("Entrez votre mot de passe  :")

    cur.execute("SELECT Password FROM JOUEUR WHERE ID=?", tu)
    a=cur.fetchone()
    a=''.join(a)
    
    while(mot_passe!=a ):
        mot_passe=input("mot de passe erroné, entrez de nouveau")  # on lui demande son mot de passe pour le connecter
    
    cur.execute("SELECT Score FROM JOUEUR WHERE ID=?", tu)
    x=cur.fetchone()
    x=x[0]
    
    joueur=Joueur(a,b,ID,x)                 #on connecte le joueur
    print("Bienvenue {} , Votre score est de {} Eco".format(b,joueur.score))

    return joueur

    





        

