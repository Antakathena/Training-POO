
import abc
from dataclasses import dataclass
import datetime


class Model(abc.ABC):
    """Classe abstraite : définit les méthodes communes à tous les modèles"""
    # @abc.abstractmethod
    # commenté car on verra plus tard
    def add_item(self):
        pass
    def save(self):
        raise NotImplementedError
    def delete(self):
        pass

@dataclass
class Player(Model):
    """Dataclass définit automatiquement les init, repr etc."""    
    name : str
    firstname : str
    birthdate : datetime
    gender : str
    rating : int

@dataclass
class Tournament(Model):
    name : str
    location : str
    dates : datetime.date # à changer en date de début à date de fin
    players : list
    number_of_rounds : int # par défault 4
    rounds : list # dict d'une liste de tuples des matchs du round ex : round1 [(joueur1, joueur5), (joueur2, joueur6), etc] 
    timecontrol : str # ou instance de classe timecontrol?
    description : str # créer un champ de texte, facultatif donc default = " "

@dataclass
class Round(Model):
    """
    définit la classe Round, qui permet:
    d'enregistrer automatiquement le début du tour (date et heure)
    d'enregistrer automatiquement la fin du tour (date et heure)
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