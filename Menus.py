import abc
from typing import Dict, List
#import datetime
from dataclasses import dataclass, field
#from typing import Tuple


FORM_QUESTIONS = {
    "Entrer un nouveau joueur": ("Nom", "Prénom", "Date de naissance", "Genre", "Classement"),
    "Entrer un nouveau tournoi" : ("Nom", "Lieu", "Dates", "Nombre de tours", "Contrôle du temps", "Description"),
}


"""
class Controleur:
    def execute(self):
        raise NotImplementedError
"""

class ControllerFactory(abc.ABC):
    def make(self, contexte={}):
        raise NotImplementedError


@dataclass
class MenuFactory(ControllerFactory):
    """
    objet_menu = MenuFactory(nom du menu, [liste de couples (("Titre option", Controleur/action)])

    """
    menu_name : str
    start : int = 1
        
    def make(self, contexte={}):
        return Menu(self.menu_name, menu_choice = MENU_CHOICES.get(self.menu_name), start = self.start, contexte=contexte)


@dataclass
class Menu:
    menu_name : str
    menu_choice : tuple
    start : int = 1
    contexte: dict = field(default_factory=dict) # sert par exemple à savoir dans quel tournoi on est


@dataclass
class FormFactory(ControllerFactory):
    form_name : str
    start : int = 1

    def make(self, contexte={}):
        return Form(self.form_name, form_questions = FORM_QUESTIONS.get(self.form_name), start = self.start, contexte=contexte)

@dataclass
class Form:
    form_name : str
    form_questions : tuple
    start : int = 1
    contexte: dict = field(default_factory=dict) # sert par exemple à savoir dans quel tournoi on est

MENU_CHOICES = {
    "menu principal" : (
        ("Menu Tournois", MenuFactory("menu tournois")),
        ("Menu Joueurs", MenuFactory("menu joueurs")),
        ("Menu Rapports", MenuFactory("menu tournois"))),
    "menu joueurs":(
        ("Entrer un nouveau joueur", FormFactory("Entrer un nouveau joueur")),
        #("Modifier un joueur", Formulaires.FormFactory("Modifier un joueur")), 
        ("Menu rapports", MenuFactory("menu des rapports (joueurs)")),
        ("Retourner au menu principal", MenuFactory("menu principal"))),
    "menu tournois":(
        #("Entrer un nouveau tournoi", Formulaires.FormFactory("Entrer un nouveau joueur")),
        #("Modifier un tournoi", Formulaires.FormFactory("Modifier un joueur")), 
        ("Lancer le tournoi", MenuFactory("Lancer le tournoi")),
        ("Retourner au menu principal", MenuFactory("menu principal"))),
    "menu lancer le tournoi":(
        ("Lancer le tournoi", MenuFactory("Lancer le tournoi")),
        ("Retourner au menu principal", MenuFactory("menu principal"))),
    "menu lancer le round": (
        ("Lancer le round", MenuFactory("Lancer le round")),
        ("Retourner au menu principal", MenuFactory("menu principal"))),
    "menu des rapports (joueurs)":(
        #("Joueurs par ordre alphabétique", ReportFactory("Joueurs par ordre alphabétique")),
        #("Joueurs par classement", ReportFactory("Joueurs par classement")),
        #("Liste des tournois", ReportFactory("Liste des tournois")),
        ("Retourner au menu principal", MenuFactory("menu principal")))
}

if __name__ == "__main__":

    print("\n\n----------Essais sur les Controleurs de Training ----------")
    print("\n----------Essais sur MenuFactory :----------\n")

    main_menu = MenuFactory("menu principal").make()
    print(main_menu)

    