import json
import csv

from src.models import Bibliotheque, Livre, LivreNumerique, User
from src.exceptions import ErreurBibliotheque


class BibliothequeAvecFichier(Bibliotheque):
    def __init__(self, nom: str, json_path: str = "data/data.json"):
        super().__init__(nom)
        self.json_path = json_path

    def save_to_json(self):
        data = [l.afficher() for l in self.livres]

        try:
            fichier = open(self.json_path, "w", encoding="utf-8")
            json.dump(data, fichier, indent=4, ensure_ascii=False)

        except PermissionError:
            raise ErreurBibliotheque("Permission refusée !")
    

    def load_from_json(self):
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

        except FileNotFoundError:
            raise ErreurBibliotheque("Fichier non trouvé !")
        except PermissionError:
            raise ErreurBibliotheque("Permission refusée !")
        except json.JSONDecodeError:
            raise ErreurBibliotheque("Format JSON invalide !")

        self.livres = []

        for item in data:
            if item["type"] == "numerique":
                livre = LivreNumerique(
                    item["titre"],
                    item["auteur"],
                    item["isbn"],
                    item["taille"]
                )
            else:
                livre = Livre(
                    item["titre"],
                    item["auteur"],
                    item["isbn"]
                )

            self.livres.append(livre)


    def dumpcsv(self, csv_path: str = "data/output.csv"):
        try:
            fichier_json = open(self.json_path, "r", encoding="utf-8")
            data = json.load(fichier_json)

        except FileNotFoundError:
            raise ErreurBibliotheque("Fichier non trouvé !")

        except PermissionError:
            raise ErreurBibliotheque("Permission refusée !")

        except json.JSONDecodeError:
            raise ErreurBibliotheque("Format invalide !")

        try:
            fichier_csv = open(csv_path, "w", newline="", encoding="utf-8")
            writer = csv.writer(fichier_csv)
            writer.writerow(["Livre"])

            for livre in data:
                writer.writerow([livre])

        except PermissionError:
            raise ErreurBibliotheque("Permission refusée !")