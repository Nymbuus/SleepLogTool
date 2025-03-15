""" Module Starts the main menu of the program and handles the overhead logic. """

from modules.main_menu import MainMenu

def main():
    """ Main. Start of the program. """
    print("Please wait...")
    main_menu = MainMenu()
    main_menu.main_window()

if __name__ == '__main__':
    main()

# Behöver fortfarande fixa ADD funktionen i browse field!!!
# Får inte tillåta Front2 och Backbone eftersom dem är flexray som jag inte vet hur man läser ifrån!!!
# Extract 2 times with different buses will get not same bus error!!!
