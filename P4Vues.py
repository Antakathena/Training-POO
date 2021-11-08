import abc
# import UIBase non car pb import circulaire, solution : la vue n'a pas à connaitre les controleurs

MENUS_CHOICES = {
    "menu principal" : ("Menu Tournois","Menu Joueurs","Menu Rapports"),
    "menu joueurs": ("Entrer un nouveau joueur","Menu rapports","Retourner au menu principal"),
    "menu tournois": ("Entrer un nouveau tournoi","Lancer le tournoi","Retourner au menu principal"),
    "menu lancer le tournoi": ("Entrer un nouveau tournoi","Lancer le tournoi","Retourner au menu principal"),
    "menu lancer le round": ("Lancer le round","Retourner au menu principal"),
    "menu des rapports (joueurs)":("Retourner au menu principal"),
    "menu des rapports (tournois)":("Retourner au menu principal"),
}

FORMS_FIELDS = {
    "Entrer un nouveau joueur" : (
        "Nom :", "Prénom :",
        "Date de naissance (**/**/****) :",
        "Genre (h/f):",
        "Classement :"),
    "Entrer un nouveau tournoi" : (
        "Nom :", "Lieu :",
        "Dates (**/**/****):",
        "Nombre de tours :",
        "Contrôle du temps :",
        "Description :")
}

 
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

    @abc.abstractmethod
    def get_the_answer(self, answer):
        return answer
      
class Welcome(View):
    def __init__(self, name = "Outil de gestion de tournois d'échecs"):
        super().__init__(name)

    def show(self):
        super().show()    
        print ("Bienvenue")

class MenuView(View):
    def __init__(self, name):
        super().__init__(name)
        choice = MENUS_CHOICES[self.name]
        return choice

    def show(self, choice):
        super().show()
        for num, choice in enumerate(choice, start=1):
            print(f"{num}) {choice[0]}")
        answer = input("Votre choix:")
        return answer

    def get_the_answer(self, choice, answer):
        try :
            answer = answer.strip()
            len(answer) == 1
            answer.isdigit()
            answer = int(answer - 1)
            print(answer)
            answer >= len(choice)
        except ValueError :
            print(f"{answer} n'est pas le numéro d'un choix possible !")
        else :
            return answer

class FormView(View):
    def __init__(self, name):
        super().__init__(name)
        questions = FORMS_FIELDS[self.name]
        return questions

    def show(self,questions):
        answer : list = []
        for question in questions :
            print(question)
            current = input()
            if current == "q":
                break
            else :
                answer.append(current)
        return answer

    def get_the_answer(self, questions,answer : list):
        try :
            assert isinstance(answer,list)
        except ValueError :
            print(f"{answer} n'est pas une liste !")
        try : 
            len(answer) == len(questions)# on vérifie que les types sont respectés
        except AssertionError :
            print(f"Vous n'avez pas répondu à toutes les questions.")

        else :
            return answer


    

    



class UIView(View):
    """Determine l'affichage des interfaces utilisateurs : menus et formulaires"""
    def __init__(self, ui: UIBase.UI):
        super().__init__(ui.name)
        self.ui: UIBase.UI = ui

    def show(self):
        super().show()
        if self.name.startswith("menu"):
            for num, choice in enumerate(self.ui.items, start=self.ui.start):
                print(f"{num}) {choice[0]}")
            selection = input("Votre choix:")
            return selection
        # le else est la vue questionnaire :    
        else : 
            answers = list()
            for question in self.ui.items[0] :
                print(question)
                current = input()
                if current == "q":
                    break
                else :
                    answers.append(current)
            print(answers)
            return answers
       
    
class ReportView(View):
    """ Défini comment les infos des rapports apparaissent à l'utilisateur"""
    pass

class PlayerView :
    """ Défini comment les infos sur les joueurs apparaissent à l'utilisateur"""
    # sauf si c'est dans le modèle
    pass

class TournamentView :
    """ Défini comment les infos sur les tournois apparaissent à l'utilisateur"""
    # sauf si c'est dans le modèle
    pass

if __name__ == "__main__":
    print("\n\n----------Essais sur les vues de training ----------")
    
    #welcome = Welcome()
    #welcome.show()

    #menu_principal = Menus.MenuFactory("menu principal").make()
    #vue_menu_principal = MenuView(menu_principal)
    #vue_menu_principal.show()
    #vue_menu_principal.prompt_for_selection()

    new_player = UIBase.UIFactory("Entrer un nouveau joueur").make()
    print(f"Voici la liste des questions pour le formulaire Entrer un nouveau joueur :\n{new_player}")
    typeof = type(new_player)
    print(typeof)
    

    vue_new_player = UIView(new_player)
    vue_new_player.show()


