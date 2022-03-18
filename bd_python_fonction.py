

import sqlite3

conn=sqlite3.connect('baseDonnees.db')

cur=conn.cursor()








def Classement():       #fonction qui classe tous les joueurs dans une liste
    L=[]
    req="SELECT *FROM JOUEUR"
    result=cur.execute(req)
    for i in result:
         ID=int(i[0])
         SCORE=int(i[3])
         tu=[ID]
         tu.append(SCORE)
         L.append(tu)

    n=len(L)
    for i in range(0,n-1):
        for j in range(i+1,n):
            if (L[i][1])<(L[j][1]):
                M=L[i][1]
                M0=L[i][0]
                L[i][1]=L[j][1]
                L[i][0]=L[j][0]
                L[j][1]=M
                L[j][0]=M0

    return L    #on a parcouru les enregistrements de la table JOUEUR et on a classés les scores en meme temps que les joueurs avec un tri 


def finpartie(joueur):                                                  #fonction agissant après la fin d'une partie
        option=0
        while(option!='1' and option!='2' and option!='3'):
            option=(input("Tapez 1 pour une nouvelle partie  \n Tapez 2 pour d'autres options \n Tapez 3 pour quitter le jeu:\n\n"))
        if option=='1':  #on joue une nouvelle partie
            joueur.jouerpartie(joueur.Id)
            finpartie(joueur)

        if option=='3':  #on quitte le jeu
            exit()

        if option=='2':  #le joueur peut accède à différentes options comme modiifer ses infos, consulter son rang et la liste des 10 meilleurs joueurs
            choix=0
            while(choix!='1' and choix!='2' and choix!='3'):
                choix=(input("Entrez 1 pour modifier vos infos\n Entrez 2 pour consulter votre rang\n Entrez 3 pour consulter la liste des 10 meilleurs joueurs : \n"))
            if choix=='1':

                mot_passe=input("Entrez votre mot de passe actuel :")  
                cur.execute("SELECT Password FROM JOUEUR WHERE ID=?",(joueur.Id,))
                x=cur.fetchone()
                passwd=x[0]
                while(passwd!=mot_passe):                                     #le joueur doit entrer son mot de passe actuel
                    print("Mot de passe erroné \n")
                    mot_passe=input("Entrez votre mot de passe actuel  :\n")
                    cur.execute("SELECT Password FROM JOUEUR WHERE ID=?",(joueur.Id,))
                    x=cur.fetchone()
                    passwd=x[0]
  
                
                nom=input("Entrez votre nouveau nom :")                      #le joueur a maintenant la possibilité de changer son nom et son mot de passe
                joueur.Nom=nom
                cur.execute("UPDATE JOUEUR SET Nom = ? WHERE Id = ? ", (joueur.Nom, joueur.Id))
                conn.commit()
                mot_de_passe=input("Entrez votre nouveau mot de passe :")
                joueur.Password=mot_de_passe
                cur.execute("UPDATE JOUEUR SET Password = ? WHERE Id = ? ", (joueur.Password, joueur.Id))
                conn.commit()
                                                                            #on fait une mise à jour des données enregistrées 
                print("Modification effectuée avec succès!!\n\n")
                

            if choix=='2':
                L=Classement()
                for i in L:
                    if (i[0]==joueur.Id):
                        rang=L.index(i)+1

                print("Vous etes le numéro {}\n\n".format(rang))                #les joueurs étant déja classés dans la liste, on affiche le rang y correspondant au score


            if choix=='3':
                L=Classement()
                LL=[[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4],[4,4]] #initialisation d'un liste 2 X 10  pour y ranger les 10 premiers (nom et score)
                nbc=0
                req="SELECT *FROM JOUEUR"
                result=cur.execute(req)
                for i in result:
                    nbc+=1
                
                for i in range(0,10):
                   if i<nbc: 
                    LL[i][1]=L[i][1]
                    cur.execute("SELECT Nom FROM JOUEUR WHERE ID=?",(L[i][0],))
                    x=cur.fetchone()
                    x=x[0]
                    LL[i][0]=(x)
                    print(LL[i][0])

                for i in range(0,10):
                   if i<nbc:  
                     print("Le numero {} est {} avec {} ECO.\n".format(i+1,LL[i][0],LL[i][1]))    # on affice les 10 meilleurs joueurs
                    
                    
            finpartie(joueur)
    
