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
        
        try:
            with open(self.json_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except PermissionError:
            print("Erreur : impossible d'écrire dans le fichier JSON (permissions insuffisantes).")


    def supprimer_par_isbn(self, isbn: str):
        self.livres = [l for l in self.livres if l.isbn != isbn]
        self.save_to_json()

    def recherche_par_titre(self, mot_cle: str):
        return [l for l in self.livres if mot_cle.lower() in l.titre.lower()]

    def recherche_par_auteur(self, auteur: str):
        return [l for l in self.livres if auteur.lower() in l.auteur.lower()]
    
    def dumpcsv(self, csv_path="data/output.csv"):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("Erreur : impossible de charger le JSON avant l'export CSV.")
            return
        except PermissionError:
            print("Erreur : impossible de lire le JSON (permissions insuffisantes).")
            return

        try:
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Livre"])  

                for livre in data:
                    writer.writerow([livre])

            print(f"Catalogue exporté dans {csv_path}")

        except PermissionError:
            print("Erreur : impossible d'écrire dans le fichier CSV (permissions insuffisantes).")


    
    def load_from_json(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("Erreur : fichier JSON introuvable.")
            return
        except json.JSONDecodeError:
            print("Erreur : le fichier JSON est invalide ou corrompu.")
            return
        except PermissionError:
            print("Erreur : impossible de lire le fichier JSON (permissions insuffisantes).")
            return

        self.livres = []

        for texte in data:
            if "MB" in texte:
                titre_auteur, reste = texte.split("(ISBN:")
                titre, auteur = titre_auteur.split(",")
                isbn, taille = reste.replace(")", "").split(",")
                livre = LivreNumerique(titre.strip(), auteur.strip(), isbn.strip(), float(taille.replace("MB", "")))
            else:
                titre_auteur, reste = texte.split("(ISBN:")
                titre, auteur = titre_auteur.split(",")
                isbn = reste.replace(")", "").strip()
                livre = Livre(titre.strip(), auteur.strip(), isbn)

            self.livres.append(livre)

