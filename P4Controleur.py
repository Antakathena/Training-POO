import abc
import datetime
from dataclasses import dataclass, asdict, field
from typing import Tuple
import P4Modeles
import P4Vues

from tinydb import TinyDB, Query



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
            print("info dev : Nouvelle boucle dans MenuManager\n")
            answer = requested_manager.view.show() # ou self.show(requested_manager) plutôt?
            name = requested_manager.choices[answer]

            if name.startswith("Menu" or "Liste"):
                requested_manager = ManagerFactory(name).make_menu()
            elif name.startswith("Rapport:"):
                requested_manager = ManagerFactory(name).make_report()
            elif name.startswith("Selectionner"):
                # on choisit le tournoi
                tournament = TournamentManager()
                tournament.select_players() #blop  
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

   
        # form ou menu, ou (?) rapport controleur = ManagerFactory.make(le nom de l'IU à générer)

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

    def make_report(self):
        #return ReportManager(args, contenu)
        return NotImplementedError
        
class PlayerManager(Controller) :
    def __init__ (self, answers):
        self.answers = answers

    def adapt_answers(self): # Nom, Prénom, Date de naissance, genre, classement
        self.answers[0] = self.answers[0].upper()
        self.answers[1] = self.answers[1].capitalize()
        self.answers[4] = int(self.answers[4])

    def add_new(self):
        self.adapt_answers()
        player = P4Modeles.Player(*self.answers)
        P4Modeles.Player.insert(player)
        print(f"\nJoueur ajouté à la base de donnée : {player}\n") 

    def execute(self) : # changer pour "save?"
        self.adapt_answers()
        self.add_new()
        
        # def execute? insert dans tinydb

class TournamentManager(Controller) :
    def __init__ (self, answers):
        self.answers = answers

    def adapt_answers(self):   # Nom, Lieu, Date de début, Date de fin, Nombre de tours, Contrôle du temps, Description
        self.answers[0] = self.answers[0].upper()
        self.answers[1] = self.answers[1].capitalize()

    def add_new(self):
        self.adapt_answers()
        tournament = P4Modeles.Tournament(*self.answers) 
        P4Modeles.Tournament.insert(tournament)
        print(f"\nAjout d'un tournoi à la base de donnée : {tournament}\n") 
   
    def execute(self):
        """Ajoute un joueur dans la db depuis le formulaire"""
        self.adapt_answers()
        self.add_new()

    def select_players(self):
        """Montre la liste des tournois pour choisir à quel tournoi on ajoute des joueurs.
        Puis demande de saisir un nom. Ajoute le nom (ça devrait suffir) à la liste players dans ce tournoi.
        Réagit si le nom y est déjà et prévient si la liste contient un nombre pair ou impair de joueurs."""
        db = P4Modeles.Database()
        #afficher tous les tournois contenus dans la db. A changer pour le rapport des tournois qd prêt
        tournois = P4Modeles.Database.get_tournaments_list()
        P4Vues.TournamentListView(tournois).show()
        # fait choisir un tournoi
        tournoi_choisi = P4Vues.TournamentListView(tournois).choose_tournament()
        tournoi_choisi = db.get_in_db(tournoi_choisi["name"])
        print(tournoi_choisi)
        # fait entre un nom de joueur
        Entrer_nom = P4Vues.PlayerSelectionView()
        joueur_choisi = Entrer_nom.show()
        # va chercher le joueur dans la db
        if db.check_if_in_db(joueur_choisi) == True:
            P4Modeles.Tournament.add_to_playerslist(joueur_choisi)


        


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

    # 5-modifier le tournoi (u.a ajouter 8 joueurs)

    # 6-Lancer un tournoi (vérifier qu'infos complètes)
    # Tournoi : {{round 1 : [(j1, score, j5, score), (j2, score, j6, score), etc]}



    db = P4Modeles.Database()

    #test_update = db.change("name", "TOURNOI DES ROIS", "number_of_rounds","4")
    #test_update = db.change("name", "TOURNOI DES ROIS", "time_control","bullet")

    
    test_remove = db.delete("firstname","Bruce")
    objet_chercher = "WAYNE"
    test_search = db.get_in_db(objet_chercher)
    resultat= test_search
    print(resultat)

    # Find all documents (dict objects) that contain 'a' key
    # and set value of key 'a' to 2
    #db.update({'a': 2}, Query().a.exists())



