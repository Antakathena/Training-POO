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
        self.show_title()    
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
        print("q) Quitter")
        return input("Votre choix : ")

class FormView(View):
    """Determine l'affichage des form"""
    def __init__(self, form: Menus.Form):
        super().__init__(form.form_name)
        self.form: Menus.Form = form

    def show(self):
        super().show()
        for i, question in enumerate(self.form.form_questions, start=self.form.start):
            print(f"{i}) {question}")
            input()
            # choice.itemview.show(position=i)
        print("q) Quitter")
       
    
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
    print("\n----------Essais sur Menus :----------\n")

    welcome = Welcome()
    welcome.show()

    menu_principal = Menus.MenuFactory("menu principal").make()
    vue_menu_principal = MenuView(menu_principal)
    vue_menu_principal.show()