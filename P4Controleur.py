import abc
import datetime
from dataclasses import dataclass, asdict

from P4Modeles import Player,Tournament 
from P4Vues import FormView, MenuView, ReportView

# listes de choix de chaque menu :
mainmenu_choices = ["Menu Tournois", "Menu Joueurs","Menu Rapports"]
playermenu_choices = ["Entrer un nouveau joueur","Modifier un joueur","Menu rapports","Retourner au menu principal"]
tournamentmenu_choices = ["Entrer un nouveau tournoi","Modifier un tournoi","Lancer le tournoi","Retourner au menu principal"]
launch_newtournament = ["Lancer le tournoi","Retourner au menu principal"]
reportmenu1_choices = ["Joueurs par ordre alphabétique", "Joueurs par classement", "Liste des tournois", "Retourner au menu principal"]
reportmenu2_choices = ["Joueurs du tournoi par ordre alphabétique", "Joueurs du tournoi par classement", "liste des tours", "liste des matchs"]


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
        self.formview = FormView()
        self.reportview = ReportView()

    def run(self):
        pass
    def add_new(self) :
        raise NotImplementedError
    def change(self):
        raise NotImplementedError
    def delete(self) :
        raise NotImplementedError
    def get_infos(self): # récupère dans le modèle ou la database les infos nécessaires à l'action
        raise NotImplementedError
    def correct_infos(self): # vérifier et corrige la teneur des données (types, longeur, etc)
        raise NotImplementedError
    def save(self):
        raise NotImplementedError
    def draw(self): # affiche
        raise NotImplementedError
    def execute_action(self):
        raise NotImplementedError


class PrintController(Controller):
    def __init__(self, to_print):
        self.to_print = to_print

    def execute_action(self):
        print(self.to_print)


class MenuManager(Controller) :
    """
    Avec cette classe nous voulons créer et gérer les objets suivants :
    main_menu, player_menu, tournament_menu, launch_newtournament, report_menu1, report_menu2

    NB : objet_menu = MenuManager(titre, [liste de(couples choix du menu et action associée)])

    rapports1 fait choisir entre les listes de tous les joueurs (hors tournoi particulier),
    rapports2 fait choisir les infos qu'on veut sur un tournoi à partir de la liste des tournois.
    """

    def __init__(self, name, choices, menu_view=MenuView(1), start=1):
        self.name = name
        self.choices = choices or []
        self.menu_view = menu_view
        self.menu_view.bind(self)
        self.start = start

    def execute_action(self):
        while True:
            choice = self.menu_view.draw()
            if choice == "q": # une solution pour retourner en arrière
                break
            try:
                choice = self.choices[int(choice) - self.start]
            except (TypeError, ValueError, IndexError):
                continue # retour au début de la boucle, q. pr break
            choice.execute_action()


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

    vue_menu = MenuView()
    
    print("\n\n----------Essais sur les modèles de training ----------\n")
    print("\n----------Essais sur Player :----------\n")

    print(Player)

    player0 = Player()
    print(player0)

    player1 = Player("ATOME", "Adam", datetime.datetime.strptime("01/02/1972", "%d/%m/%Y"), "homme", 2001 )
    print(player1)

    print(player1.__repr__)

    typeof = type(player1.birthdate)
    print(typeof)

    print("\n\n----------Test de la fonction dataclasses.asdict :----------\n") 

    print(asdict(player1))

    print("\n\n----------Essais sur Tournament :----------\n")

    print(Tournament)

    tournament0 = Tournament()
    print("\n----------Voici la représentation du tournoi test, listes à compléter:----------\n")
    print(tournament0.__repr__)
    print("\n----------Et voici son str :----------\n")
    print(tournament0)


    main_menu = MenuManager(
    "Menu Principal",
    [("Menu Tournois", MenuView.draw(tournamentmenu_choices)),
    ("Menu Joueurs", MenuView.draw(playermenu_choices)),
    ("Menu Rapports", MenuView.draw(reportmenu1_choices))])

    tournament_menu = MenuManager(
    "Menu Tournoi",
    [("Entrer un nouveau tournoi", TournamentManager.add_new()),
    ("Modifier un tournoi", TournamentManager.change()),
    ("Lancer le tournoi", TournamentManager.start_tournament()),
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])

    launch_newtournament = MenuManager(
    "lancer nouveau tournoi",
    [("Lancer le tournoi", TournamentManager.start_tournament()),
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])

    player_menu = MenuManager(
    "Menu Joueurs",
    [("Entrer un nouveau joueur", PlayerManager.add_new()),
    ("Modifier un joueur", PlayerManager.change()),
    ("Menu rapports", MenuView.draw(reportmenu1_choices))
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])

    report_menu1 = MenuManager(
    "Menu Rapports, Accueil",
    [("Joueurs par ordre alphabétique", ReportView.draw(players, alpha)),
    ("Joueurs par classement", ReportView.draw(players, ranking)),
    ("Liste des tournois", MenuView.draw(reportmenu2_choices)),
    ("Retourner au menu principal", MenuView.draw(mainmenu_choices))])