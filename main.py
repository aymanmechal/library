from src.models import Livre, LivreNumerique
from src.file_manager import BibliothequeAvecFichier
from src.exceptions import ErreurBibliotheque

b = BibliothequeAvecFichier("Médiathèque")

try:
    b.ajouter_livre(Livre("2020", "Lionel Messi", "10"))
    b.ajouter_livre(LivreNumerique("Python", "John Py", "222", 12.5))

    print("=== Livres en mémoire ===")
    for livre in b.livres:
        print(livre.afficher())

    b.save_to_json()

    b2 = BibliothequeAvecFichier("Copie", json_path=b.json_path)
    b2.load_from_json()

    print("\n=== Livres rechargés ===")
    for livre in b2.livres:
        print(livre.afficher())

    b.dumpcsv()

except ErreurBibliotheque as e:
    print("Erreur :", e)
