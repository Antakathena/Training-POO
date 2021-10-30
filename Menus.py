from typing import Dict, List
import abc
#import datetime
from dataclasses import dataclass, field
#from typing import Tuple


class Controleur:
    def execute(self):
        raise NotImplementedError


class ControleurFactory:
    def make(self, contexte={}):
        raise NotImplementedError


@dataclass
class MenuFactory(ControleurFactory):
    """
    objet_menu = MenuFactory(nom du menu, [liste de couples (("Titre option", Controleur/action)])

    """
    menu_name : str
    start : int = 1
        
    def make(self, contexte={}):
        return Menu(self.menu_name, menu_choice = MENU_CHOICES.get(self.menu_name), start = self.start, contexte=contexte)


@dataclass
class Menu(Controleur):
    menu_name : str
    menu_choice : tuple
    start : int = 1
    contexte: dict = field(default_factory=dict) # sert par exemple à savoir dans quel tournoi on est

    def __post_init__(self):
        self.menu_view = MenuView(self)
        self.contexte = self.contexte.copy()
    
    def show(self): # attention : ne pas re-donner les arguments du init)
        return self.menu_view.show() # ici ils sont appelés par self.mot si besoin)

    def read(self):
        """ construit un menu en fonction de la demande de l'utilisateur"""
        while True:
            selection = self.show()
            if selection == "q": # une solution pour retourner en arrière
                break
            selection = int(selection) - self.start # susceptible de lancer une erreur : int("toto") => ???
            controleur = self.menu_choice[selection][1].make(contexte=self.contexte)
            controleur.execute()

    def execute(self):
        self.read()

@dataclass
class FormFactory(ControleurFactory):
    form_name : str
    start : int = 1

    def make(self, contexte={}):
        return Form(self.form_name, form_questions = FORM_QUESTIONS.get(self.form_name), start = self.start, contexte=contexte)

@dataclass
class Form(Controleur):
    form_name : str
    form_questions : tuple
    start : int = 1
    contexte: dict = field(default_factory=dict) # sert par exemple à savoir dans quel tournoi on est

    def __post_init__(self):
        self.form_view = FormView(self)
        self.contexte = self.contexte.copy()
    
    def show(self): # attention : ne pas re-donner les arguments du init)
        return self.form_view.show() # ici ils sont appelés par self.mot si besoin)

    def read(self):
        """ construit un formulaire en fonction de la demande de l'utilisateur"""
        while True:
            selection = self.show()
            if selection == "q": # une solution pour retourner en arrière
                break
            selection = int(selection) - self.start # susceptible de lancer une erreur : int("toto") => ???
            controleur = self.form_questions[selection][1].make(contexte=self.contexte)
            controleur.execute()

    def execute(self):
        self.read()


# listes de choix de chaque menu (faire fichier exterieur?) :
MENU_CHOICES = {
    "menu principal" : (
        ("Menu Tournois", MenuFactory("menu tournois")),
        ("Menu Joueurs", MenuFactory("menu joueurs")),
        ("Menu Rapports", MenuFactory("menu tournois"))),
    "menu joueurs":(
        ("Entrer un nouveau joueur", FormFactory("Entrer un nouveau joueur")),
        #("Modifier un joueur", FormFactory("Modifier un joueur")), 
        ("Menu rapports", MenuFactory("menu des rapports (joueurs)")),
        ("Retourner au menu principal", MenuFactory("menu principal"))),
    "menu tournois":(
        #("Entrer un nouveau tournoi", FormFactory("Entrer un nouveau joueur")),
        #("Modifier un tournoi", FormFactory("Modifier un joueur")), 
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

FORM_QUESTIONS = {
    "Entrer un nouveau joueur": ("Nom", "Prénom", "Date de naissance", "Genre", "Classement"),
    "Entrer un nouveau tournoi" : ("Nom", "Lieu", "Dates", "Nombre de tours", "Contrôle du temps", "Description"),
}

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
    """Determine l'affichage des menus"""
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
    """Determine l'affichage des form"""
    def __init__(self, form: Form):
        super().__init__(form.form_name)
        self.form: Form = form

    def show(self):
        super().show()
        for i, question in enumerate(self.form.form_questions, start=self.form.start):
            print(f"{i}) {question}")
            input()
            # choice.itemview.show(position=i)
        print("q) Quitter")
       

if __name__ == "__main__":

    print("\n\n----------Essais sur les Controleurs de Training ----------")
    print("\n----------Essais sur MenuFactory :----------\n")

    welcome: View = Welcome()
    welcome.show()

    main_menu = MenuFactory("menu principal").make()
    main_menu.execute()
    print(main_menu)

    