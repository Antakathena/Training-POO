import datetime

PLAYERS = []

class Player:
    """
    définit la classe Player, qui permet:
    d'enregistrer et de modifier les informations sur les joueurs
    """
    def __init__(self, name, firstname, birthdate, gender, rating):
        """constructeur de Player"""
        print("Création d'un joueur...")
        self.name = name
        self.firstname = firstname
        self.birthdate = birthdate
        self.gender = gender
        self.rating = rating

    @staticmethod
    def _init_debug():
        joueur1 = Player("ATOME", "Adam", datetime.datetime.strptime("01/01/1971", "%d/%m/%Y"), "homme", 2001 )
        joueur2 = Player( "BARDOT", "Brigitte", datetime.datetime.strptime("01/02/1972", "%d/%m/%Y"), "femme", 1002 )
        joueur3 = Player("CRUZ", "Chloé", datetime.datetime.strptime("01/01/1973", "%d/%m/%Y"), "femme", 2003 ) 
        joueur4 = Player("DOUILLET", "David", datetime.datetime.strptime("01/01/1974", "%d/%m/%Y"), "homme", 2004 )
        joueur5 = Player("ELITE", "Eddy", datetime.datetime.strptime("01/01/1975", "%d/%m/%Y"), "homme", 1005 )
        joueur6 = Player("FEZ", "Françoise", datetime.datetime.strptime("01/01/1976", "%d/%m/%Y"), "femme", 2006 )
        joueur7 = Player("GEANT", "George", datetime.datetime.strptime("01/01/1977", "%d/%m/%Y"), "homme", 1007 )
        joueur8 = Player("HULOT", "Harry", datetime.datetime.strptime("01/01/1978", "%d/%m/%Y"), "homme", 2008 )
        for j in (joueur1, joueur2, joueur3, joueur4, joueur5, joueur6, joueur7, joueur8):
            PLAYERS.append(j)
        #type_de_joueur = type(joueur1)
        #print(f"type de joueur1, joueur2 etc...:{type_de_joueur}")

    @property
    def birthdate(self):
        return self._birthdate
    
    @birthdate.setter
    def birthdate(self, value):
        assert isinstance(value, datetime.datetime), "Le contrôleur aurait du convertir cette donnée en datetime"
        self._birthdate = value

    def __repr__(self):
            fiche = f"Player({self.name}, {self.firstname}, {self.birthdate}, {self.gender}, {self.rating})"
            return fiche
    
    def __str__(self):
            return f"{self.name}, {self.firstname}, {self.birthdate.strftime('%d/%m/%Y')}, {self.gender}, {self.rating}"
 
    def player_serialization(self): #arg supprimé : player
        keys = ("nom","prénom","date de naissance","genre","rang")
        values = str(self)
        values_list = values.split(',')
        dict_for_player = dict(zip(keys,values_list))
        return dict_for_player   
        

if __name__ == "__main__":
    print ("Essais sur players...\n")

if __debug__: # True si le programme a été appelé SANS l'option -o
    Player._init_debug()
    print("\n\n Voici la liste de joueurs pour les tests :\n")
    for p in PLAYERS :
        print(p)