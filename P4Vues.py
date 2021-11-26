import abc
import datetime
from dataclasses import dataclass
# pb import circulaire, solution : la vue n'a pas à connaitre les controleurs

MENUS_CHOICES = {
    "Menu principal" : ("Menu tournois","Menu joueurs","Menu rapports"),
    "Menu joueurs": ("Entrer un nouveau joueur", "Modifier un joueur","Menu principal"),
    "Menu tournois": ("Entrer un nouveau tournoi", "Modifier un tournoi", "Selectionner les joueurs", "Lancer le tournoi","Menu principal"),
    "Menu lancer le tournoi": ("Entrer un nouveau tournoi","Lancer le tournoi","Menu principal"),
    "Menu lancer le round": ("Lancer le round","Menu principal"),
    "Menu des rapports":("Liste des tournois", "Liste des joueurs par classement","Liste des joueurs par ordre alphabétique","Menu principal"),
    "Liste des informations du tournoi" : ("Liste des joueurs par ordre alphabétique", "Liste des joueurs par classement",
        "Liste des matchs", "Liste des tous (déroulé du tournoi)","Menu principal")
}

FORMS_FIELDS = {
    "Entrer un nouveau joueur" : (
        "Nom :", 
        "Prénom :",
        "Date de naissance (**/**/****) :",
        "Genre (h/f):",
        "Classement :"),
    "Entrer un nouveau tournoi" : (
        "Nom (Commencer pas tournoi):",
        "Lieu :", 
        "Date de début (**/**/****):",
        "Date de fin (**/**/****):",
        "Nombre de tours (facultatif) :",
        "Contrôle du temps (bullet/blitz/coup rapide):", 
        "Description (facultatif):")
}

# en fait ça fera une fonction pour chaque obtention de liste + choix du retour au menu:
REPORTS = {
    "Liste des tournois" :("tournois = P4Modeles.Database.get_tournaments_list()"),
    "Liste des informations du tournoi" : (
        "Liste des joueurs par ordre alphabétique", "Liste des joueurs par classement",
        "Liste des matchs", "Liste des tous (déroulé du tournoi)"),
    "Liste des joueurs par classement":(),
    "Liste des joueurs par ordre alphabétique":()
}

class ErrorMessages:
    WRONG_DATES = [
"La date de début doit être antérieure à la date de fin.",
"La date de début ne peut être antérieure à la date d'aujoud'hui.",

"\nRetour au menu principal\n"
]
    def show(self, i : int, sentences = WRONG_DATES) :
        sentence = sentences[i]
        print(sentence, sentences[-1])


class View(abc.ABC):
    """ méthode appelée par un contrôleur, affiche des choses à l'écran, les renvoie au contrôleur"""
    def __init__(self, name):
        self.name = name
        
    def show_title(self):
        title = self.name.upper()
        print(f"-----------{title}-----------")

    @abc.abstractmethod
    def show(self):
        self.show_title()
    
      
class Welcome(View):
    def __init__(self, name = "Outil de gestion de tournois d'échecs" ):
        super().__init__(name)

    def show(self):
        super().show()    
        print ("------------Bienvenue !")


class MenuView(View):
    def __init__(self, name, choices =None, start=1):
        super().__init__(name)
        self.choices = choices
        self.start = start
  
    def show(self):
        super().show()
        if self.choices == None:
            choices = MENUS_CHOICES[self.name]
        else:
            choices = self.choices
        nbr_of_choices = len(choices)
        for num, choice in enumerate(choices, start= self.start):
            print(f"{num}) {choice}")
        while True :
            answer = input("Votre choix:")
            # on vérifie que l'utilisateur entre une valeur correcte
            try :
                answer = answer.strip()
                if len(answer) != 1 or not answer.isdigit():
                    raise ValueError
                answer = int(answer)
            except ValueError :
                print(f"{answer} n'est pas un choix possible.")
                continue
            if answer >= (nbr_of_choices + 1):
                print(f"{answer} ne fait pas partie des choix. Veuillez saisir un chiffre entre 1 et {nbr_of_choices}")
                continue
            else:
                break
        answer = int(answer) - self.start
        #print(f"\ninfo dev : la vue retourne la réponse :{answer}")
        # On obtient un int coorespondant à choix -1:
        return answer
                

class FormView(View):
    def __init__(self, name):
        super().__init__(name)

    def show(self):
        super().show()
        answer : list = []
        questions = FORMS_FIELDS[self.name]
        
        for question in questions :
            print(question)
            current = input()
            if current == "q":
                break
            while "(**/**/****)" in question:
                try:
                    # faire fonction pour check if birthdate (fichier fonctions et exceptions persos)
                    #  + vérif 1920 <= birthyear <= 2016
                    current = datetime.datetime.strptime(current, "%d/%m/%Y") 
                except ValueError:
                    print("Vous n'avez pas respecté le format de date, veuillez réessayer")
                    print(question)
                    current = input()
                else : 
                    #answer.append(current)
                    break
            while "temps" in question:
                if current in ["bullet","blitz","coup rapide"]:
                    break
                else : 
                    print("Vous devez indiquer bullet, blitz ou coup rapide , veuillez réessayer")
                    print(question)
                    current = input()
            while "nombre" in question:
                if current.isdigit():
                    current = int(current)
                else :
                    try:
                        current == ""
                    except ValueError:
                        print(f"La réponse doit être laissée vide ou être un chiffre.\
                            Vous avez saisi {self.answers}. Veuillez répondre à nouveau :")
            while "date de début" in question:
                if current > datetime.datetime.now():
                    break
                else : 
                    print("La date de début du tournoi ne peut être antérieure à celle d'aujourd'hui")
                    print(question)
                    current = input() 

            answer.append(current)
        return answer

class TournamentView(View):
    def __init__(self, name = f"Lancement du tournoi"):
        super().__init__(name)

    def show(self):
        super().show()
        print(f"-----------Tour n°1 : Appeirage des joueurs...----------") 

    def start_shift(self):
        while True :
            answer = input("Commencer le tour?(l'heure sera automatiquement enregistrée.) (Saisir O)")
            if answer == "O":
                start_time = datetime.datetime.now() # ajouter à round_infos (et passer à add_to_shift_infos)
                print(start_time.strftime("%d/%m/%Y, %H:%M:%S"))
                break
            else :
                continue
        return start_time

    def end_shift(self):
        while True :
            answer = input("Finir le tour?(l'heure sera automatiquement enregistrée.) (Saisir O)")
            if answer == "O":
                end_time = datetime.datetime.now()
                print(end_time.strftime("%d/%m/%Y, %H:%M:%S"))
                break
            else :
                continue
        return end_time

    def get_scores(self, pairings) -> dict:
        """Renvoie la liste de dictionnaires des matchs de round où
        joueur : score (vainqueur =1, perdant =0, ex-equo = 0.5)"""
        # NB : liste de tuples demandé dans livret technique?
        possible_results = ["Joueur 1 gagne", "Joueur 2 gagne", "Egalité"]
        scores_dict = {}
        scores = []
        for match in pairings :
            pretty_match = f" {match[0]} vs {match[1]}"
            answer = MenuView(f"Veuillez indiquer le résultat du match:{pretty_match}", possible_results).show()
            if answer == 0:
                result = (1.0,0.0)
            elif answer == 1:
                result = (0.0,1.0)
            else:
                result = (0.5,0.5)
            
            match_score = tuple(zip(match,result)) # créé la liste de tuples demandée par l'énoncé
            for_total_score = dict(zip(match,result))
            scores_dict.update(for_total_score) # ajoute au dict des scores
            scores.append(match_score)
        return scores, scores_dict #à ajouter à info round -> find_total_score dans P4Modeles.Tournament


    if __name__ == "__main__":

        print("\n\n----------Essais sur les vues de training ----------")
    
        #welcome = Welcome()
        #welcome.show()

        #menu_principal = MenuView("Menu principal")
        #menu_principal.show()


        #menu_joueur = MenuView("menu joueurs")
        #menu_joueur.show()

        #new_player_form = FormView("Entrer un nouveau joueur")
        #new_player_form.show()

