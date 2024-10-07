"""
TP2 : Système de gestion de livres pour une bibliothèque

Groupe de laboratoire : 01  
Numéro d'équipe : 01
Noms et matricules : Gaetan Lohier (2371634), Jad Charbachi (2381646)
"""
import csv
from datetime import datetime

########################################################################################################## 
# PARTIE 1 : Création du système de gestion et ajout de la collection actuelle
########################################################################################################## 

# TODO : Écrire votre code ici
csv_collection = open("collection_bibliotheque.csv", newline='')

collection = csv.DictReader(csv_collection)

bibliotheque  = dict()

for c in collection:
    bibliotheque[c["cote_rangement"]] = dict(titre = c["titre"], auteur = c["auteur"], date_publication = c["date_publication"])
    
print(f' \n Bibliotheque initiale : {bibliotheque} \n')

########################################################################################################## 
# PARTIE 2 : Ajout d'une nouvelle collection à la bibliothèque
########################################################################################################## 

# TODO : Écrire votre code ici


csv_nvCollection = open("nouvelle_collection.csv", newline='')

nvCollection = csv.DictReader(csv_nvCollection)

for c in nvCollection:
    if c["cote_rangement"] in bibliotheque:
        print(f"Le livre {c["cote_rangement"]} ---- {c["titre"]} par {c["auteur"]} ---- est déjà présent dans la bibliothèque")
    else:
        bibliotheque[c["cote_rangement"]] = {"titre":c["titre"], "auteur":c["auteur"], "date_publication":c["date_publication"]}
        print(f"Le livre {c["cote_rangement"]} ---- {c["titre"]} par {c["auteur"]} ---- a été ajouté avec succès")


########################################################################################################## 
# PARTIE 3 : Modification de la cote de rangement d'une sélection de livres
########################################################################################################## 

# TODO : Écrire votre code ici

toRemove = [ b for b in bibliotheque if "Shakespeare" in bibliotheque[b]["auteur"]]

bibliotheque.update({"W" + r : bibliotheque[r] for r in toRemove})

for r in toRemove:
    bibliotheque.pop(r)

print(f" \n Bibliotheque avec modifications de cote : {bibliotheque} \n")



########################################################################################################## 
# PARTIE 4 : Emprunts et retours de livres
########################################################################################################## 

# TODO : Écrire votre code ici

csv_emprunts = open("emprunts.csv", newline='')

emprunts = csv.DictReader(csv_emprunts)

bibliotheque.update({"emprunts" : dict()})
    
for b in bibliotheque:
    for e in emprunts:
        if b == e["cote_rangement"]:
            bibliotheque["emprunts"][b] = dict( etat = "emprunté", date_emprunt = e["date_emprunt"])
            break
    else:
        bibliotheque["emprunts"][b] = dict( etat = "disponible", date_emprunt = None)
        csv_emprunts.seek(0)
    

print(f' \n Bibliotheque avec ajout des emprunts : {bibliotheque} \n')

########################################################################################################## 
# PARTIE 5 : Livres en retard 
########################################################################################################## 

# TODO : Écrire votre code ici
today = datetime.now()
bibliotheque.update({"livres_perdus" : []})
bibliotheque.update({"frais_retard" : {}})

for e in bibliotheque["emprunts"]:
    if bibliotheque["emprunts"][e]["etat"] == "emprunté":
        date_emprunt = datetime.fromisoformat(bibliotheque["emprunts"][e]["date_emprunt"])
        temps_emprunt = abs(date_emprunt - today)
        if  (temps_emprunt.days > 365):
            bibliotheque["livres_perdus"].append(e)
            
        elif temps_emprunt.days > 30:
            frais = min((temps_emprunt.days - 30) * 2 , 100)
            bibliotheque["frais_retard"].update({e : frais})
            
print(f' \n Bibliotheque avec ajout des retards et frais : {bibliotheque} \n')



