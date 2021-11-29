
import abc
from dataclasses import dataclass, field, asdict
import datetime
import re
import itertools
from enum import Enum, auto
from pprint import pprint
from tinydb import TinyDB, Query, operations

db = TinyDB('db.json', ensure_ascii=False)

class Serialization:

    @staticmethod
    def date_serialization(datetime_obj) -> str:
        """Adapte à la db en changeant un datetime en str"""
        return datetime_obj.strftime("%d/%m/%Y")

    @staticmethod
    def serialize_all_dates(dict_obj):
        """
        Trouve les objets datetime au format datetime.datetime(2000, 1, 1, 0, 0) dans un dict.
        Change tous les datetime présents dans les valeurs d'un dict en string.(Juste la date)
        """
        dates ={}
        for k, v in dict_obj.items() :
            if type(v) == datetime.datetime:
                dates[k] = v.strftime("%d/%m/%Y")
        for k,v in dates.items():
            dict_obj[k] = v
        return dict_obj

    @staticmethod
    def serialize_all_times(dict_obj):
        """
        Trouve les objets datetime au format datetime.datetime(2000, 1, 1, 0, 0) dans un dict.
        Change tous les datetime présents dans les valeurs d'un dict en string.(Avec l'heure)
        """
        dates ={}
        for k, v in dict_obj.items() :
            if type(v) == datetime.datetime:
                dates[k] = v.strftime("%d/%m/%Y, %H:%M:%S")
        for k,v in dates.items():
            dict_obj[k] = v
        return dict_obj
    
    @staticmethod
    def date_deserialization(date_string) -> datetime:
        """Adapte à l'usage un objet date str venant de la db"""
        return datetime.datetime.strptime(date_string, "%d/%m/%Y")

    @staticmethod
    def find_datestring(text) :
        """Trouve la première date au format **/**/**** dans l'élément string
        et la change en datetime."""
        match = re.search(r'\d{2}/\d{2}/\d{4}', text)
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
        print(date)
        return date

    @staticmethod
    def findall_datestring(elt) -> list:
        """Trouve juste les dates au format **/**/**** dans l'élément."""
        match = re.findall(r'\d{2}/\d{2}/\d{4}', str(elt))
        dates = []
        for date in match:
            dates.append(date)
        return dates

    def deserialize_all_dates(self, dict_obj = None):
        """Trouve les dates au format **/**/**** dans l'élément.
        Les change en datetime. """
        match = re.findall(r'\d{2}/\d{2}/\d{4}', str(dict_obj)) 
        dates ={}
        for date in match:
            for k, v in dict_obj.items():
                if v == date:
                    dates[k] = datetime.datetime.strptime(v, "%d/%m/%Y")
        for k,v in dates.items():
            dict_obj[k] = v
        return dict_obj

    def calculate_age(valeur):
        today = datetime.datetime.now()
        age = today.year - valeur.year - ((today.month, today.day) < (valeur.month, valeur.day))
        print(age)
        return age


class Database:
    def __init__ ( self = db):
        pass
    
    def insert(self, dataclass_instance_to_insert):
        Recherche = Query()
        dict_du_modele = asdict(dataclass_instance_to_insert)

        # On change les datetimes en date_strings:
        dict_du_modele = Serialization.serialize_all_dates(dict_obj = dict_du_modele)

        # On vérifie avec le nom si l'objet est déjà dans la db:
        try: db.contains(Recherche[dict_du_modele['name']])
        except RuntimeError:
            db.insert(dict_du_modele)
            print(f"Enregistrement de {dict_du_modele['name']} dans la base de données...")
        else:
            print(f"{dict_du_modele['name']} est déjà enregistré dans la base de données")

        # db.insert({'type': 'apple', 'count': 7})
        # db.insert({'type': 'peach', 'count': 3})
        # pourrait chercher et remplacer systématiquement les datetime ds les dataclasses asdict avt db.insert

    def check_if_in_db(self, to_find : str):
        """Vérifie si un objet est dans la db"""
        Recherche = Query()
        to_find = to_find.upper()
        if db.contains(Recherche.name == to_find):
            print(f"{to_find} est bien dans la base de données.")
            return True
        else:
            print("Le nom donné n'est pas dans la db.")
            return False

    def get_dict_from_db(self, to_find : str) -> dict:
        Recherche = Query()
        to_find = str(to_find).upper()
        if db.contains(Recherche.name == to_find):
            result = db.get(Recherche.name == to_find)
            serialization = Serialization()
            serialization.deserialize_all_dates(result)
            return dict(result)
        else :
            return False

    def get_in_db(self, to_find : str) -> list:
        """Cherche un objet dans la db à partir de son nom (clé = name). Prévoit les erreurs de casse.
        Renvoie les valeurs de l'objet sous forme de liste."""
        Recherche = Query()
        to_find = str(to_find).upper()
        if db.contains(Recherche.name == to_find):
        #resultat = db.search (Recherche.name.matches( a_chercher, flags=re.IGNORECASE)) # donne une liste avec tout le dico dedans
            result = db.get(Recherche.name == to_find).values()
            return list(result)
        else :
            return False
  
        # recherche = Query()
        # db.search (recherche.type == "peach") >>> [{'count': 3, 'type': 'peach'}]
        # db.search (recherche.count > 5 "peach") >>> [{'count': 7, 'type': 'apple'}]
        # pourrait chercher et remplacer systématiquement les datetime ds les dataclasses asdict après db.search
        # attention : search sensible à la casse donc prévoir que l'utilisateur n'utilise pas la bonne ( lettres maj ou minuscules etc)
        # pourrait chercher et remplacer systématiquement les date_string en datetime

    def change(self, k, v, k_to_change, v_to_change):
        """
        Modifie un objet dans la db.

        k = clé du champs pour trouver l'objet (ex : "firstname")
        v = valeur connue pour trouver l'objet (ex : "Jasper")        
        k_to_change = clé du champs à changer
        v_to_change = nouvelle valeur
        """
        Recherche = Query()
        action = db.update ({k_to_change: v_to_change}, Recherche[k] == v)
        return action
        
        # db.update ({"count" : 10}, fruit type == "apple")}) >>> [{'count': 10, 'type': 'apple'}

    def delete(self, to_delete):
        """Efface de la db, à partir du nom"""
        Recherche = Query()
        to_delete = to_delete.upper()
        db.remove (Recherche.name == to_delete)

    def getFieldList(self,fieldName):
        """ Crée une liste de toutes les valeurs correspondant à la clé donnée (fieldname)"""
        result = [r[fieldName] for r in db]
        return result
        # exemple d'utilisation dans le code : print(getFieldData('firstname')) >>> liste des prénoms

    def getFieldData(self, key, value,field_name):
        """
        clé : name, firstname, birthdate... entre guillements
        objet_a_trouver : la valeur connue entre guillements
        fieldname : la clé du champs dont on souhaite voir la valeur.

        Par exemple : si key = firstname,
        objet_a_trouver = "Brigitte" et field_name = name,
        le retour sera Bardot.
        """
        Recherche = Query()
        results = db.search( Recherche[key] == value)
        result = [r[field_name] for r in results]
        return result
        # plus tard dans le code 
        # res = getFieldData('name',"TOURNOI DES FOUS", "players")
        # for name in res:
        # print(name)

    
class Report:
    def __init__ ( self = db):
        pass
    
    def get_tournaments_list(self = db):
        """
        Génère une liste des tournois si leur nom commence pas tournoi.
        Idéalement il aurait fallu rajouter un champs "nature : tournoi ou joueur
        dans les dataclass et trouver comment récupérer
        l'objet entier d'après une clé dans la db (mais comment faire?)
        "
        """
        registered_tournaments = [] 
        result = [r['name'] for r in db]
        for r in result:
            if "TOURNOI" in r:
                registered_tournaments.append(r)
        return registered_tournaments

    def get_players_list(self = db):
        """Renvoie la liste de tous les joueurs présents dans la base de données.
        Utiliser avec : players_in_db = Report.get_players_list()"""
        registered_players = []
        result = [r['name'] for r in db]
        for r in result:
            if not "TOURNOI" in r: # il n'y a que les joueurs qui n'ont pas "tournoi"
                registered_players.append(r)
        return registered_players

    def get_names_and_ratings(self = db, players_list =[] ) -> dict:
        """ Donne une liste de dictionnaires contenant pour nom, prénom et classement de chaque joueur.
        Utiliser avec names_and_ratings = Report.get_names_and_ratings(players_list = players_in_db)"""
        players_names_and_ratings =[]
        for player in players_list :
            instance_db = Database()
            player = instance_db.get_in_db(player)
            name = player[0]
            firstname = player[1]
            rating = player[4]
            player_name_and_rating = {"name" : name, "firstname": firstname, "rating" : rating }
            players_names_and_ratings.append(player_name_and_rating)
        return players_names_and_ratings

    def sort_by_rating(self = db, list_to_sort = []):
        """Renvoie la liste des noms de joueurs triée par classement.
        Brute sous forme de dictionnaire [0] ou Bien présentée en string [1]"""
        sortable_list = self.get_names_and_ratings(list_to_sort)
        sorted_list = sorted(sortable_list, key=lambda k: k["rating"], reverse=True)
        pretty_sorted_list =[]
        for player in sorted_list:
            pplayer = "{firstname} {name}, classement :{rating}".format(**player)
            pretty_sorted_list.append(pplayer)
        return sorted_list, pretty_sorted_list

    def sort_by_name(self = db, list_to_sort = []):
        """Renvoie la liste des noms des joueurs triée par ordre alphabétique.
        Brute sous forme de dictionnaire [0] ou Bien présentée en string [1]"""
        sortable_list = self.get_names_and_ratings(list_to_sort)
        sorted_list = sorted(sortable_list, key=lambda k: k["name"])
        pretty_sorted_list =[]
        for player in sorted_list:
            pplayer = "{firstname} {name}".format(**player)
            pretty_sorted_list.append(pplayer)
        return sorted_list, pretty_sorted_list

    def get_a_report(self = db, elt = None)->list :
        if isinstance(elt, str):
            elt = elt.upper()
        else : elt = elt
        report = []
        result = [r['name'] for r in db]
        for r in result:
            if elt in r:
                report.append(r)
        return report
        # Use with : rech = Report.get_a_report(elt="TOURNOI")

#idée ?
class TimeControl(Enum):
    """Types de parties possibles"""
    blitz = auto()
    bullet = auto()
    coup_rapide = auto()


@dataclass
class Model(abc.ABC):
    """Classe abstraite : définit les méthodes communes à tous les modèles"""
    
    @abc.abstractmethod
    def __str__(self):
        """Défini l'apparence de l'objet pour l'utilisateur."""
        raise NotImplementedError


@dataclass
class Player(Model):
    """Dataclass définit automatiquement les init, repr etc."""    
    name : str = field(default = "John")
    firstname : str = field(default = "Doe")
    birthdate : datetime = field(default = datetime.datetime.strptime("05/06/1980", "%d/%m/%Y"))
    gender : str = field(default = "h")
    rating : int = field (default = 0)

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value):
        age = Serialization.calculate_age(value)
        if age < 18 or age > 99:
            raise ValueError
        self._birthdate = value

    def __str__(self):
        if self.gender == "h":
            titre = "Monsieur"
            birthdate_indication = "né le"
            ranking_indication = "classé"
        else :
            titre = "Madame"
            birthdate_indication = "née le"
            ranking_indication = "classée"
        return f"{titre} {self.firstname} {self.name}, {birthdate_indication} {self.birthdate.strftime('%d/%m/%Y')},{ranking_indication} {self.rating}"
  
 
@dataclass
class Tournament(Model):
    #TOTAL_SCORES = {}
    name : str
    location : str
    start_date : datetime = datetime.datetime.strptime("06/06/2025", "%d/%m/%Y")
    end_date : datetime = datetime.datetime.strptime("06/06/2025", "%d/%m/%Y")
    number_of_rounds : int= 4
    timecontrol : str = "bullet/blitz/coup rapide" # créer classe enum : time-control -> timecontrol : timecontrol
    description : str = ""

    # Créés au cours du tournoi :
    players : list = field(default_factory=list) # liste des noms des joueurs
    matches : list = field(default_factory=list)
    shifts : list = field(default_factory=list)
    # total_scores : dict = field(default_factory=dict)
    #  shifts = liste de dict contenant pour chaque round le début, la fin, la liste de tuples des matchs du round avec les scores
    #  ex : [{round : 1, début : x , fin : x , matches : [j1-j5, j2-j6, j3-j7, j4-j8], scores :
    # [(joueur1, score, joueur5, score), (joueur2 score, joueur6, score), etc] }

    """
    @property
    def start_date(self):
        return self.start_date
    
    @start_date.setter
    def start_date(self, value):
        assert isinstance(value, datetime.datetime), "Le contrôleur aurait du convertir cette donnée en datetime"
        assert value < datetime.datetime.now(), "La date de début ne peut être antérieure à la date d'aujourd'hui."
        assert value < self.end_date, "La date de début du tournoi doit être antérieure à la date de fin du tournoi"
        self.start_date = value 
    """

    def __str__(self):   # Pour amélioration, utiliser propriété de dataclasses : for info in dataclasses.fields(Tournament): return str(info)?
        return f"{self.name}, à {self.location},\
 du : {self.start_date.strftime('%d/%m/%Y')}, au : {self.end_date.strftime('%d/%m/%Y')},\
 {self.number_of_rounds} tours, contrôle du temps : {self.timecontrol}. {self.description}"

    def add_to_playerslist(self, joueur):
        Recherche = Query()
        # vérifier ici si joueur n'est pas dans la db
        if joueur.upper() in self.players:
            return False
        else :
            db.update(operations.add("players", [joueur.upper()]), Recherche.name == self.name)
            # print du tournoi pour vérifier :
            database = Database()
            rech = database.get_in_db(to_find=self.name)
            print(f"{joueur} ajouté, liste des joueurs = {rech[7]}, {len(rech[7])} joueurs dans le tournoi")
            self.players.append(joueur)
            return True
                
    def which_shift(self, shift_number = 0):
        """
        La fonction définit le numéro d'ordre du round au début de chaque tour
        On lui passe un objet tournoi et le numéro du tour précédent.
        Elle renvoie l'instance de Shift (nom du tournoi, numéro du tour)"""
    
        if shift_number <= int(self.number_of_rounds): # il aurait fallu caster en int lors de la déserialization
            shift_number += 1
            shift = Shift(self.name, shift_number) # est-ce que je l'ajoute là à shift.infos = {}
            shift.update_infos({"Tournament":self.name, "shift_number":shift_number})
            return shift
        else :
            return False       

    def add_to_matches(self, matches:list):
        """Ajoute la liste de tuples des matchs à la liste complète des matchs du tournoi."""
        Recherche = Query()
        db.update(operations.add("matches", matches), Recherche.name == self.name)
        return True

    def add_to_shifts(self, shift_infos : dict):
        """Ajoute le dictionnaire avec toutes les infos d'un tour à shift"""
        shift_infos = Serialization.serialize_all_times(shift_infos)
        Recherche = Query()
        db.update(operations.add("shifts", [shift_infos]), Recherche.name == self.name)
        return True

        """
        # print du tournoi pour vérifier :
        database = Database()
        rech = database.get_in_db(to_find=self.name)
        print(f"{shift_infos} ajouté, état du tournoi =")
        for info in rech:
            print(info)
        """


    def initialize_total_scores (self) -> dict:
        total_scores = {}
        for player in self.players:
            total_scores[player] = 0
        return total_scores


@dataclass
class Shift(Model):
    """
    Définit la classe Shift (chess game is played in shifts), qui référence :
    son tournoi et  son numéro d'ordre (à passer en arg)
    Et, définis au cours du round : le début du tour (date et heure), la fin du tour (date et heure), la liste de ses matchs
    """
    tournament : str # nom du tournoi
    shift_number : int # ou alors on fait un enumerate quelque part
    infos : dict = field(default_factory=dict) # à passer ensuite à tournoi

    # tournoi {rounds_infos : {round1 : {tournament name : name, round number : 1, matchs : [(a,b), (c, d), etc],
    # start_time : telle heure, end_time : telle heure, scores : [(a:0, b:1), (c:0.5, d:0.5), etc] }
    
    def __str__(self):   # Pour amélioration, utiliser propriété de dataclasses : for info in dataclasses.fields(Tournament): return str(info)?
        return f"Tour n°{self.shift_number} du {self.tournament}"

    def update_infos(self, dico=None, **to_add_to_infos):
        """ Ajoute les elt d'un dico au dico infos"""
        if dico is None:
            self.infos.update(to_add_to_infos)
        else:
            #assert isinstance(dico, dict) # print("Attention  : changement de syntaxe pour matches = matches et **")
            self.infos.update(dico)
        return True

    def create_pairs_shift1(self) -> list: #(modèle -> controleur -> vue)
        """Renvoie la liste des tuples de matchs du round"""
        database = Database()
        tournoi_dict: dict = database.get_dict_from_db(self.tournament)
        info = Report()
        players = tournoi_dict["players"]
        info.sort_by_rating(players)
        half = len(players) // 2
        first_half = players[:half]
        second_half = players[half:]
        if len(players) % 2 != 0:
            raise Exception("Impossible de générer des appairages avec un nombre impair de joueurs")
        # liste des matchs
        matches = []
        for first_half, second_half in zip(first_half, second_half):
            #print(f"Match {first_half} vs {second_half}")
            match = first_half, second_half
            matches.append(match)
        return matches
                  
        # calculer les paires du 1er round, #(modèle -> controleur -> vue)
        #  lancer le 1er round (controleur -> vue)
        # O -> enregistrer l'heure de début du round (controleur -> modèle -> db)
        # demander si finir le round (controleur -> vue)
        # O -> enregistrer l'heure de fin du round (controleur -> modèle -> db)
        # Demander les scores (controleur -> vue)
        # les scores vont dans db du Tournoi : {{round 1 : [(j1, score, j5, score), (j2, score, j6, score), etc]} (controleur -> modèle -> db)
        # calculer les paires du 2ème round ((modèle -> controleur -> vue)
        # etc. tant que nbr de rounds <= nbr annoncé
        # Le tournoi est terminé

    def create_pairs2(self, total_scores):
        players_by_scores = self.sort_by_scores(total_scores)
        sorted_list_by_score_and_rating = self.sort_by_score_and_rating(players_by_scores)
        sorted_names_list = self.simplify_list(sorted_list_by_score_and_rating)
        suggested_matches = self.suggested_matches(sorted_names_list)
        played_matches = self.get_played_matches() # à changer si je mets une variable au lieu d'un elt en plus au tournoi  
        played_matches = self.change_list_to_tuple(played_matches)
        already_played = self.matches_not_ok(suggested_matches, played_matches)
        if already_played == False:
            return suggested_matches
        else :
            other_propositions = self.propose_other_matches(sorted_names_list, played_matches)
            return other_propositions

    def sort_by_scores(self, total_scores):
        """ 
        Entrée : variable total_scores (dict. k = joueur, v = score total durant ce tournoi)
        Sortie : liste de dict. (k = 'name', 'fistname', 'rating', 'total_score')

        """
        # récupérer les scores_totaux des joueurs :
        players_total_scores = total_scores
        database = Database()
        tournoi_dict: dict = database.get_dict_from_db(self.tournament)
        
        # récupérer les noms complets avec classement :
        info = Report()
        players = tournoi_dict["players"]
        players = info.sort_by_name(players)[0]

        # assembler les deux pour trier avec la clé qu'on veut :
        for dico_joueur in players:
            for k, v in players_total_scores.items():
                to_add = {"total_score": v}
                if k in dico_joueur.values():
                    dico_joueur.update(to_add)

        # trier par score :
        players_by_scores = sorted(players, key=lambda k: k["total_score"], reverse=True)
        return players_by_scores
     
    def sort_by_score_and_rating(self, players_by_scores):
        # trouver les joueurs avec le même score:
        def get_score(player):
            return player["total_score"]
        players_group = itertools.groupby(players_by_scores, get_score)

        # trier ceux avec un score égal selon leur classement:
        groups = [] # -> liste de listes correspondant aux joueurs qui ont eu le même score
        for key, group in players_group :
            groups.append(list(group))    

        sorted_list_by_score_and_rating = [] # -> dict des joueurs trié par scores égaux et classement
        for group in groups:
            order_by_rating = sorted((group), key=lambda k: k["rating"], reverse=True)
            for j in order_by_rating:
                    sorted_list_by_score_and_rating.append(j)
        return sorted_list_by_score_and_rating

    def simplify_list(self, list_of_dict):
        # On ne garde que les noms :
        sorted_names_list = [] # -> noms des joueurs triés par scores puis classement pour un même score
        for elt in list_of_dict:
            name = elt.get('name')
            sorted_names_list.append(name)
        return sorted_names_list

    def suggested_matches(self,sorted_names_list):
        # liste des matchs proposés : associer les joueurs par 2:
        joueurs_x = sorted_names_list[0::2]
        joueurs_y = sorted_names_list[1::2]
        suggested_matches = []
        for joueurs_x, joueurs_y in zip(joueurs_x, joueurs_y):
            suggested_match = joueurs_x, joueurs_y
            suggested_matches.append(suggested_match)
        #print(f'\nMatchs proposés : {suggested_matches}')
        return suggested_matches
    
    def get_played_matches(self):
        database = Database()
        tournoi_dict: dict = database.get_dict_from_db(self.tournament)
        played_matches = tournoi_dict["matches"]
        return played_matches

    def change_list_to_tuple(self,played_matches):
        played_matches_tuples = []
        for elt in played_matches:
            match = tuple(elt)
            played_matches_tuples.append(match)
        return played_matches_tuples # à remonter pour ne faire qu'une fois. Et pourquoi ils ne sont pas en tuple dans la liste d'instance? 

    def matches_not_ok(self,suggested_matches, played_matches):
        """
        Entrée : une liste de tuples
        Renvoie True si les matches proposés n'ont pas été joués, False sinon"""
        set_propositions = set(suggested_matches)
        result = set.intersection(set_propositions, set(played_matches)) # = matchs déjà joués
        print(f'matchs déjà joués dans les proposés : {result}')
        if len(result) != 0:
            return True
        else:
            return False

    def propose_other_matches(self,sorted_names_list, played_matches):
        """ Si des matches parmis les proposés ont déjà été joués"""
        # le problème c'est que si il n'y a qu'un match déjà joué, on a plus d'adversaires à échanger !
         # donc si des matchs ont déjà été joués
        suggested_matches = []
        protagonists= sorted_names_list[0::2]
        search_opponent = len(protagonists)
        antagonists = sorted_names_list[1::2]
        joueur_x = protagonists.pop(0)
        antagonist = antagonists[0]
        test_opponent = antagonists[:]      
        while len(suggested_matches) < search_opponent:
            # for _ in range(search_opponent):
            match = (joueur_x,antagonist)
            print(f'Match proposé : {match}')
            if self.matches_not_ok([match], played_matches) == False:
                # if len(set.intersection(played_matches, set(match))) == 0:
                antagonists.remove(antagonist)
                suggested_matches.append(match)
                test_opponent = antagonists[:]
                if len(protagonists) > 0:
                    joueur_x = protagonists.pop(0)
                if len(antagonists) > 0:
                    antagonist = antagonists[0]       
            else :
                test_opponent.remove(antagonist)
                antagonist = test_opponent[0]
                continue
        
        assert len(suggested_matches) == 4
        return suggested_matches

        # trouver l'index de chaque dans la liste :
        #player_place_in_list_by_score = sorted_list.index(player)
        """
        while len(sorted_names_list) > 0:
            joueur_x = sorted_names_list.pop(0)
            for joueur_y in sorted_names_list:
                paire_consideree = {joueur_y, joueur_x} # = set
                for match in played_matches:
                    paire_match = set(match)
                    if paire_consideree != paire_match: 
                        break
                print(f"\nProposés : Match {match}")
                suggested_matches.append(match)
        """


@dataclass
class Match: # à utiliser au min pour faire un str correct
    """
    définit la classe Match, qui permet:
    d'enregistrer les parties jouées et les scores
    """
    joueur_x : str
    joueur_y : str
    score_joueur_x : float = field(default = None)
    score_joueur_y : float = field(default = None)

    def __str__(self):
        if self.score_joueur_x > self.score_joueur_y:
            return f"Match {self.joueur_x} contre {self.joueur_y}. {self.joueur_x} vainqueur."
        elif self.score_joueur_x < self.score_joueur_y:
            return f"Match {self.joueur_x} contre {self.joueur_y}. {self.joueur_y} vainqueur."
        else :
            return f"Match {self.joueur_x} contre {self.joueur_y}"


if __name__ == "__main__":
    """
    print("\n\n----------Essais sur Database :----------\n")

    Recherche = Query()
    print(db.search (Recherche.name == "WAYNE"))

    len(db)

    blop =db.get(Recherche["name"]=='BARDOT') # récupère un seul elt même si plusieurs dans la db
    print(blop)

    print(Database.getFieldList(db,'name')) # liste des noms

    print(Database.getFieldData(db,"firstname", "Bruce", "birthdate"))

    result = db.contains(Recherche["name"]=='BARDOT')# Joueur1 = Player(*joueur)
    #print(Joueur1)

    #db.remove (Recherche.name == "TOURNOI DES TSARS")

    result = [r['name'] for r in db]
    print(result)

    clés = db.all()[0].keys()
    print(clés)

    valeurs = db.all()[0].values()
    print (valeurs)

    joueur = Database.get_in_db(self = db, to_find="Fez")
    print(type(joueur))

    #trouve toutes les entrée de la db qui on le morceau dedans
    nom = db.search(Query().name.search(r'^TOUR*'))
    print(nom)

    #trouve les tournois dont le début est en 2022
    rech =db.search(Query()["start_date"].search(r'2022'))
    print(rech)

    players_in_db = Report.get_players_list()
    print(players_in_db )
    
    names_and_ratings = Report.get_names_and_ratings(players_list = players_in_db)
    print(names_and_ratings)
    
    sorted_list = Report.sort_by_rating(list_to_sort = names_and_ratings)
    print(sorted_list)

    infos = Report()
    players_in_db = infos.get_players_list()
    print(players_in_db)
    players_dict = infos.get_names_and_ratings(players_in_db)
    print(players_dict)
    choices = infos.sort_by_name(players_dict)
    print(choices)

    all = db.all()
    for elt in all:
    print(elt)

       """
    database = Database()
    

    rapport = Report()
    tournois = rapport.get_tournaments_list()
    #print(tournois)
    
 
    database = Database()

    tournoi = "Tournoi des reines"
    tournoi = tournoi.upper()

    def reset_tournament(tournoi : str):
        """Réinitialiser un tournoi après des tests"""
        # Rapidement mettre à jour une valeur :
        database.change("name", tournoi, "players",['ATOME','BARDOT','CRUZ','DOUILLET', 'ELITE', 'FEZ','GEANT','HULOT'])
        database.change("name", tournoi, "matches",[])
        database.change("name", tournoi, "shifts",[])
        #database.change("name", tournoi, "number_of_rounds",4)

    #reset_tournament(tournoi)

    #database.delete(tournoi)

    bidule = database.get_dict_from_db(tournoi)
    pprint(bidule)

    match = [("A","B"), ("H","D"), ("C","G"), ("E","F")]
    played_matches = [("A","E"), ("B","F"), ("C","G"), ("D","H"), ("F","D"),("A","G"),("C","H"),("E","B")]
    shift = Shift("Tournoi des reines", 3)
    sorted_names_list = ["A","B", "H","D","C","G","E","F"]

    shift.matches_not_ok(match,played_matches)
    shift.propose_other_matches(sorted_names_list, played_matches)
