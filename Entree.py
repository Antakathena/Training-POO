import P4Controleur
import P4Vues




def main(fac: P4Controleur.MenuFactory)-> None:
    """ Main function"""
   
    P4Vues.Welcome.show_title()
    P4Vues.Welcome.greetings()
    P4Vues.MenuView.show() # trouver comment afficher un main menu
    P4Controleur.MenuManager.read_menu() # et déclencher les choix du main menu

 # retrieve the menus
    menu1 = fac.get_main_menu()


    # retrieve the forms


    # retrieve the reports

#main_menu = fac.get-mainmenu_choice() # ? l'idée est de faire créer un objet main menu à la factory

if __name__ == "__main__":
    #1 : afficher l'accueil
    main()

    #2 afficher le menu principal


    #fac = read_menu()
    #main(fac)

#P4Controleur.MenuManager.execute_action()


