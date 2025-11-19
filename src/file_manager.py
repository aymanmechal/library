import json
import csv

from src.models import Bibliotheque, Livre, LivreNumerique
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
            print("Permission refusée !")
            raise ErreurBibliotheque("Permission refusée !")

        else:
            print("Lecture réussie !")

        finally:
            try:
                fichier.close()
            except:
                pass

    def load_from_json(self):
        try:
            fichier = open(self.json_path, "r", encoding="utf-8")
            contenu = fichier.read()
            data = json.loads(contenu)

        except FileNotFoundError:
            print("Fichier non trouvé !")
            raise ErreurBibliotheque("Fichier non trouvé !")

        except PermissionError:
            print("Permission refusée !")
            raise ErreurBibliotheque("Permission refusée !")

        except json.JSONDecodeError:
            print("Format invalide !")
            raise ErreurBibliotheque("Format invalide !")

        else:
            print("Lecture réussie !")

            self.livres = []

            for texte in data:
                if "MB" in texte:
                    titre_auteur, reste = texte.split("(ISBN:")
                    titre, auteur = titre_auteur.split(",")
                    isbn, taille = reste.replace(")", "").split(",")
                    livre = LivreNumerique(
                        titre.strip(),
                        auteur.strip(),
                        isbn.strip(),
                        float(taille.replace("MB", ""))
                    )
                else:
                    titre_auteur, reste = texte.split("(ISBN:")
                    titre, auteur = titre_auteur.split(",")
                    isbn = reste.replace(")", "").strip()
                    livre = Livre(titre.strip(), auteur.strip(), isbn)

                self.livres.append(livre)

        finally:
            try:
                fichier.close()
            except:
                pass

    def dumpcsv(self, csv_path: str = "data/output.csv"):
        try:
            fichier_json = open(self.json_path, "r", encoding="utf-8")
            data = json.load(fichier_json)

        except FileNotFoundError:
            print("Fichier non trouvé !")
            raise ErreurBibliotheque("Fichier non trouvé !")

        except PermissionError:
            print("Permission refusée !")
            raise ErreurBibliotheque("Permission refusée !")

        except json.JSONDecodeError:
            print("Format invalide !")
            raise ErreurBibliotheque("Format invalide !")

        else:
            print("Lecture réussie !")

        finally:
            try:
                fichier_json.close()
            except:
                pass

        try:
            fichier_csv = open(csv_path, "w", newline="", encoding="utf-8")
            writer = csv.writer(fichier_csv)
            writer.writerow(["Livre"])

            for livre in data:
                writer.writerow([livre])

        except PermissionError:
            print("Permission refusée !")
            raise ErreurBibliotheque("Permission refusée !")

        else:
            print("Lecture réussie !")

        finally:
            try:
                fichier_csv.close()
            except:
                pass
