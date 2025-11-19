from src.exceptions import ErreurBibliotheque

class Livre:
    def __init__(self, titre: str, auteur: str, isbn: str):

        if not titre.strip():
            raise ErreurBibliotheque("Le titre du livre ne peut pas être vide.")

        if not isbn.strip():
            raise ErreurBibliotheque("L'ISBN ne peut pas être vide.")

        self.titre = titre
        self.auteur = auteur
        self.isbn = isbn

    def afficher(self):
        return f"{self.titre}, {self.auteur} (ISBN: {self.isbn})"


class LivreNumerique(Livre):
    def __init__(self, titre: str, auteur: str, isbn: str, taille_fichier: float):

        if taille_fichier <= 0:
            raise ErreurBibliotheque("La taille du fichier doit être positive.")

        super().__init__(titre, auteur, isbn)
        self.taille_fichier = taille_fichier

    def afficher(self):
        return f"{super().afficher()}, {self.taille_fichier}MB"


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
