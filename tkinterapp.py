from tkinter import *
from tkinter import ttk, messagebox

from src.models import Livre, LivreNumerique, Bibliotheque
from src.file_manager import BibliothequeAvecFichier
from src.exceptions import ErreurBibliotheque


class AppBibliotheque:
    def __init__(self):
        self.bibliotheque = Bibliotheque()
        
        self.fenetre = Tk()
        self.fenetre.title("Bibliothèque")
        self.fenetre.geometry("400x500")
        
        self.creer_interface()
        self.fenetre.mainloop()


    def creer_interface(self):
        label_titre = ttk.Label(self.fenetre, text="Titre")
        label_titre.pack()
        self.entree_titre = ttk.Entry(self.fenetre)
        self.entree_titre.pack()
        
        label_auteur = ttk.Label(self.fenetre, text="Auteur")
        self.entree_auteur = ttk.Entry(self.fenetre)
        self.entree_auteur.pack()
        
        label_isbn = ttk.Label(self.fenetre, text="ISBN")
        self.entree_isbn = ttk.Entry(self.fenetre)
        self.entree_isbn.pack()
        
        bouton_ajout = ttk.Button(self.fenetre, text="Ajouter un livre", command=self.ajouter_livre)
        bouton_ajout.pack(pady=10)
        
        self.zone_liste = Text(self.fenetre, height=10)
        self.zone_liste.pack(fill="both", expand=True, pady=10)
        
        self.zone_recherche = ttk.Label(self.fenetre, text="Rechercher par auteur :")
        self.zone_recherche.pack()
        self.entree_recherche = ttk.Entry(self.fenetre)
        self.entree_recherche.pack()
        
        bouton_recherche = ttk.Button(self.fenetre, text="Rechercher", command=self.rechercher_auteur)
        bouton_recherche.pack(pady=10)

    def ajouter_livre(self):
        titre = self.entree_titre.get()
        auteur = self.entree_auteur.get()
        isbn = self.entree_isbn.get()

        try:
            livre = Livre(titre, auteur, isbn)
            self.bibliotheque.ajouter_livre(livre)
            self.afficher_livres()
        except ErreurBibliotheque as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def afficher_livres(self):
        self.zone_liste.delete("1.0", END)
        for livre in self.bibliotheque.livres:
            ligne = livre.afficher() + "\n"
            self.zone_liste.insert(END, ligne)
        
    def rechercher_auteur(self):
        auteur = self.entree_recherche.get().lower()
        
        self.zone_liste.delete("1.0",END)
        
        for livre in self.bibliotheque.livres:
            if auteur in livre["auteur"].lower():
                ligne = livre.afficher() + "\n"
                self.zone_liste.insert(END, ligne)
                
                
app = AppBibliotheque()
