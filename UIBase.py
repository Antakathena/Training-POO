import abc
#import datetime
from dataclasses import dataclass, field


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

  
    def execute_action(self):
        while True:
            choice = self.menu_view.show(self.choices)
            if choice == "q": # une solution pour retourner en arrière
                break
            try:
                choice = self.choices[int(choice) - self.start][1]
            except (TypeError, ValueError, IndexError):
                continue # retour au début de la boucle, q. pr break
            else:
                if callable(choice):
                    choice()
                # TournamentManager.add_new
                else:
                    choice.execute_action()
                # TournamentManager.add_new.execute_action()

class PrintController(Controller):
    
    def __init__(self, to_print):
        self.to_print = to_print

    def execute_action(self):
        print(self.to_print)


class UIManager(Controller):
    def __init__(self, ui, view):
        self.ui : UIBase.UI = ui 
        self.view : P4Vues.UIView =  view 
        self.start = self.ui.start
        self.name = self.ui.name
        self.items = self.ui.items
    
    def show(self): # attention : ne pas re-donner les arguments du init)
        return self.view.show() # ici ils sont appelés par self.mot si besoin)

    def read(self):
        """construit un menu en fonction de la demande de l'utilisateur"""
        while True:
            if self.name.startswith("menu"):
                selection = self.show()
                if selection == "q": 
                    break
                selection = selection.strip()
                if selection.isdigit():
                    selection = int(selection) - self.start # susceptible de lancer une erreur : int("toto") => ??
                    i = self.items[selection][1].make() # en fait menu ici peut être form ou menu, ou (?) rapport
                    assert isinstance(i, UIBase.UI)
                    vue = P4Vues.UIView(i)
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





class TournamentManager(Controller) :
    def __init__(self):
        self.players = []
        self.rounds = []
        self.matchs = []
    
    def choose_players(self):
        """ 
        permet de séléctionner les joueurs dans la base de donnée
        vérifier que au moins 8 joueurs, nombre pair, pas deux fois le même
        """
        while len(self.players) < 8:
            name = self.view.prompt_for_players()
            if not name:
                return
            player = P4Modeles.Player(name)
            self.players.append(player)

    def start_tournament(self):
        """
        vérifier que toutes les infos sont là (u.a afficher la fiche du tournoi selectionné) et que self.player est viable;
        lancer le tournoi -> lancer round 1
        """
        return "Entrée dans le start_tournament"
        pass
    
    def next_round (self):
        """
        lance la création d'un nouvel objet round dans le tournoi en indiquant de son numéro d'ordre
        """
        pass

    def end_tournament(self):
        #clôture le tournoi -> archivé?
        pass


class RoundManager(Controller):
    def __init__(self, number, players):
        self.number = number
        self.players = players
        self.matchs = []

    def create_pairs_1(self):
        """calcule les paires de joueurs pour les matchs du round 1"""
        pass
    
    def create_pairs_2(self):
        """calcule les paires de joueurs pour les matchs des autres rounds"""
        pass

    def start_round(self):
        #enregistre l'heure de début du round    
        pass

    def finish_round(self):
        #enregistre l'heure de fin du round
        pass

    def record_scores(self):
        """
        lance la vue pour entrer les scores du round (la liste des noms et la règle "0","1" ou "0,5"),
        caste les input en int et vérifie que le total est égal à la moitié du nombre de joueurs
        et les enregistre :

        Matchs[] devrait passer par exemple de 
        Round1.matchs = [(p1,p5), (p2,p6), (p3,p7), (p4,p8)]
        à
        Round1.matchs = [{p1:0,p5:1} , {p2:1,p6:0} ,{p3:0,5,p7:0,5} , {p4:0,p8:1} ]
        joueur_x, score_joueur_x, joueur_y, score_joueur_y
        """
        pass


class ReportManager(Controller) :
    pass


ITEMS = {
    "Menu principal" : (
        ("Menu Tournois", ManagerFactory("menu tournois")), 
        ("Menu Joueurs", ManagerFactory("menu joueurs")), 
        ("Menu Rapports", ManagerFactory("menu rapports"))),
    "Menu joueurs":(
        ("Entrer un nouveau joueur", ManagerFactory("Entrer un nouveau joueur")),
        #("Modifier un joueur", IFactory("Modifier un joueur")), 
        ("Menu rapports", ManagerFactory("menu des rapports (joueurs)")),
        ("Retourner au menu principal", ManagerFactory("menu principal"))),
    "Menu tournois":(
       ("Entrer un nouveau tournoi", ManagerFactory("Entrer un nouveau tournoi")),
        #("Modifier un tournoi", IFactory("Modifier un joueur")), 
        ("Lancer le tournoi", ManagerFactory("Lancer le tournoi")),
        ("Retourner au menu principal", ManagerFactory("menu principal"))),
    "Menu lancer le tournoi":(
        ("Lancer le tournoi", ManagerFactory("Lancer le tournoi")),
        ("Retourner au menu principal", ManagerFactory("menu principal"))),
    "Menu lancer le round": (
        ("Lancer le round", ManagerFactory("Lancer le round")),
        ("Retourner au menu principal", ManagerFactory("menu principal"))),
    "Menu des rapports (joueurs)":(
        #("Joueurs par ordre alphabétique", ReportFactory("Joueurs par ordre alphabétique")),
        #("Joueurs par classement", ReportFactory("Joueurs par classement")),
        #("Liste des tournois", ReportFactory("Liste des tournois")),
        ("Retourner au menu principal", ManagerFactory("menu principal"))),
    "Entrer un nouveau joueur": (
        (P4Vues.FORMS_FIELDS["Entrer un nouveau joueur"], PlayerManager)), # FormFactory
    "Entrer un nouveau tournoi" : (
        (P4Vues.FORMS_FIELDS["Entrer un nouveau tournoi"], TournamentManager)),   
}

"""