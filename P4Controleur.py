import abc
import datetime
from dataclasses import dataclass, asdict, field
from typing import Tuple
import P4Modeles
import P4Vues
import Menus


"""Nous avons ici commandes/managers"""

class Controller(abc.ABC):
    """Gère le stockage et la récupération d'information -> méthodes de recherche et de stockage en db
    Appelle les vues suivantes et déclenche les actions"""
    # Est-ce qu'il faut mettre des @abc.abstractmethod avant chaque?
    def __init__ (self):
        # modèles
        self.player = P4Modeles.Player()
        self.tournament = P4Modeles.Tournament()
        # vues
        self.menuview = P4Vues.MenuView()
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

class PrintController(Controller):
    
    def __init__(self, to_print):
        self.to_print = to_print

    def execute_action(self):
        print(self.to_print)


"""   
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
"""

class MenuManager(Controller):
    def __init__(self, menu, menu_view):
        self.menu : Menus.Menu = menu 
        self.menu_view : P4Vues.MenuView =  menu_view 
        self.start = self.menu.start
        self.contexte = self.menu.contexte.copy() # pb : not callable 
        self.name = self.menu.menu_name
        self.menu_choice = self.menu.menu_choice
    
    def show(self): # attention : ne pas re-donner les arguments du init)
        return self.menu_view.show() # ici ils sont appelés par self.mot si besoin)

    def prompt_for_selection(self):
        return self.menu_view.prompt_for_selection()

    def read(self):
        """ construit un menu en fonction de la demande de l'utilisateur"""
        while True:
            self.show()
            selection = self.prompt_for_selection()
            selection = selection.strip()
            if selection == "q": # une solution pour retourner en arrière
                break
            elif selection.isdigit():
                selection = int(selection) - self.start # susceptible de lancer une erreur : int("toto") => ??
                menu = self.menu_choice[selection][1].make(contexte=self.contexte) # en fait menu ici peut être form ou menu, ou (?) rapport
                assert isinstance(menu, Menus.Menu) or isinstance(menu, Menus.Form)
                vue = P4Vues.MenuView(menu)
                controleur = MenuManager(menu, vue)
                controleur.execute()
                assert isinstance (controleur, Controller)#MenuManager
            else :
                print("Choix non valide")
                #self.read()

    def execute(self):
        self.read()


class FormManager(Controller) :
    def __init__ (self, form, form_view, contexte):
        self.form = Menus.Form()
        self.form_view = P4Vues.FormView()
        self.contexte = form.contexte.copy() # ou contexte: dict = field(default_factory=dict) et à retirer de class Form
    
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


    pass


class PlayerManager(Controller) :
    def __init__ (self, answers):
        self.answers = answers

    def adapt_answers(self, answers):
        answers[2] = datetime.datetime.strptime(answers[2], "%d/%m/%Y") # birthdate
        answers[4] = int(answers[4])
        print(*answers)

    def add_new(self, answers): # rempl answers par *args si ça ne marche pas et qu'on doit iterer dans answers
        self.adapt_answers(answers)
        player = P4Modeles.Player(*answers) # pareil
        print(player)
        return player

    def execute(self, player : P4Modeles.Player) : # changer pour "save?"
        P4Modeles.Player.insert(player)# def execute? insert dans tinydb


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
        """clôture le tournoi -> archivé?"""
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
        """enregistre l'heure de début du round"""    
        pass

    def finish_round(self):
        """enregistre l'heure de fin du round"""
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



if __name__ == "__main__":

    print("\n\n----------Essais sur les Controleurs de Training ----------")
    print("\n----------Essais sur MenuFactory :----------\n")

    welcome = P4Vues.Welcome()
    welcome.show()

    menu_principal = Menus.MenuFactory("menu principal").make()
    #typeof = type(menu_principal)
    #print(typeof)
    vue_menu_principal = P4Vues.MenuView(menu_principal)
    #vue_menu_principal.show()
    menu_principal = MenuManager(menu_principal, vue_menu_principal)
    menu_principal.execute()

    menu_joueur= Menus.MenuFactory("menu joueurs").make()

