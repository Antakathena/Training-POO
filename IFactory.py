import abc
#import datetime
from dataclasses import dataclass, field
from P4Controleur import PlayerManager, TournamentManager
import P4Modeles


class ControllerFactory(abc.ABC):
    def make(self, contexte={}):
        raise NotImplementedError


@dataclass
class IFactory(ControllerFactory):
    """
    Récupère les informations dans le dictionnaire ITEMS:
    "titre" =  infos à afficher pour demander un input ,Controller
    objet_menu = IFactory(nom du menu, (liste de couples (("Titre option", Controleur/action)))
    objet_form = IFactory(nom du form, (liste de questions", Controleur/action - ex : créer nouveau joueur)])

    """
    Iname : str
    start : int = 1
        
    def make(self, contexte={}):
        return I(self.Iname, choice = ITEMS.get(self.Iname), start = self.start, contexte=contexte)



@dataclass
class I:
    name : str
    choice : tuple
    start : int = 1
    contexte: dict = field(default_factory=dict) # sert par exemple à savoir dans quel tournoi on est

ITEMS = {
    "menu principal" : (
        ("Menu Tournois", IFactory("menu tournois")), 
        ("Menu Joueurs", IFactory("menu joueurs")), 
        ("Menu Rapports", IFactory("menu rapports"))),
    "menu joueurs":(
        ("Entrer un nouveau joueur", IFactory("Entrer un nouveau joueur")),
        #("Modifier un joueur", IFactory("Modifier un joueur")), 
        ("Menu rapports", IFactory("menu des rapports (joueurs)")),
        ("Retourner au menu principal", IFactory("menu principal"))),
    "menu tournois":(
       ("Entrer un nouveau tournoi", IFactory("Entrer un nouveau joueur")),
        #("Modifier un tournoi", IFactory("Modifier un joueur")), 
        ("Lancer le tournoi", IFactory("Lancer le tournoi")),
        ("Retourner au menu principal", IFactory("menu principal"))),
    "menu lancer le tournoi":(
        ("Lancer le tournoi", IFactory("Lancer le tournoi")),
        ("Retourner au menu principal", IFactory("menu principal"))),
    "menu lancer le round": (
        ("Lancer le round", IFactory("Lancer le round")),
        ("Retourner au menu principal", IFactory("menu principal"))),
    "menu des rapports (joueurs)":(
        #("Joueurs par ordre alphabétique", ReportFactory("Joueurs par ordre alphabétique")),
        #("Joueurs par classement", ReportFactory("Joueurs par classement")),
        #("Liste des tournois", ReportFactory("Liste des tournois")),
        ("Retourner au menu principal", IFactory("menu principal"))),
    "Entrer un nouveau joueur": (
        (P4Modeles.CHAMPS_DE_PLAYER, PlayerManager.add_new)), # FormFactory
    "Entrer un nouveau tournoi" : (
        ("Nom :", "Lieu :", "Dates (**/**/****):", "Nombre de tours :", "Contrôle du temps :", "Description :", TournamentManager.add_new)),   
}

 
class View(abc.ABC):
    """ méthode appelée par un contrôleur, affiche des choses à l'écran, les renvoie au contrôleur"""
    def __init__(self, name):
        self.name = name

    def show_title(self):
        title = self.name.upper()
        print(f"-----------{title}-----------")

    @abc.abstractmethod
    def show(self):
        self.show_title()

class IView(View):
    """Determine l'affichage des menus et forms"""
    def __init__(self, i: I):
        super().__init__(i.name)
        self.i: I = i

    def show(self):
        super().show()
        if self.name.startswith("menu"):
            for num, choice in enumerate(self.i.choice, start=self.i.start):
                print(f"{num}) {choice[0]}")
            selection = input("Votre choix:")
            return selection
        # le else est la vue questionnaire :    
        else : 
            answers = list()
            for question in self.i.choice[0] :
                print(question)
                current = input()
                if current == "q":
                    break
                else :
                    answers.append(current)
            print(answers)
            return answers
        
       
class Controller(abc.ABC):
    """Gère le stockage et la récupération d'information -> méthodes de recherche et de stockage en db
    Appelle les vues suivantes et déclenche les actions"""
    # Est-ce qu'il faut mettre des @abc.abstractmethod avant chaque?
    def __init__ (self):
        # modèles
        self.player = P4Modeles.Player()
        self.tournament = P4Modeles.Tournament()
        # vues
        self.menuview = IView()
        ##self.formview = FormView()
        ##self.reportview = ReportView()
    def add_new(self) :
        raise NotImplementedError
    def change(self):
        # on affiche la liste de instances qu'on peut changer
        # on demande à l'utilisateur de faire un choix parmi ces choix
        # et ICI on créé le FormManager pour changer l'item => cas n°1 sans Factory Pattern
        # Si on avait eu une usine :
        # on appelle le make() de l'usine AVEC le bon choix, et l'usine retourne le formulaire adapté au bon choix
        # éventuellement quand y aura TinyDB une méthode pour répercuter le changement en DB
        raise NotImplementedError
    def delete(self) :
        raise NotImplementedError
    def get_infos(self): # récupère dans le modèle ou la database les infos nécessaires à l'action
        raise NotImplementedError
    def correct_infos(self): # vérifier et corrige la teneur des données (types, longeur, etc)
        raise NotImplementedError
    def save(self):
        raise NotImplementedError
    def show(self): # affiche
        raise NotImplementedError
    def execute(self):
        raise NotImplementedError


class IManager(Controller):
    def __init__(self, i, view):
        self.i : I = i 
        self.view : IView =  view 
        self.start = self.i.start
        self.contexte = self.i.contexte.copy()
        self.name = self.i.name
        self.choice = self.i.choice
    
    def show(self): # attention : ne pas re-donner les arguments du init)
        return self.view.show() # ici ils sont appelés par self.mot si besoin)

    def read(self):
        """ construit un menu en fonction de la demande de l'utilisateur"""
        while True:
            if self.name.startswith("menu"):
                selection = self.show()
                if selection == "q": 
                    break
                selection = selection.strip()
                if selection.isdigit():
                    selection = int(selection) - self.start # susceptible de lancer une erreur : int("toto") => ??
                    i = self.choice[selection][1].make(contexte=self.contexte) # en fait menu ici peut être form ou menu, ou (?) rapport
                    assert isinstance(i, I)
                    vue = IView(i)
                    controleur = IManager(i, vue)
                    controleur.execute()
                    assert isinstance (controleur, Controller) # MenuManager
                else :
                    print("Choix non valide")
                    #self.read()
            else: # gestion si on a un formulaire
                answers = self.show()
                if answers == "q": 
                    break
                # convertissement des answers en objets python
                # ex: date de naissance => objet Date()
                for i, answer in enumerate(answers):
                    answers[i] = self.choice[0][i][1](answer) # attention : peut raise une exception
                self.choice[1](*answers) # Controleur.methode(answers[0], answers[1], answers[2], ...)
                # récupérer answers et avec add_new en faire un dictionnaire et db.insert

    def execute(self):
        self.read()

class PlayerManager(Controller) :
    def add_new(self, *args):
        P4Modeles.Player(*args)
        # insert dans tinydb

if __name__ == "__main__":

    print("\n----------Essais sur IFactory :----------\n")

    menu_principal = IFactory("menu principal").make()
    vue_menu_principal = IView(menu_principal)
    menu_principal = IManager(menu_principal, vue_menu_principal)
    menu_principal.execute()