from src.models import *


b = Bibliotheque("Médiathèque")
b.ajouter_livre(Livre("2020", "Lionel Messi", "10"))
b.ajouter_livre(LivreNumerique("Python", "John Py", "222", 12.5))

print("Mes livres : ")
for livre in b.livres:
    print(livre)
    

b.save_to_json("data/biblio.json")
