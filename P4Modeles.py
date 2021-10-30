
import abc
from dataclasses import dataclass, field, asdict
import datetime
#from pprint import pprint
from tinydb import TinyDB, Query

db = TinyDB('db.json')




@dataclass
class Model(abc.ABC):
    """Classe abstraite : définit les méthodes communes à tous les modèles"""
    # @abc.abstractmethod
    # commenté car on verra plus tard

@dataclass
class Player(Model):
    """Dataclass définit automatiquement les init, repr etc."""    
    name : str = field(default = "John")
    firstname : str = field(default = "Doe")
    birthdate : datetime = field(default =datetime.datetime.strptime("05/06/1980", "%d/%m/%Y"))
    gender : str = field(default = "h") # à convertir en Mr ou Mme dans le __str__
    rating : int = field (default = 0)


    def __str__(self): # comment transformer h en monsieur et f en madame dans le str?
        if self.gender == "h":
            titre = "Monsieur"
            birthdate_indication = "né le"
            ranking_indication = "classé"
        else :
            titre = "Madame"
            birthdate_indication = "née le"
            ranking_indication = "classée"
        return f"{titre} {self.firstname} {self.name}, {birthdate_indication} {self.birthdate.strftime('%d/%m/%Y')},{ranking_indication} {self.rating}"
  
    def player_serialization(self) -> dict : # en fait méthode save (?)
        # dataclasses.asdict(instance_de_player) devrait pour passer le joueur à la db sous forme de dict
        pass


@dataclass
class Tournament(Model):
    name : str = "Tournoi Test"
    location : str = "Quelque part"
    dates : datetime = datetime.datetime.strptime("05/06/2025", "%d/%m/%Y")
    # dates : à changer en date de début à date de fin donc tuple de dates?
    players : list = field(default_factory=list)
    number_of_rounds : int= field(default=4)
    rounds : list = field(default_factory=list)
    # rounds = dict ou liste d'une liste de tuples des matchs du round ex : round1 [(joueur1, joueur5), (joueur2, joueur6), etc] 
    timecontrol : str = "bullet/blitz/coup rapide"
    description : str = field(default= " ")

    def __str__(self):
        return f"{self.name},{self.location},{self.dates.strftime('%d/%m/%Y')},\
{self.players},{self.number_of_rounds},{self.rounds},{self.timecontrol},{self.description}"

        # Pour amélioration, utiliser propriété de dataclasses :
        # essayer : for info in dataclasses.fields(Tournament): return str(info)
        # ou quelque chose comme ça
        
    

@dataclass
class Round(Model):
    """
    définit la classe Round, qui référence :
    son tournoi
    son numéro d'ordre
    le début du tour (date et heure)
    la fin du tour (date et heure)
    la liste de ses matchs
    """
    round_number : int # ou alors on fait un enumerate quelque part
    matchs_list : list # liste de tuples
    start_datetime : datetime
    end_datetime : datetime

    def create_list_by_rating(self): # à revoir pour dataclass _ cf order = True ou .fields()
        """tri les joueurs du tournoi par classement/rang"""
        players_by_rating = sorted(self._players, key=lambda k: k["rang"], reverse=True)
        return players_by_rating

    def create_pairs_round1(self): 
        """Créé des matchs basés sur le classement des joueurs pour le round 1"""
        # une fonction "split" quand le reste marchera? sert aussi plus tard

        if len(self.players) % 2 != 0:
            raise Exception("Impossible de générer des appairages avec un nombre impair de joueurs")

        half = len(self.players) // 2
        first_half = self.players_by_rating[:half]
        second_half = self.players_by_rating[half:]

        # création des matchs
        matchs_round1 = zip(first_half, second_half)

        # liste des matchs
        pairings = []
        for first_half, second_half in zip(first_half, second_half):
            pairings.append(first_half, second_half)
        return pairings

    def create_pairs2(self, tournament_players):
        pass


class Match: # à garder ou pas?
    """
    définit la classe Match, qui permet:
    d'enregistrer les parties jouées et les scores
    """
    def __init__(self, joueur_x, score_joueur_x, joueur_y, score_joueur_y):
        self.joueur_x = joueur_x
        self.score_joueur_x = score_joueur_x
        self.joueur_y = joueur_y
        self.score_joueur_y = score_joueur_y

    def record_score(self, score_x, score_y):
        """ permet de saisir les scores des 2 joueurs du match à la fin de la partie et les ajoute aux listes"""
        pass


if __name__ == "__main__":

    print("\n\n----------Essais sur les modèles de training ----------")
    print("\n----------Essais sur Player :----------\n")

    print(Player)

    player0 = Player()
    print(player0)

    player1 = Player("ATOME", "Adam", datetime.datetime.strptime("01/02/1972", "%d/%m/%Y"), "h", 2001 )
    print(player1)

    print(f"\n__repr__ de player1 : {repr(player1)}\n")

    typeof = type(player1.birthdate)
    print(f"Type de player1.birthdate : {typeof}")

    print("\n\n----------Test de la fonction dataclasses.asdict :----------\n") 

    print(asdict(player1))

    print("\n\n----------Essais sur Tournament :----------\n")

    print(Tournament)

    tournament0 = Tournament()
    print("\n----------Voici la représentation du tournoi test, listes à compléter:----------\n")
    print(f"\n__repr__ de tournament0 : {repr(tournament0)}\n")
    print("\n----------Et voici son str :----------\n")
    print(tournament0)

