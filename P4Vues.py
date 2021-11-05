import abc
import Menus


 
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
    def __init__(self, name = "Outil de gestion de tournois d'échecs"):
        super().__init__(name)

    def show(self):
        super().show()    
        print ("Bienvenue")


class MenuView(View):
    """Determine l'affichage des menus"""
    def __init__(self, menu: Menus.Menu):
        super().__init__(menu.menu_name)
        self.menu: Menus.Menu = menu

    def show(self):
        super().show()
        for i, choice in enumerate(self.menu.menu_choice, start=self.menu.start):
            print(f"{i}) {choice[0]}")
            # choice.itemview.show(position=i)
        #print("q) Quitter")
        #return input("Votre choix : ")

    def prompt_for_selection(self):
        selection = input("Votre choix:")
        return selection
        

class FormView(View):
    """Determine l'affichage des form"""
    def __init__(self, form: Menus.Form):
        super().__init__(form.form_name)
        self.form: Menus.Form = form
        
    
    def show(self):
        super().show()
        answers = list()
        for question in self.form.form_questions :
            print(question)
            current = input()
            if current == "q":
                break
            else :
                answers.append(current)
        print(answers)
        return answers
        print("q) Quitter")

    
    def get_the_answers(self):
        pass
       
       
    
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

    new_player = Menus.FormFactory("Entrer un nouveau joueur").make()
    print(f"Voici la liste des questions pour le formulaire Entrer un nouveau joueur :\n{new_player}")
    typeof = type(new_player)
    print(typeof)
    

    vue_new_player = FormView(new_player)
    vue_new_player.show()


