import abc
import datetime
from dataclasses import dataclass, asdict, field
import P4Modeles
import P4Vues


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
        self.menuview = P4Vues.UIView()
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


@dataclass
class MenuManager(Controller):
    name : str
    choices : tuple
    view : P4Vues.View
    start : int = 1

    def initial_manager(self):
        """On commence forcément par un menu."""
        answer = self.view.show()
        name = self.choices[answer]

        requested_manager = ManagerFactory(name).make_menu()
        return requested_manager 
            
    def react_to_answer(self, requested_manager : Controller):
        """Récupère la réponse de l'utilisateur depuis la vue du menu.
        Créé un controleur en fonction de la demande de l'utilisateur."""
        
        name = requested_manager.name

        while True:
            #print("info dev : Nouvelle boucle dans MenuManager\n")
            answer = requested_manager.view.show() # ou self.show(requested_manager) plutôt?
            name = requested_manager.choices[answer]

            if name.startswith("Menu"):
                requested_manager = ManagerFactory(name).make_menu()
            elif name.startswith("Liste"):
                report = ReportManager()
                report.react_to_answer()
                requested_manager = ManagerFactory("Menu Rapports").make_menu()
            elif name.startswith("Selectionner les joueurs"):
                tournament = TournamentManager()
                tournament.select_players()
                requested_manager = ManagerFactory("Menu tournois").make_menu()
            elif name == "Lancer le tournoi":
                tournament = TournamentManager()
                tournament.play_tournament()
                # ajouter le retour à un menu?
            else :
                requested_manager = ManagerFactory(name).make_form()
                answers = requested_manager.view.show()
                if "joueur" in name:
                    PlayerManager(answers).execute()
                    requested_manager = ManagerFactory("Menu joueurs").make_menu()
                if "tournoi" in name:
                    TournamentManager(answers).execute()
                    requested_manager = ManagerFactory("Menu tournois").make_menu()
            
    def show(self, requested_manager : Controller):
        requested_manager.view.show()

    @staticmethod
    def back_to_main_menu():
        back_to_menu = ManagerFactory("Menu principal").make_menu()
        requested_manager = back_to_menu.initial_manager()
        MenuManager.react_to_answer(back_to_menu, requested_manager)


   
        # form ou menu, ou (?) rapport controleur = ManagerFactory.make(le nom de l'IU à générer)


class ReportManager(Controller):
    #Obligatoires pour init : titre du rapport, optionnel : tournoi (si infos tournoi) et vue d'office reportview ou pas?
    name : str
    start : int = 1
    
    tournament : str = None
    pass

    """
    def react_to_answer(self):
        #affiche un rapport en fonction de la demande de l'utilisateur
        infos = P4Modeles.Report()
        view = P4Vues.ReportView(self.name)

        # rapports liés à un tournois :
        if self.tournament != None:
            database = P4Modeles.Database()
            tournoi_dict: dict = database.get_dict_from_db(self.tournament)
            tournament_players = tournoi_dict["players"]
            controleurs = [
                ("Liste des joueurs par ordre alphabétique", infos.sort_by_name(tournament_players)[1]),
                ("Liste des joueurs par classement", infos.sort_by_rating(tournament_players)[1]),
                ("Liste des matchs", tournoi_dict["matches"] )
                ("Liste des tours (déroulé du tournoi)", tournoi_dict["shifts"])
            ]
        # rapport généraux :
        else :
            controleurs = [
                ("Liste des tournois", infos.get_tournaments_list()),
                ("Liste des joueurs par ordre alphabétique", infos.sort_by_name(infos.get_players_list())[1]),
                ("Liste des joueurs par classement", infos.sort_by_rating(infos.get_players_list())[1]),    
            ]

        for controleur in controleurs :
            if self.name == controleur[0]:
                action = view.show(controleur[1])
                return action()
            else :
                print("Pas de contrôleur associé à ce nom")
                return False

        """  

@dataclass
class FormManager(Controller):
    name : str
    questions : tuple
    view : P4Vues.View
    start : int = 1
    
    def react_to_answer(self):
        """lance un formulaire en fonction de la demande de l'utilisateur"""
        answers = self.view.show()
        print(answers)
        if "joueur" in self.name:
            PlayerManager(answers).execute()
            # et revenir au menu joueur
        elif "tournoi" in self.name:
            TournamentManager(answers).execute()
            # et revenir au menu tournoi
        else :
            print(f"Je ne sais pas encore quoi faire avec {self.name} ")


        # convertir les answers en objets python :
        # ex: date de naissance => objet Date()
        #for i, answer in enumerate(answers):
        # try:
        #   answers[i] = self.items[0][i][1](answer) # attention : peut raise une exception                         
        # except :
        #self.items[1](*answers) # Controleur.methode(answers[0], answers[1], answers[2], ...)
        # récupérer answers et avec add_new en faire un dictionnaire et db.insert

@dataclass
class ManagerFactory:
    """
    Réuni les informations et créé les controleurs pour les UI
    donc la base des Menus, Questionnaires et Rapports.

    """
    name : str
    start : int = 1


    def make_menu(self):
        return MenuManager(
            self.name,
            choices = P4Vues.MENUS_CHOICES[self.name], # controleur = ManagerFactory(name < answer)
            view = P4Vues.MenuView(self.name),
            start = self.start
        )

    def make_form(self):
        return FormManager(
            self.name,
            questions = P4Vues.FORMS_FIELDS[self.name], # controleur => doit créer un objet/add_new
            view = P4Vues.FormView(self.name),
            start = self.start
        )


class PlayerManager(Controller) :
    def __init__ (self, answers = None):
        self.answers = answers

    def adapt_answers(self): # Nom, Prénom, Date de naissance, genre, classement
        self.answers[0] = self.answers[0].upper()
        self.answers[1] = self.answers[1].capitalize()
        self.answers[4] = int(self.answers[4])

    def add_new(self):
        self.adapt_answers()
        try:
            player = P4Modeles.Player(*self.answers)
        except ValueError: 
            print("Le joueur doit avoir entre 18 et 99 ans.")
        # ça ça ne marche pas, comment faire que les exceptions dans le modèle soient traduites par un print dans la vue?
        else:
            database = P4Modeles.Database()
            database.insert(dataclass_instance_to_insert = player)
            # _logger.debug("Joueur ajouté à la base ...")
            print(f"\nJoueur ajouté à la base de donnée : {player}\n") 

    def execute(self) : # changer pour "save?"
        self.adapt_answers()
        self.add_new()
        
        # def execute? insert dans tinydb


class TournamentManager(Controller) :
    def __init__ (self, answers=None):
        self.answers = answers

    def adapt_answers(self):   # Nom, Lieu, Date de début, Date de fin, Nombre de tours, Contrôle du temps, Description
        today = datetime.datetime.now()
        vue = P4Vues.ErrorMessages()
        self.answers[0] = self.answers[0].upper()
        self.answers[1] = self.answers[1].capitalize()
        if self.answers[2]<self.answers[3] :
            vue.show(0)
            MenuManager.back_to_main_menu()
        if self.answers[2]< today :
            vue.show(1)
            MenuManager.back_to_main_menu()
        if self.answers[4] == "":
            self.answers[4] = None

    def add_new(self):
        self.adapt_answers()
        tournament = P4Modeles.Tournament(*self.answers)
        database = P4Modeles.Database()
        database.insert(dataclass_instance_to_insert = tournament)
        print(f"\nAjout d'un tournoi à la base de donnée : {tournament}\n") 
   
    def execute(self):
        """Ajoute un joueur dans la db depuis le formulaire"""
        self.adapt_answers()
        self.add_new()

    def select_tournament(self):
        tournamentslist = P4Modeles.Report.get_tournaments_list()
        tournamentslist.append("Menu principal")
        choices = tournamentslist
        vue = P4Vues.MenuView(name ="Selectionner un tournoi :", choices = choices)
        answer = vue.show()
        if answer == len(tournamentslist) -1 :
            MenuManager.back_to_main_menu()
        else :
            tournoi_choisi = choices[answer]
            return tournoi_choisi

    def select_players(self):
        """Montre la liste des tournois pour choisir à quel tournoi on ajoute des joueurs.
        Puis demande de saisir un nom. Ajoute le nom (ça devrait suffir) à la liste players dans ce tournoi.
        Réagit si le nom y est déjà et prévient si la liste contient un nombre pair ou impair de joueurs."""
        db = P4Modeles.Database()
        tournoi_choisi = self.select_tournament()
        tournoi: dict = db.get_dict_from_db(tournoi_choisi)
        tournoi: P4Modeles.Tournament = P4Modeles.Tournament(*tournoi.values())
        print(tournoi)
        while True :
            # on fait choisir parmis les joueurs dans la db :
            infos = P4Modeles.Report()
            players_in_db = infos.get_players_list()
            choices = infos.sort_by_name(players_in_db)[1]
            vue = P4Vues.MenuView(name ="Selectionner le joueur", choices = choices)
            answer = vue.show()
            joueur_choisi = infos.sort_by_name(players_in_db)[0][answer]
            joueur_choisi = joueur_choisi["name"]
            # va chercher le joueur dans la db
            if db.check_if_in_db(joueur_choisi):
                if not tournoi.add_to_playerslist(joueur = joueur_choisi): # équivalent de is False
                    print("Impossible d'ajouter ce joueur (déjà ajouté).")
            answer = input("Selectionner un autre joueur? O/n")
            if answer == "O":
                continue
            else :
                break
        return "Joueurs ajoutés dans la liste de joueurs du tournoi." #liste [nom du tournoi, nom joueur1, nom joueur2, etc...]

    def play_tournament(self):
        db = P4Modeles.Database()
        tournoi_choisi = self.select_tournament()
        tournoi_dict: dict = db.get_dict_from_db(tournoi_choisi)
        instance_de_tournament: P4Modeles.Tournament = P4Modeles.Tournament(*tournoi_dict.values())
        total_scores = instance_de_tournament.initialize_total_scores ()
        tournoi:str = tournoi_dict["name"] # nom du tournoi dont a besoin l'instance de shift et la vue
        vue = P4Vues.TournamentView(name = f"Lancement du {tournoi}")
        vue.show()

        if not len(tournoi_dict["players"])%2 ==0:
            print("Le nombre de joueurs n'est pas pair. Impossible de lancer le tournoi.")
            return MenuManager.back_to_main_menu()

        # on peut rajouter une vue début du tour qui indique "Tour n°{shift_number} et liste des matchs":
        shift = instance_de_tournament.which_shift() # on créé un objet round
        matches = shift.create_pairs_shift1() #liste de tuples

        while True :
            for match in matches:
                print(f"match : {str(match)}")
            shift.update_infos( matches= matches) # utile?
            instance_de_tournament.add_to_matches(matches = matches) # avt intervention c'était ({"matches" = matches})
            start_time = P4Vues.TournamentView.start_shift(shift) # à ajouter à infos
            shift.update_infos(start_time = start_time)  
            end_time = P4Vues.TournamentView.end_shift(shift) # ajouter à round_infos (et passer à add_to_shift_infos)
            shift.update_infos(end_time = end_time)
            scores  = P4Vues.TournamentView.get_scores(shift, matches) #[0] = liste de tuple, [1] = dict
            total_scores.update(scores[1])
            print(total_scores)
            shift.update_infos(scores = scores[1]) # attention : changé de scores[0] car ne renvoyait pas le tupple donc dico
            # à ce stade le dict des infos du tour est complet, il faut le passer au tournoi dans la db.
            shift_infos = shift.infos
            instance_de_tournament.add_to_shifts(shift_infos= shift_infos)

            shift = instance_de_tournament.which_shift(shift.shift_number)

            if shift == False: # ça veut dire qu'on a fini le dernier tour.
                print("\nFélicitations à tous les participants. Le tournoi est terminé.\n")
                break
            else :
                matches = shift.create_pairs2(total_scores=total_scores)
                continue

        return MenuManager.back_to_main_menu() 


        # calculer les paires du 1er round,
        # demander si lancer le 1er round O/n
        # O -> enregistrer l'heure de début du round
        # finir le tournoi O/n -> enregistrer l'heure de fin du round et demander les scores
        # les scores vont dans Tournoi : {{round 1 : [(j1, score, j5, score), (j2, score, j6, score), etc]}
        # calculer les paires du 2ème round
        # etc. tant que nbr de rounds <= nbr annoncé
        # Le tournoi est terminé


if __name__ == "__main__":

    print("\n\n----------Essais sur les Controleurs de Training ----------")
    print("\n----------Essais sur ManagerFactory :----------\n")

    # 1-afficher la vue d'accueil
    welcome = P4Vues.Welcome()
    welcome.show()

    # 2-afficher le menu principal
    """
    menu_principal = ManagerFactory("Menu principal").make_menu()
    requested_manager = menu_principal.initial_manager()
    MenuManager.react_to_answer(menu_principal, requested_manager)
    """
    # 3-afficher le formulaire pour enregistrer un nouveau joueur (inscrire 8 joueurs au moins ds la db)

    #enregistrer_joueur = ManagerFactory("Entrer un nouveau joueur").make_form()
    #enregistrer_joueur.react_to_answer()

    # 4-afficher le formulaire pour enregistrer un nouveau tournoi

    # 5-ajouter 8 joueurs)

    # 6-Lancer un tournoi (vérifier qu'infos complètes)
    # Tournoi : {{round 1 : [(j1, score, j5, score), (j2, score, j6, score), etc]}

    db = P4Modeles.Database()

    #test_update = db.change("name", "TOURNOI DES ROIS", "number_of_rounds","4")
    #test_update = db.change("name", "TOURNOI DES ROIS", "time_control","bullet")

    # Find all documents (dict objects) that contain 'a' key
    # and set value of key 'a' to 2
    #db.update({'a': 2}, Query().a.exists())

    tournoi = P4Modeles.Tournament(name = "Tournoi Test", location = "Honolulu", timecontrol = "blitz")
    print(tournoi)

    tournoi = TournamentManager(tournoi).play_tournament()








