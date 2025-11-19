import pytest
import json
import os

from src.file_manager import BibliothequeAvecFichier
from src.models import Livre, LivreNumerique
from src.exceptions import ErreurBibliotheque

def test_save_cree_fichier(biblio_avec_livres):
    b = biblio_avec_livres
    b.save_to_json()
    assert os.path.exists(b.json_path)

def test_save_contenu_correct(biblio_avec_livres):
    b = biblio_avec_livres
    b.save_to_json()
    with open(b.json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 2
    assert any("Lionel Messi" in line for line in data)

def test_save_biblio_vide(tmp_path):
    path = tmp_path / "data.json"
    b = BibliothequeAvecFichier("Test", json_path=str(path))
    b.save_to_json()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == []

def test_load_reconstruit_biblio(tmp_path):
    path = tmp_path / "data.json"
    b = BibliothequeAvecFichier("Test", json_path=str(path))

    b.ajouter_livre(Livre("Titre","A", "1"))
    b.ajouter_livre(LivreNumerique("Python","B","2",10))
    b.save_to_json()

    b2 = BibliothequeAvecFichier("Copie", json_path=str(path))
    b2.load_from_json()

    assert len(b2.livres) == 2
    assert any(isinstance(l, LivreNumerique) for l in b2.livres)

def test_load_ecrase_anciens_livres(tmp_path):
    path = tmp_path / "data.json"
    b = BibliothequeAvecFichier("Test", json_path=str(path))

    b.ajouter_livre(Livre("A","X","1"))
    b.save_to_json()

    b2 = BibliothequeAvecFichier("Copie", json_path=str(path))
    b2.ajouter_livre(Livre("B","Y","2"))
    b2.load_from_json()
    assert len(b2.livres) == 1
    assert b2.livres[0].titre == "A"

def test_load_fichier_inexistant(tmp_path):
    path = tmp_path / "absent.json"
    b = BibliothequeAvecFichier("Test", json_path=str(path))
    with pytest.raises(ErreurBibliotheque):
        b.load_from_json()

def test_load_json_invalide(tmp_path):
    path = tmp_path / "data.json"
    with open(path, "w") as f:
        f.write("ceci n'est pas du json")
    b = BibliothequeAvecFichier("Test", json_path=str(path))
    with pytest.raises(ErreurBibliotheque):
        b.load_from_json()

def test_dumpcsv_cree_fichier(tmp_path, biblio_avec_livres):
    csv = tmp_path / "data.csv"
    biblio_avec_livres.save_to_json()
    biblio_avec_livres.dumpcsv(str(csv))
    assert os.path.exists(csv)

def test_dumpcsv_nombre_lignes(tmp_path, biblio_avec_livres):
    csv = tmp_path / "data.csv"
    biblio_avec_livres.save_to_json()
    biblio_avec_livres.dumpcsv(str(csv))
    with open(csv, "r") as f:
        lignes = f.readlines()
    assert len(lignes) >= 2

def test_dumpcsv_contenu(tmp_path, biblio_avec_livres):
    csv = tmp_path / "data.csv"
    biblio_avec_livres.save_to_json()
    biblio_avec_livres.dumpcsv(str(csv))
    with open(csv, "r") as f:
        contenu = f.read()
    assert "Python" in contenu

def test_dumpcsv_json_inexistant(tmp_path):
    csv = tmp_path / "data.csv"
    json_path = tmp_path / "absent.json"
    b = BibliothequeAvecFichier("Test", json_path=str(json_path))
    with pytest.raises(ErreurBibliotheque):
        b.dumpcsv(str(csv))

def test_dumpcsv_json_invalide(tmp_path):
    csv = tmp_path / "data.csv"
    json_path = tmp_path / "data.json"
    with open(json_path, "w") as f:
        f.write("pas du json")
    b = BibliothequeAvecFichier("Test", json_path=str(json_path))
    with pytest.raises(ErreurBibliotheque):
        b.dumpcsv(str(csv))
