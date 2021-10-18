import sys

class Vue :
    def entree (self):
        # sys.stdin.readline() est assez similaire à input()
        # mais tient compte des espaces et peu ne retenir que quelques caractères ex:(2) en paramètre
        return sys.stdin.readline()


class Controleur :
    def stockeEntree(self):
        chaine = vue.entree()
        modele.ajouter(chaine.upper())

    def sauvegardeChaines (self):
        chaines = modele.recupererChaines()
        with open ("test.txt", "w") as f:
            for chaine in chaines :
                f.write(chaine)

class Modele:
    def __init__(self):
        self.chaines = []

    def ajouter(self,chaine):
        self.chaines.append (chaine)

    def recupererChaines(self):
        return self.chaines

vue = Vue()
controleur = Controleur()
modele = Modele()

for i in range(2):
    controleur.stockeEntree()
controleur.sauvegardeChaines()
