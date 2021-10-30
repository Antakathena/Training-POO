import abc
import datetime
from dataclasses import dataclass, asdict, field
from typing import Tuple

from P4Modeles import Player,Tournament
from P4Vues import MenuView 


# listes de choix de chaque menu (faire fichier exterieur?) :
MENU_CHOICES = {
    "menu principal" : ("Menu Tournois", "Menu Joueurs","Menu Rapports"),
    "menu joueurs":("Entrer un nouveau joueur","Modifier un joueur","Menu rapports","Retourner au menu principal"),
    "menu tournois":("Entrer un nouveau tournoi","Modifier un tournoi","Lancer le tournoi","Retourner au menu principal"),
    "menu lancer le tournoi":("Lancer le tournoi","Retourner au menu principal"),
    "menu lancer le round":("Lancer le round","Retourner au menu principal"),
    "menu des rapports (joueurs)":("Joueurs par ordre alphabétique", "Joueurs par classement", "Liste des tournois", "Retourner au menu principal"),
    "menu des rapports (tournois)":("Joueurs du tournoi par ordre alphabétique", "Joueurs du tournoi par classement", "liste des tours", "liste des matchs")
    }


@dataclass
class Menu(abc.ABC):
    menu_name : str
    menu_choice : tuple = field(default_factory=tuple)
    menu_view : MenuView = field(default=None)
    start : int = 1

    def __post_init__(self, menu_name):
        menu_choice = MENU_CHOICES.get(menu_name)

@dataclass
class MenuFactory(Menu):
    """
    NB : objet_menu = MenuFactory(nom du menu, [
    liste de couples (("Titre option", Controleur/action)])

    """
    menu_name : str
    menu_choice : tuple = field(default_factory=tuple)
    menu_view : MenuView = None
    start : int = 1

    def __post_init__(self, menu_name):
        menu_choice = MENU_CHOICES.get(menu_name)


    def __call__(self, **kwargs) -> Menu:
        return Menu(self.menu_name, self.menu_choice, self.menu_view, self.start, **kwargs)

    #def make(self, **kwargs) -> Menu:
    #    return Menu(self.name, self.choices, self.menu_view, self.start, **kwargs)

MENU_FACTORIES = {
    "menu principal": Menu(menu_name="menu principal"),
    "menu joueurs": Menu("menu joueurs"),
    "menu tournois": Menu("menu tournois"),
    "menu lancer le tournoi": Menu("menu lancer le tournoi"),
    "menu lancer le round": Menu("menu lancer le round"),
    "menu des rapports (joueurs)": Menu("menu des rapports (joueurs)"),
    "menu des rapports (tournois)": Menu("menu des rapports (tournois)")
    }
# MainMenu(), PlayerMenu(), TournamentMenu(), StartNewTournament(), StartNewRound(), ReportMenu1(), ReportMenu2()


class Controller(abc.ABC):
    """Gère le stockage et la récupération d'information -> méthodes de recherche et de stockage en db
    Appelle les vues suivantes et déclenche les actions"""
    # Est-ce qu'il faut mettre des @abc.abstractmethod avant chaque?
    def __init__ (self):
        # modèles
        self.player = Player()
        self.tournament = Tournament()
        # vues
        self.menuview = MenuView()
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
    def execute_action(self):
        raise NotImplementedError


class PrintController(Controller):
    
    def __init__(self, to_print):
        self.to_print = to_print

    def execute_action(self):
        print(self.to_print)



class MenuManager(Controller):

    def read_menu(self):
        """ construit un menu en fonction de la demande de l'utilisateur"""
        while True :
            selection = input("Votre choix:")
            if selection == "q": # une solution pour retourner en arrière
                break
            if selection in MENU_FACTORIES:
                return MENU_FACTORIES(selection) # ajouter enumerate pour numéro au lieu de nom
    
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

class FormManager(Controller) :
    """
    with items (inputs), nous avons les formulaires à remplir pour:
    nouveau joueur,
    nouveau tournoi,
    demande de rapport
    Il faut auss pouvoir modifier les existants
    """
    pass


class PlayerManager(Controller) :
    pass


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
            player = Player(name)
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

    main_menu = MenuFactory("menu principal")
    print(main_menu)

    

    """
    print("TournamentManager.start_tournament(TournamentManager())", TournamentManager.start_tournament(TournamentManager()))

    main_menu = Menu(
    "Menu Principal",
    [("Menu Tournois", MenuView.draw(tournamentmenu_choices)),# vue pas = controleur
    ("Menu Joueurs", MenuView.draw(playermenu_choices)),
    ("Menu Rapports", MenuView.draw(reportmenu1_choices))])

    # main_menu.execute_action()

    tournament_menu = MenuManager(
    "Menu Tournoi",
    [("Entrer un nouveau tournoi", TournamentManager().add_new),
    ("Modifier un tournoi", TournamentManager().change),
    ("Lancer le tournoi", TournamentManager().start_tournament),
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])

    launch_newtournament = MenuManager(
    "lancer nouveau tournoi",
    [("Lancer le tournoi", TournamentManager.start_tournament),
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])

    player_menu = MenuManager(
    "Menu Joueurs",
    [("Entrer un nouveau joueur", PlayerManager.add_new),
    ("Modifier un joueur", PlayerManager.change),
    ("Menu rapports", MenuView.draw(reportmenu1_choices))
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])

    report_menu1 = MenuManager(
    "Menu Rapports, Accueil",
    [("Joueurs par ordre alphabétique", ReportView.draw(players, alpha)),
    ("Joueurs par classement", ReportView.draw(players, ranking)),
    ("Liste des tournois", MenuView.draw(reportmenu2_choices)),
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])
    """