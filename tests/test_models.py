import pytest

from src.models import Livre, LivreNumerique, Bibliotheque
from src.exceptions import ErreurBibliotheque

def test_creer_livre_ok():
    livre = Livre("1984", "George Orwell", "111")
    assert livre.titre == "1984"
    assert livre.auteur == "George Orwell"
    assert livre.isbn == "111"

def test_afficher_livre():
    livre = Livre("1984", "George Orwell", "111")
    txt = livre.afficher()
    assert "1984" in txt
    assert "George Orwell" in txt
    assert "ISBN: 111" in txt

def test_livre_titre_vide():
    with pytest.raises(ErreurBibliotheque):
        Livre("", "Auteur", "999")

def test_livre_titre_espaces():
    with pytest.raises(ErreurBibliotheque):
        Livre("   ", "Auteur", "999")

def test_livre_isbn_vide():
    with pytest.raises(ErreurBibliotheque):
        Livre("Titre", "Auteur", "")

def test_livre_isbn_espaces():
    with pytest.raises(ErreurBibliotheque):
        Livre("Titre", "Auteur", "   ")

def test_creer_livrenumerique_ok():
    livre = LivreNumerique("Python", "John", "222", 12.5)
    assert livre.taille_fichier == 12.5

def test_afficher_livrenumerique():
    livre = LivreNumerique("Python", "John", "222", 12.5)
    txt = livre.afficher()
    assert "MB" in txt
    assert "12.5" in txt

def test_livrenumerique_taille_zero():
    with pytest.raises(ErreurBibliotheque):
        LivreNumerique("Ebook", "Auteur", "333", 0)

def test_livrenumerique_taille_negative():
    with pytest.raises(ErreurBibliotheque):
        LivreNumerique("Ebook", "Auteur", "333", -1)

def test_livrenumerique_heritage():
    livre = LivreNumerique("Titre", "Auteur", "555", 10)
    assert livre.titre == "Titre"
    assert livre.auteur == "Auteur"
    assert livre.isbn == "555"

def test_biblio_nom_valide():
    b = Bibliotheque("Médiathèque")
    assert b.nom == "Médiathèque"

def test_biblio_nom_vide():
    with pytest.raises(ErreurBibliotheque):
        Bibliotheque("")

def test_biblio_nom_espaces():
    with pytest.raises(ErreurBibliotheque):
        Bibliotheque("   ")

def test_ajouter_livre_simple(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A", "X", "1"))
    assert len(biblio_vide.livres) == 1

def test_ajouter_livrenumerique(biblio_vide):
    biblio_vide.ajouter_livre(LivreNumerique("Ebook", "Moi", "10", 5))
    assert isinstance(biblio_vide.livres[0], LivreNumerique)

def test_ajouter_plusieurs_livres(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","X","1"))
    biblio_vide.ajouter_livre(Livre("B","Y","2"))
    biblio_vide.ajouter_livre(Livre("C","Z","3"))
    assert len(biblio_vide.livres) == 3

def test_supprimer_isbn_existant(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","X","1"))
    biblio_vide.ajouter_livre(Livre("B","Y","2"))
    biblio_vide.supprimer_par_isbn("1")
    assert len(biblio_vide.livres) == 1
    assert biblio_vide.livres[0].isbn == "2"

def test_supprimer_isbn_inexistant(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","X","1"))
    biblio_vide.supprimer_par_isbn("999")
    assert len(biblio_vide.livres) == 1

def test_supprimer_sur_biblio_vide(biblio_vide):
    biblio_vide.supprimer_par_isbn("1")
    assert len(biblio_vide.livres) == 0

def test_supprimer_isbn_duplique(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","X","1"))
    biblio_vide.ajouter_livre(Livre("B","Y","1"))
    biblio_vide.supprimer_par_isbn("1")
    assert len(biblio_vide.livres) == 0
    
def test_recherche_titre_un_seul(biblio_vide):
    biblio_vide.ajouter_livre(Livre("Python débutant","A","1"))
    biblio_vide.ajouter_livre(Livre("Football","B","2"))
    r = biblio_vide.recherche_par_titre("Python")
    assert len(r) == 1

def test_recherche_titre_plusieurs(biblio_vide):
    biblio_vide.ajouter_livre(Livre("Python A","A","1"))
    biblio_vide.ajouter_livre(Livre("Python B","B","2"))
    r = biblio_vide.recherche_par_titre("Python")
    assert len(r) == 2

def test_recherche_titre_aucun(biblio_vide):
    biblio_vide.ajouter_livre(Livre("Python","A","1"))
    r = biblio_vide.recherche_par_titre("Java")
    assert r == []

def test_recherche_titre_insensible_casse(biblio_vide):
    biblio_vide.ajouter_livre(Livre("Python","A","1"))
    r = biblio_vide.recherche_par_titre("python")
    assert len(r) == 1

def test_recherche_titre_sous_chaine(biblio_vide):
    biblio_vide.ajouter_livre(Livre("Python débutant","A","1"))
    r = biblio_vide.recherche_par_titre("début")
    assert len(r) == 1

def test_recherche_auteur_un_seul(biblio_vide):
    biblio_vide.ajouter_livre(Livre("Titre","Alice","1"))
    r = biblio_vide.recherche_par_auteur("Alice")
    assert len(r) == 1

def test_recherche_auteur_plusieurs(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","Alice","1"))
    biblio_vide.ajouter_livre(Livre("B","Alice","2"))
    r = biblio_vide.recherche_par_auteur("Alice")
    assert len(r) == 2

def test_recherche_auteur_aucun(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","Bob","1"))
    r = biblio_vide.recherche_par_auteur("Alice")
    assert r == []

def test_recherche_auteur_insensible_casse(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","Alice","1"))
    r = biblio_vide.recherche_par_auteur("alice")
    assert len(r) == 1

def test_recherche_auteur_sous_chaine(biblio_vide):
    biblio_vide.ajouter_livre(Livre("A","Alice","1"))
    r = biblio_vide.recherche_par_auteur("Ali")
    assert len(r) == 1
