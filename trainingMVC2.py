# POO avec Python p.181

class Vue:
    def __init__(self, nom_fichier):
        self.fichier = open(nom_fichier, "r")

    def __del__(self):
        self.fichier.close()

    def entree(self) :
        return self.fichier.readline()

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

    class ListeChaine :
        def __init__(self):
            self.chaines = []

        def sauvegarder (self, chaine) :
            self.chaines.append (chaine)

        def charger(self):
            return self.chaines

    def __init__(self):
        self.liste = Modele.ListeChaine()

    def ajouter (self, chaine):
        self.liste.sauvegarder(chaine)

    def recupererChaines(self):
        return self.liste.charger()

vue = Vue("mvc2.txt")
controleur = Controleur()
modele = Modele()

for i in range(2):
    controleur.stockeEntree()
controleur.sauvegardeChaines()

# Essais perso :
with open("mvc2.txt", "r") as f:
    lignes = f.readlines()
    for ligne in lignes:
        print(ligne)

with open("mvc2.txt", "r") as f:        
    texte = f.read() # lit tout le contenu et renvoie une chaîne de caractères uniques
    #texte = texte.split(" ") # coupe la chaîne en mots et renvoie la liste >>> ['pif', 'paf\nbim', 'boum']
    texte = str(texte).replace("\n"," ").split()
    print(texte)
    mot = texte[3]
    print(mot)