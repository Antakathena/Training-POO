import P4Controleur
import P4Vues


def main():
    """ Main function"""
    #1 : afficher l'accueil
    welcome = P4Vues.Welcome()
    welcome.show()
    #2 afficher le menu principal
    menu_principal = P4Controleur.ManagerFactory("Menu principal").make_menu()
    requested_manager = menu_principal.initial_manager()
    P4Controleur.MenuManager.react_to_answer(menu_principal, requested_manager)


if __name__ == "__main__":
    
    main()


