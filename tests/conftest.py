import pytest

from src.models import Livre, LivreNumerique, Bibliotheque
from src.file_manager import BibliothequeAvecFichier


@pytest.fixture
def biblio_vide():
    return Bibliotheque("Test")


@pytest.fixture
def biblio_avec_livres(tmp_path):
    json_path = tmp_path / "data.json"
    b = BibliothequeAvecFichier("Test avec fichiers", json_path=str(json_path))

    b.ajouter_livre(Livre("2020", "Lionel Messi", "10"))
    b.ajouter_livre(LivreNumerique("Python", "John Py", "222", 12.5))

    return b



