import P4Controleur
import P4Vues
import UIBase




def main():
    """ Main function"""
    #1 : afficher l'accueil
    welcome = P4Vues.Welcome()
    welcome.show()
    #2 afficher le menu principal
    menu_principal = UIBase.UIFactory("menu principal").make()
    vue_menu_principal = P4Vues.UIView(menu_principal)
    menu_principal = P4Controleur.UIManager(menu_principal, vue_menu_principal)
    menu_principal.execute()


if __name__ == "__main__":
    
    main()


