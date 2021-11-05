import P4Controleur
import P4Vues
import Menus




def main():
    """ Main function"""
    #1 : afficher l'accueil
    welcome = P4Vues.Welcome()
    welcome.show()
    #2 afficher le menu principal
    menu_principal = Menus.MenuFactory("menu principal").make()
    vue_menu_principal = P4Vues.MenuView(menu_principal)
    menu_principal = P4Controleur.MenuManager(menu_principal, vue_menu_principal)
    menu_principal.execute()


if __name__ == "__main__":
    
    main()


