import pytest
from datetime import datetime, timedelta

from src.models import *


def test_user_creation_ok():
    u = User("ayman", "1234")
    assert u.username == "ayman"
    assert u.password == "1234"
    assert u.abonnement == "basique"


def test_user_creation_username_vide():
    with pytest.raises(ErreurBibliotheque):
        User("", "pass")


def test_user_creation_password_vide():
    with pytest.raises(ErreurBibliotheque):
        User("ayman", "")


def test_user_admin():
    u = User("admin", "pass", is_admin=True)
    assert u.est_admin() is True


def test_abonnement_valide():
    u = User("ayman", "1234")
    assert u.abonnement_est_valide() is True


def test_abonnement_expire():
    u = User("ayman", "1234")
    u.abonnement_expire = datetime.today() - timedelta(days=1)
    assert u.abonnement_est_valide() is False


def test_user_limites_abonnement_basique():
    u = User("ayman", "1234")
    limites = u.limites()
    assert limites["max"] == 2
    assert limites["jours"] == 14


def test_emprunt_simple_ok():
    u = User("ayman", "pass")
    livre = Livre("Dune", "Herbert", "1")
    livre.exemplaires = [{"id": 1, "etat": "disponible"}]

    u.emprunter(livre)
    assert u.emprunt_en_cours is not None


def test_emprunt_refuse_si_penalite():
    u = User("ayman", "1234")
    u.penalites = 5.0
    livre = Livre("Dune", "Herbert", "1")
    livre.exemplaires = [{"id": 1, "etat": "disponible"}]

    with pytest.raises(ErreurBibliotheque):
        u.emprunter(livre)


def test_emprunt_refuse_si_deja_emprunt():
    u = User("ayman", "1234")
    livre = Livre("Dune", "Herbert", "1")
    livre.exemplaires = [{"id": 1, "etat": "disponible"}]

    u.emprunter(livre)

    with pytest.raises(ErreurBibliotheque):
        u.emprunter(livre)


def test_emprunt_refuse_si_limite_mensuelle():
    u = User("ayman", "1234")
    u.emprunts_mois = u.limites()["max"]  # déjà au max
    livre = Livre("Dune", "Herbert", "1")
    livre.exemplaires = [{"id": 1, "etat": "disponible"}]

    with pytest.raises(ErreurBibliotheque):
        u.emprunter(livre)


def test_rendre_sans_retard():
    u = User("ayman", "1234")
    livre = Livre("Dune", "Herbert", "1")
    livre.exemplaires = [{"id": 1, "etat": "disponible"}]

    u.emprunter(livre)
    emprunt = u.emprunt_en_cours
    emprunt["date_de_retour"] = datetime.now() + timedelta(days=1)

    u.rendre()
    assert u.penalites == 0
    assert len(u.historique) == 1


def test_rendre_avec_retard():
    u = User("ayman", "1234")
    livre = Livre("Dune", "Herbert", "1")
    livre.exemplaires = [{"id": 1, "etat": "disponible"}]

    u.emprunter(livre)
    emprunt = u.emprunt_en_cours
    emprunt["date_de_retour"] = datetime.now() - timedelta(days=2)

    u.rendre()

    assert u.penalites > 0


def test_file_attente_si_pas_exemplaire():
    u1 = User("a", "1")
    u2 = User("b", "1")
    livre = Livre("Dune", "Herbert", "1")
    livre.file_attente = []
    livre.exemplaires = []

    msg = u1.emprunter(livre)
    assert msg == "Ajouté à la file d'attente"
    assert u1 in livre.file_attente


def test_reservation_attribue_exemplaire_automatiquement():
    u1 = User("a", "1")
    u2 = User("b", "1")

    livre = Livre("Dune", "Herbert", "1")
    livre.file_attente = []
    livre.exemplaires = [{"id": 1, "etat": "disponible"}]

    u1.emprunter(livre)
    livre.exemplaires = []      # plus aucun dispo
    u2.emprunter(livre)         # va en file d'attente

    livre.exemplaires = [{"id": 1, "etat": "disponible"}]
    u1.rendre()                 # transmet au suivant

    assert u2.emprunt_en_cours is not None
    assert u2.emprunt_en_cours["livre"] == livre
