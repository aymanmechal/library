from src.file_manager import BibliothequeAvecFichier
from src.models import *
from src.user_manager import *
from src.exceptions import ErreurBibliotheque
from datetime import *

print("\n=== 1) Création des livres ===")
livre = Livre("Dune", "Frank Herbert", "001")
livre.ajouter_genre("Science-Fiction")
livre.ajouter_genre("Aventure")

livre.exemplaires = [
    {"id": 1, "etat": "disponible"},
    {"id": 2, "etat": "disponible"}
]

livre.file_attente = []

print("Livre créé :", livre)
print("Genres :", livre.genres)
print("Exemplaires :", livre.exemplaires)


print("\n=== 2) Création des utilisateurs ===")
u1 = User("ayman", "1234")
u2 = User("boss", "admin", is_admin=True)

print("User 1 :", u1.username, "| Admin :", u1.is_admin)
print("User 2 :", u2.username, "| Admin :", u2.is_admin)


print("\n=== 3) Emprunt du livre par Ayman ===")
u1.emprunter(livre)
print("Emprunt en cours :", u1.emprunt_en_cours)
print("Exemplaires restants :", sum(1 for ex in livre.exemplaires if ex["etat"] == "disponible"))


print("\n=== 4) Tentative d’emprunt par Boss (pas d’exemplaire dispo) ===")
result = u2.emprunter(livre)
print("Résultat :", result)
print("File d’attente :", [u.username for u in livre.file_attente])
print("Réservations de Boss :", [l.titre for l in u2.reservations])


print("\n=== 5) Retour du livre par Ayman ===")
u1.rendre()

print("Exemplaires après retour :", sum(1 for ex in livre.exemplaires if ex["etat"] == "disponible"))
print("Historique livre :", livre.historique)
print("Emprunt actuel Boss :", u2.emprunt_en_cours)


print("\n=== 6) Retour de Boss ===")
u2.rendre()

print("Historique livre final :", livre.historique)
print("Historique Ayman :", u1.historique)
print("Historique Boss :", u2.historique)
print("Pénalités Ayman :", u1.penalites)
print("Pénalités Boss :", u2.penalites)


print("\n=== 7) Notation du livre ===")
livre.notes = []
livre.notes.append({"user": "ayman", "note": 5})
livre.notes.append({"user": "boss", "note": 4})

moyenne = sum(n["note"] for n in livre.notes) / len(livre.notes)

print("Notes :", livre.notes)
print("Moyenne :", moyenne)


print("\n=== TEST COMPLET TERMINE ===")

