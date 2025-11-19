from src.models import *

b = Bibliotheque("Médiathèque")

b.ajouter_livre(Livre("2020", "Lionel Messi", "10"))
b.ajouter_livre(LivreNumerique("Python", "John Py", "222", 12.5))

for livre in b.livres:
    print(livre.afficher())

b.save_to_json()

b2 = Bibliotheque("Copie")
b2.load_from_json()

for livre in b2.livres:
    print(livre.afficher())

b.dumpcsv()
