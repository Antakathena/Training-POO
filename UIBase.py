import abc
#import datetime
from dataclasses import dataclass, field
from P4Controleur import PlayerManager, TournamentManager
import P4Modeles

@dataclass
class ControllerFactory(abc.ABC):
    def make(self):
        raise NotImplementedError


@dataclass
class UIFactory(ControllerFactory):
    """
    Récupère les informations dans le dictionnaire ITEMS:
    "titre" =  infos à afficher pour demander un input ,Controller
    objet_menu = IFactory(nom du menu, (liste de couples (("Titre option", Controleur/action)))
    objet_form = IFactory(nom du form, (liste de questions", Controleur/action - ex : créer nouveau joueur)])

    """
    name : str
    start : int = 1
        
    def make(self):
        return UI(self.name, items = ITEMS.get(self.name), start = self.start)


@dataclass
class UI:
    name : str
    items : tuple
    start : int = 1



ITEMS = {
    "menu principal" : (
        ("Menu Tournois", UIFactory("menu tournois")), 
        ("Menu Joueurs", UIFactory("menu joueurs")), 
        ("Menu Rapports", UIFactory("menu rapports"))),
    "menu joueurs":(
        ("Entrer un nouveau joueur", UIFactory("Entrer un nouveau joueur")),
        #("Modifier un joueur", IFactory("Modifier un joueur")), 
        ("Menu rapports", UIFactory("menu des rapports (joueurs)")),
        ("Retourner au menu principal", UIFactory("menu principal"))),
    "menu tournois":(
       ("Entrer un nouveau tournoi", UIFactory("Entrer un nouveau tournoi")),
        #("Modifier un tournoi", IFactory("Modifier un joueur")), 
        ("Lancer le tournoi", UIFactory("Lancer le tournoi")),
        ("Retourner au menu principal", UIFactory("menu principal"))),
    "menu lancer le tournoi":(
        ("Lancer le tournoi", UIFactory("Lancer le tournoi")),
        ("Retourner au menu principal", UIFactory("menu principal"))),
    "menu lancer le round": (
        ("Lancer le round", UIFactory("Lancer le round")),
        ("Retourner au menu principal", UIFactory("menu principal"))),
    "menu des rapports (joueurs)":(
        #("Joueurs par ordre alphabétique", ReportFactory("Joueurs par ordre alphabétique")),
        #("Joueurs par classement", ReportFactory("Joueurs par classement")),
        #("Liste des tournois", ReportFactory("Liste des tournois")),
        ("Retourner au menu principal", UIFactory("menu principal"))),
    "Entrer un nouveau joueur": (
        (P4Modeles.PLAYER_FIELDS, PlayerManager)), # FormFactory
    "Entrer un nouveau tournoi" : (
        (P4Modeles.TOURNAMENT_FIELDS, TournamentManager)),   
}

""" 
class View(abc.ABC):
    méthode appelée par un contrôleur, affiche des choses à l'écran, les renvoie au contrôleur
    def __init__(self, name):
        self.name = name

    def show_title(self):
        title = self.name.upper()
        print(f"-----------{title}-----------")

    @abc.abstractmethod
    def show(self):
        self.show_title()


class UIView(View):
    Determine l'affichage des interfaces utilisateurs : menus et formulaires
    def __init__(self, ui: UI):
        super().__init__(ui.name)
        self.ui: UI = ui

    def show(self):
        super().show()
        if self.name.startswith("menu"):
            for num, choice in enumerate(self.ui.items, start=self.ui.start):
                print(f"{num}) {choice[0]}")
            selection = input("Votre choix:")
            return selection
        # le else est la vue questionnaire :    
        else : 
            answers = list()
            for question in self.ui.items[0] :
                print(question)
                current = input()
                if current == "q":
                    break
                else :
                    answers.append(current)
            print(answers)
            return answers
       
       

class UIManager(Controller):
    def __init__(self, ui, view):
        self.ui : UI = ui 
        self.view : UIView =  view 
        self.start = self.ui.start
        self.name = self.ui.name
        self.items = self.ui.items
    
    def show(self): # attention : ne pas re-donner les arguments du init)
        return self.view.show() # ici ils sont appelés par self.mot si besoin)

    def read(self):
        construit un menu en fonction de la demande de l'utilisateur
        while True:
            if self.name.startswith("menu"):
                selection = self.show()
                if selection == "q": 
                    break
                selection = selection.strip()
                if selection.isdigit():
                    selection = int(selection) - self.start # susceptible de lancer une erreur : int("toto") => ??
                    i = self.items[selection][1].make() # en fait menu ici peut être form ou menu, ou (?) rapport
                    assert isinstance(i, UI)
                    vue = UIView(i)
                    controleur = UIManager(i, vue)
                    controleur.execute()
                    assert isinstance (controleur, Controller) # MenuManager
                else :
                    print("Choix non valide")
                    #self.read()
            else: # gestion si on a un formulaire
                answers = self.show()
                if answers == "q": 
                    break
                else :
                    controleur = self.items[1](answers)
                    controleur.add_new(answers)
                # convertissement des answers en objets python
                # ex: date de naissance => objet Date()
                #for i, answer in enumerate(answers):
                # try:
                #   answers[i] = self.items[0][i][1](answer) # attention : peut raise une exception                         
                # except :
                #self.items[1](*answers) # Controleur.methode(answers[0], answers[1], answers[2], ...)
                # récupérer answers et avec add_new en faire un dictionnaire et db.insert

    def execute(self):
        self.read()

"""

if __name__ == "__main__":

    print("\n----------Essais sur IFactory :----------\n")

    menu_principal = UIFactory("menu principal").make()
    new_player = UIFactory("Entrer un nouveau joueur").make()