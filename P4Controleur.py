import abc
import datetime
from dataclasses import dataclass, asdict, field
from typing import Tuple
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
class Appli(Controller):
    controller : Controller

    def execute(self):
        while True:
            action = self.controller.MenuManager.react_to_answer()
            self.MenuManager.show(action)


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
            print("\ninfo dev : Nouvelle boucle dans MenuManager\n")
            answer = requested_manager.view.show() # ou self.show(requested_manager) plutôt?
            name = requested_manager.choices[answer]

            if name.startswith("Menu"):
                requested_manager = ManagerFactory(name).make_menu()
            elif name.startswith("Rapport:"):
                requested_manager = ManagerFactory(name).make_report()
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

    def adapt_answers(self):
        self.answers[0] = self.answers[0].upper()
        #self.answers[2] = datetime.datetime.strptime(self.answers[2], "%d/%m/%Y") # birthdate
        self.answers[4] = int(self.answers[4])

    def add_new(self): # rempl answers par *args si ça ne marche pas et qu'on doit iterer dans answers
        self.adapt_answers()
        player = P4Modeles.Player(*self.answers) # pareil
        P4Modeles.Player.insert(player)
        print(f"\nAjout d'un joueur à la base de donnée : {player}\n") 

    def execute(self) : # changer pour "save?"
        self.adapt_answers()
        self.add_new()
        
        # def execute? insert dans tinydb

class TournamentManager(Controller) :
    def execute(self):
        return super().execute()

if __name__ == "__main__":

    print("\n\n----------Essais sur les Controleurs de Training ----------")
    print("\n----------Essais sur ManagerFactory :----------\n")

# 1-afficher la vue d'accueil
    welcome = P4Vues.Welcome()
    welcome.show()

# 2-afficher le menu principal
    menu_principal = ManagerFactory("Menu principal").make_menu()
    requested_manager = menu_principal.initial_manager()
    MenuManager.react_to_answer(menu_principal, requested_manager)

# 3-afficher le formulaire pour enregistrer un nouveau joueur (inscrire 8 joueurs au moins ds la db)

#enregistrer_joueur = ManagerFactory("Entrer un nouveau joueur").make_form()
#enregistrer_joueur.react_to_answer()

# 4-afficher le formulaire pour enregistrer un nouveau tournoi

# 5-modifier le tournoi (u.a ajouter 8 joueurs)

# 6-Lancer un tournoi (vérifier qu'infos complètes)
# Tournoi : {{round 1 : [(j1, score, j5, score), (j2, score, j6, score), etc]}