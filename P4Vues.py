import abc
import P4Controleur
from Menus import Menu


# Pour le test, j'importe les vues avant de résoudre les problèmes d'imports croisés
    
 
class View(abc.ABC):
    """ méthode appelée par un contrôleur, affiche des choses à l'écran, les renvoie au contrôleur"""
    def __init__(self, name):
        self.name = name

# en fait c'est plutôt un décorateur ça : faire décorateur vue qui montre titre, explique "q" et montre la transition?
    def show_title(self):
        title = self.name.upper()
        print(f"-----------{title}-----------")

    @abc.abstractmethod
    def show(self):
        self.show_title()
      
class Welcome(View):
    def __init__(self, name = "Outil de gestion de tournois d'échecs"):
        super().__init__(name)

    def show(self):
        self.show_title()    
        print ("Bienvenue")

class MenuView(View):
    """Determine l'affichage des menus tournoi, lancer nouveau tournoi, joueur,..."""
    def __init__(self, menu: Menu):
        super().__init__(menu.menu_name)
        self.menu: Menu = menu

    def show(self):
        super().show()
        for i, choice in enumerate(self.menu.menu_choice, start=self.menu.start):
            print(f"{i}) {choice[0]}")
            # choice.itemview.show(position=i)
        print("q) Quitter")
        return input("Votre choix : ")

class FormView(View):
    """with items (inputs) : nous avons les formulaires à remplir pour nouveau joueur, nouveau tournoi, demande de rapport
    Il faut auss pouvoir modifier les existants"""
    def __init__(self, start=1):
        self.start = start
        super().__init__("FormView")

    def show(self):
        print("def show pour afficher les formulaires à implémenter")

class ReportView(View):
    """ Défini comment les infos des rapports apparaissent à l'utilisateur"""
    pass

class PlayerView :
    """ Défini comment les infos sur les joueurs apparaissent à l'utilisateur"""
    # sauf si c'est dans le modèle
    pass

class TournamentView :
    """ Défini comment les infos sur les tournois apparaissent à l'utilisateur"""
    # sauf si c'est dans le modèle
    pass

if __name__ == "__main__":
    print("\n\n----------Essais sur les vues de training ----------")
    print("\n----------Essais sur Menus :----------\n")

    welcome = Welcome
    print(welcome)