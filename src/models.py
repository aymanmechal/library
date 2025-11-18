import csv
import json

class Livre:
    def __init__(self, titre: str, auteur: str, isbn: str):
        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn

    def afficher(self):
        return f"{self.titre}, {self.auteur} (ISBN: {self.isbn})"


class LivreNumerique(Livre):
    def __init__(self, titre: str, auteur: str, isbn: str, taille_fichier: float):
        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    def afficher(self):
        return f"{super().afficher()}, {self.taille_fichier}MB"


class Bibliotheque:
    def __init__(self, nom, json_path="data/data.json"):
        self.nom = nom
        self.livres = []
        self.json_path = json_path

    def ajouter_livre(self, livre: Livre):
        self.livres.append(livre)
        self.save_to_json()

    def save_to_json(self):
        data = [l.afficher() for l in self.livres]
        
        with open(self.json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def supprimer_par_isbn(self, isbn: str):
        self.livres = [l for l in self.livres if l.isbn != isbn]
        self.save_to_json()

    def recherche_par_titre(self, mot_cle: str):
        return [l for l in self.livres if mot_cle.lower() in l.titre.lower()]

    def recherche_par_auteur(self, auteur: str):
        return [l for l in self.livres if auteur.lower() in l.auteur.lower()]

    def dumpcsv(self, csv_path="data/output.csv"):
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            
            for livre in data:
                writer.writerow([livre]) 
        print(f"Catalogue exporté dans {csv_path}")