
import abc
from dataclasses import dataclass, field, asdict
import datetime
import re
from enum import Enum, auto
from pprint import pprint
from tinydb import TinyDB, Query, operations

db = TinyDB('db.json', ensure_ascii=False)

class Serialization:

    def date_serialization(datetime_obj) -> str:
        """Adapte à la db en changeant un datetime en str"""
        return datetime_obj.strftime("%d/%m/%Y")

    def serialize_all_dates(dict_obj):
        """
        Trouve les objets datetime au format datetime.datetime(2000, 1, 1, 0, 0) dans un dict.
        Change tous les datetime présents dans les valeurs d'un dict en string.
        """
        dates ={}
        for k, v in dict_obj.items() :
            if type(v) == datetime.datetime:
                dates[k] = v.strftime("%d/%m/%Y")
        for k,v in dates.items():
            dict_obj[k] = v
        return dict_obj
    
    def date_deserialization(date_string) -> datetime:
        """Adapte à l'usage un objet date str venant de la db"""
        return datetime.datetime.strptime(date_string, "%d/%m/%Y")

    def find_datestring(text) :
        """Trouve la première date au format **/**/**** dans l'élément string
        et la change en datetime."""
        match = re.search(r'\d{2}/\d{2}/\d{4}', text)
        date = datetime.datetime.strptime(match.group(), '%d/%m/%Y').date()
        print(date)
        return date

    def findall_datestring(elt) -> list:
        """Trouve juste les dates au format **/**/**** dans l'élément."""
        match = re.findall(r'\d{2}/\d{2}/\d{4}', str(elt))
        dates = []
        for date in match:
            dates.append(date)
        return dates

    def deserialize_all_dates(self, elt):
        """Trouve les dates au format **/**/**** dans l'élément.
        Les change en datetime. """
        match = re.findall(r'\d{2}/\d{2}/\d{4}', str(elt)) 
        dates = []
        for date in match:
            dates.append(date) 
        for date_string in dates : # va changer selon liste ou dico
            self.date_deserialization(date_string)
        return dates # ou elt selon la suite

    def calculate_age(birthdate):
        today = datetime.date.today()
        print(today)
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
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

    def check_if_in_db(self, a_chercher : str):
        """Vérifie si un objet est dans la db"""
        Recherche = Query()
        db.contains(Recherche[a_chercher])


    def get_in_db(self, a_chercher : str):
        """Cherche un objet dans la db à partir de son nom (clé = name). Prévoit les erreurs de casse."""
        Recherche = Query()
        a_chercher = str(a_chercher)
        resultat = db.search (Recherche.name.matches( a_chercher, flags=re.IGNORECASE))
        print(type(resultat))
        #print(resultat)
        # Bon là il faut déserialiser pour que l'objet redevienne un dico? une instance de dataclasse?, une liste d'infos?
        return resultat

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
        db.update ({k_to_change: v_to_change}, Recherche[k] == v)

        # db.update ({"count" : 10}, fruit type == "apple")}) >>> [{'count': 10, 'type': 'apple'}

    def delete(self, k, v):
        """Efface de la db"""
        Recherche = Query()
        db.remove (Recherche[k] == v)
        print(f"Objet dont {k} = {v} Effacé")

    def getFieldList(self,fieldName):
        """ Crée une liste de toutes les valeurs correspondant à la clé donnée (fieldname)"""
        result = [r[fieldName] for r in db]
        return result
        # plus tard dans le code :
        # print(getFieldData('name')) >>> liste des noms
        # print(getFieldData('firstname')) >>> liste des prénoms

    def getFieldData(self, key, objet_a_trouver,field_name):
        """
        clé : name, firstname, birthdate... entre guillements
        objet_a_trouver : la valeur cherchée entre guillements
        fieldname : la valeur que l'on souhaite trouver.

        Par exemple : si key = firstname,
        objet_a_trouver = "Brigitte" et field_name = name,
        le retour sera Bardot.
        """
        Recherche = Query()
        results = db.search( Recherche[key] == objet_a_trouver)
        result = [r[field_name] for r in results]
        return result
        # plus tard dans le code 
        # res = getFieldData('name')
        # for name in res:
        # print(name)

    def get_tournaments_list(self = db):
        """
        Génère une liste des tournois si leur nom commence pas tournoi.
        Idéalement il aurait fallu rajouter un champs "nature : tournoi ou joueur
        dans les dataclass et trouver comment récupérer
        l'objet entier d'après une clé dans la db (mais comment faire?)"
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

    def get_names_and_ratings(self = db, players_list =[]):
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
        """Renvoie la liste de dictionnaire des joueurs triée par classement.
        Utiliser avec : sorted_list = Report.sort(list_to_sort = names_and_ratings)"""
        sorted_list = sorted(list_to_sort, key=lambda k: k["rating"], reverse=True)
        pretty_sorted_list =[]
        for player in sorted_list:
            pplayer = "{firstname} {name}, classement :{rating}".format(**player)
            pretty_sorted_list.append(pplayer)
        return sorted_list, pretty_sorted_list

    def sort_by_name(self = db, list_to_sort = []):
        """Renvoie la liste de dictionnaire des joueurs triée par nom.
        Utiliser avec : sorted_list = Report.sort(list_to_sort = names_and_ratings)"""
        sorted_list = sorted(list_to_sort, key=lambda k: k["name"])
        pretty_sorted_list =[]
        for player in sorted_list:
            pplayer = "{firstname} {name}".format(**player)
            pretty_sorted_list.append(pplayer)
        return sorted_list, pretty_sorted_list

    def get_a_report(self = db, elt = "mes lunettes")->list :
        if isinstance(elt, str):
            elt = elt.upper()
        else : elt = elt
        report = []
        result = [r['name'] for r in db]
        for r in result:
            if elt in r:
                report.append(r)
        print(report)
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
    birthdate : datetime = field(default =datetime.datetime.strptime("05/06/1980", "%d/%m/%Y"))
    gender : str = field(default = "f")
    rating : int = field (default = 0)

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
  
    def insert(self):
        Database.insert(db,self)

        """
        player = asdict(self)
        player["birthdate"] = Serialization.date_serialization(player["birthdate"])
        db.insert(player)
        """

    
    def get_in_db(self,objet_a_chercher):
        super().__init__(objet_a_chercher)
        #recherche = Query()
        # db.search (recherche.type == "peach") >>> [{'count': 3, 'type': 'peach'}]
        # db.search (recherche.count > 5 "peach") >>> [{'count': 7, 'type': 'apple'}]
        # pourrait chercher et remplacer systématiquement les datetime ds les dataclasses asdict après db.search
        # attention : search sensible à la casse donc prévoir que l'utilisateur n'utilise pas la bonne ( lettres maj ou minuscules etc)
 

    def change(self):
        # db.update ({"count" : 10}, fruit type == "apple")}) >>> [{'count': 10, 'type': 'apple'}
        pass

    def delete(self):
        # >>> db.remove(recherche.count < 5) >>> db.all() >>> [{'count': 10, 'type': 'apple'}]
        pass


@dataclass
class Tournament(Model):
    name : str
    location : str
    start_date : datetime = datetime.datetime.strptime("06/06/2025", "%d/%m/%Y")
    end_date : datetime = datetime.datetime.strptime("06/06/2025", "%d/%m/%Y")
    number_of_rounds : int= 4
    timecontrol : str = "bullet/blitz/coup rapide" # créer classe enum : time-control -> timecontrol : timecontrol
    description : str = ""

    # Créés au cours du tournoi :
    players : list = field(default_factory=list) # liste d'objets Player
    rounds : list = field(default_factory=list) 
    #  rounds = dict contenant pour chaque round le début, la fin, la liste de tuples des matchs du round
    #  ex : round1, début, fin, [(joueur1, score, joueur5, score), (joueur2 score, joueur6, score), etc] 
    
    

    def __str__(self):   # Pour amélioration, utiliser propriété de dataclasses : for info in dataclasses.fields(Tournament): return str(info)?
        return f"{self.name},{self.location},{self.start_date.strftime('%d/%m/%Y')},\
{self.end_date.strftime('%d/%m/%Y')},{self.number_of_rounds},{self.timecontrol},{self.description}"

    def select_players(self, nom) :
        try:
            player = Database.get_in_db(nom)
            print(player)
            answer = input("C'est bien la fiche à ajouter? (O/n")
            if answer == "O":
                self.players.append(Player())
        except NameError:
            print("Ce joueur n'est pas dans la base de données.")

    def add_to_playerslist(self,joueur):
        Recherche = Query()
        db.update(operations.add("players",joueur), Recherche.name == self.name)


    def insert(self):
        Database.insert(db,self)

    def get_in_db(self):
        # recherche = Query()
        # db.search (recherche.type == "peach") >>> [{'count': 3, 'type': 'peach'}]
        # db.search (recherche.count > 5 "peach") >>> [{'count': 7, 'type': 'apple'}]
        # pourrait chercher et remplacer systématiquement les datetime ds les dataclasses asdict après db.search
        # attention : search sensible à la casse donc prévoir que l'utilisateur n'utilise pas la bonne ( lettres maj ou minuscules etc)
        pass

    def change(self):
        # db.update ({"count" : 10}, fruit type == "apple")}) >>> [{'count': 10, 'type': 'apple'}
        pass

    def delete(self):
        # >>> db.remove(recherche.count < 5) >>> db.all() >>> [{'count': 10, 'type': 'apple'}]
        pass


@dataclass
class Round(Model):
    """
    définit la classe Round, qui référence :
    son tournoi ?
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
    """
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
    print(asdict(tournament0))

    print("\n\n----------Essais sur Database :----------\n")

    Recherche = Query()
    print(db.search (Recherche.name == "WAYNE"))

    joueur = Database.get_in_db(self=db, objet_a_chercher="Fez")
    print(type(joueur))
    for elt in joueur:
        print(elt)
        print(type(elt))

    len(db)

    try:
        result = db.search(Recherche["name"]=='ATOME')
        print(result)
    except IndexError:
        pass

    blop =db.get(Recherche["name"]=='BARDOT') # récupère un seul elt même si plusieurs dans la db
    print(blop)

    print(Database.getFieldList(db,'name')) # liste des noms

    print(Database.getFieldData(db,"firstname", "Bruce", "birthdate"))

    
    result = db.contains(Recherche["name"]=='BARDOT')# Joueur1 = Player(*joueur)
    #print(Joueur1)

    #db.remove (Recherche.name == "TOURNOI DES TSARS")

"""

    #Crée une liste de toutes les valeurs correspondant à la clé donnée (fieldname):
    result = [r['name'] for r in db]
    print(result)



