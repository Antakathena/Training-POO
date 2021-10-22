import abc


class View(abc.ABC):
    """ méthode appelée par un contrôleur, affiche des choses à l'écran, les renvoie au contrôleur"""
    def __init__(self, name):
        self.name = name

    def show_title(self, name):
        self.name = name(str)
        title = name.upper()
        print(f"----------{title}----------")

    def bind(self, controller):
        self.controller = controller

    def draw(self):
        raise NotImplementedError

class MenuView(View):
    """with choices : nous avons les menus tournoi, lancer nouveau tournoi, joueur, rapport"""
    def __init__(self, start=1):
        self.start = start
        super().__init__("MenuView")

    def draw(self):
        for i, choice in enumerate(self.controller.choices, start=self.start):
            choice.itemview.draw(position=i)
        return input("Votre choix : ")

class FormView(View):
    """with items (inputs) : nous avons les formulaires à remplir pour nouveau joueur, nouveau tournoi, demande de rapport
    Il faut auss pouvoir modifier les existants"""
    def __init__(self, start=1):
        self.start = start
        super().__init__("FormView")

    def draw(self):
        print("def draw pour afficher les formulaires à implémenter")

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