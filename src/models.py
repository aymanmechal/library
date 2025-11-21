import json
from src.exceptions import ErreurBibliotheque
from datetime import *

class Livre:
    def __init__(self, titre: str, auteur: str, isbn: str):

        if not titre.strip():
            raise ErreurBibliotheque("Le titre du livre ne peut pas être vide")

        if not auteur.strip():
            raise ErreurBibliotheque("L'auteur ne peut pas être vide")

        if not isbn.strip():
            raise ErreurBibliotheque("L'ISBN ne peut pas être vide")

        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn
        
        self.historique = []
        self.genres = []
        
        self.file_attente = []
        self.exemplaires = []
        self.exemplaires.append({"etat": "disponible"})

        
        self.notes = []
        self.commentaires = []
        
    def exemplaires_disponibles(self):
        count = 0
        for ex in self.exemplaires:
            if ex["etat"] == "disponible":
                count += 1
        return count

    def ajouter_exemplaire(self):
        self.exemplaires.append({"etat": "disponible"})

    def prendre_exemplaire(self):
        for ex in self.exemplaires:
            if ex["etat"] == "disponible":
                ex["etat"] = "emprunté"
                return ex
        return None

    def rendre_exemplaire(self, exemplaire):
        exemplaire["etat"] = "disponible"

    def ajouter_commentaire(self, username, texte):
        self.commentaires.append({"user": username, "commentaire": texte})

    def ajouter_note(self, username, note):
        self.notes.append({"user": username, "note": note})

    def moyenne_notes(self):
        if not self.notes:
            return None
        total = 0
        for n in self.notes:
            total += n["note"]
        return total / len(self.notes)

    def ajouter_genre(self, genre):
        if genre not in self.genres:
            self.genres.append(genre)


    def afficher(self):
        base = f"{self.titre}, {self.auteur} (ISBN: {self.isbn})"
        
        if hasattr(self, "genres") and self.genres:
            genres_str = ", ".join(self.genres)
            return f"{base}, Genres : {genres_str}"
        
        return base

    
    def __str__(self):
        return self.afficher()
    
    def __repr__(self):
        return self.afficher()


class LivreNumerique(Livre):
    def __init__(self, titre: str, auteur: str, isbn: str, taille_fichier: float):

        if taille_fichier <= 0:
            raise ErreurBibliotheque("La taille du fichier doit être positive.")

        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    def afficher(self):
        return f"{super().afficher()}, {self.taille_fichier}MB"
    
    def __str__(self):
        return self.afficher()
    
    def __repr__(self):
        return self.afficher()



class Bibliotheque:
    def __init__(self, nom: str):

        if not nom.strip():
            raise ErreurBibliotheque("Le nom de la bibliothèque ne peut pas être vide.")

        self.nom = nom
        self.livres = []

    def ajouter_livre(self, livre: Livre):
        self.livres.append(livre)

    def supprimer_par_isbn(self, isbn: str):
        self.livres = [l for l in self.livres if l.isbn != isbn]

    def recherche_par_titre(self, mot_cle: str):
        return [l for l in self.livres if mot_cle.lower() in l.titre.lower()]

    def recherche_par_auteur(self, auteur: str):
        return [l for l in self.livres if auteur.lower() in l.auteur.lower()]


class User:
    Limites = {
    "basique": {"max": 2, "jours": 14, "penalite": 0.5},
    "premium": {"max": 5, "jours": 21, "penalite": 0.2},
    "VIP": {"max": 10, "jours": 30, "penalite": 0.0}
    }

    
    def __init__(self, username, password, is_admin=False):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        
        self.emprunt_en_cours = None
        self.historique = []
        
        self.emprunts_mois = 0
        self.penalites = 0.0
        
        self.reservations = []
        
        self.abonnement = "basique"
        self.abonnement_expire = date.today() + timedelta(days=30)
        
        if not username.strip():
            raise ErreurBibliotheque("Le username ne peut pas être vide")
        if not password.strip():
            raise ErreurBibliotheque("Le mot de passe ne peut pas être vide")

    def to_data(self):
        return {
            "username": self.username,
            "password": self.password,
            "is_admin": self.is_admin,
            "abonnement": self.abonnement,
            "abonnement_expire": self.abonnement_expire.isoformat()
        }

       
    def est_admin(self):
        return self.is_admin

    def limites(self):
        return User.Limites[self.abonnement]
    
    def abonnement_est_valide(self):
        return date.today() <= self.abonnement_expire

    def peut_emprunter(self):
        if self.penalites > 0:
            raise ErreurBibliotheque("Pénalités impayées")

        if self.emprunt_en_cours is not None:
            raise ErreurBibliotheque("Déjà un emprunt en cours")

        if not self.abonnement_est_valide():
            raise ErreurBibliotheque("Abonnement expiré")

        lim = self.limites()
        if self.emprunts_mois >= lim["max"]:
            raise ErreurBibliotheque("Limite d'emprunts mensuels atteinte")

        return True

    def emprunter(self, livre):
        self.peut_emprunter()

        exemplaire_dispo = None
        for ex in livre.exemplaires:
            if ex["etat"] == "disponible":
                exemplaire_dispo = ex
                break

        if exemplaire_dispo is None:
            livre.file_attente.append(self)
            self.reservations.append(livre)
            return "Ajouté à la file d'attente"

        exemplaire_dispo["etat"] = "emprunté"

        self.emprunt_en_cours = {
            "livre": livre,
            "exemplaire": exemplaire_dispo,
            "date_emprunt": datetime.now(),
            "date_de_retour": datetime.now() + timedelta(days=self.limites()["jours"])
        }

        self.emprunts_mois += 1
        return f"Exemplaire {exemplaire_dispo['id']} emprunté"


    def rendre(self):
        if self.emprunt_en_cours is None:
            raise ErreurBibliotheque("Aucun emprunt en cours")

        emprunt = self.emprunt_en_cours
        livre = emprunt["livre"]
        exemplaire = emprunt["exemplaire"]
        date_retour = datetime.now()

        retard = (date_retour - emprunt["date_de_retour"]).days
        if retard > 0:
            self.penalites += retard * self.limites()["penalite"]

        self.historique.append(emprunt)

        livre.rendre_exemplaire(exemplaire)

        livre.historique.append({
            "user": self.username,
            "exemplaire": exemplaire,
            "date_emprunt": emprunt["date_emprunt"],
            "date_retour": date_retour
        })

        self.emprunt_en_cours = None

        if livre.file_attente:
            prochain_user = livre.file_attente.pop(0)
            prochain_user.reservations.remove(livre)

            nouvel_exemplaire = livre.prendre_exemplaire()

            prochain_user.emprunt_en_cours = {
                "livre": livre,
                "exemplaire": nouvel_exemplaire,
                "date_emprunt": datetime.now(),
                "date_de_retour": datetime.now() + timedelta(days=prochain_user.limites()["jours"])
            }

            prochain_user.send_email(
                f"Le livre '{livre.titre}' est disponible"
            )

    def send_email(self, message):
        print(f"Email pour {self.username}:  {message}")


    def reset_mensuel(self):
        if datetime.now().day == 1:
            self.emprunts_mois = 0
            
    def noter_livre(self, livre, note):
        if not (0 <= note <= 5):
            raise ErreurBibliotheque("La note doit être entre 0 et 5")
        for emprunt in self.historique:
            if not emprunt["livre"] is livre:
                raise ErreurBibliotheque("Vous ne pouvez noter que les livres que vous avez empruntés")
        livre.ajouter_note(self.username, note)

    def commenter_livre(self, livre, texte):
        for emprunt in self.historique:
            if not emprunt["livre"] is livre:
                raise ErreurBibliotheque("Vous ne pouvez commenter que les livres que vous avez empruntés")
        
        livre.ajouter_commentaire(self.username, texte)

    def recommandations(self, bibliotheque):
        genres_lus = []

        for emprunt in self.historique:
            livre = emprunt["livre"]
            for genre in livre.genres:
                genres_lus.append(genre)

        if not genres_lus:
            return [] 

        comptage = {}

        for genre in genres_lus:
            if genre not in comptage:
                comptage[genre] = 1
            else:
                comptage[genre] += 1

        genre_pref = None
        max_count = 0

        for genre, count in comptage.items():
            if count > max_count:
                max_count = count
                genre_pref = genre

        recommandations = [l for l in bibliotheque.livres if genre_pref in l.genres]

        return recommandations

            


