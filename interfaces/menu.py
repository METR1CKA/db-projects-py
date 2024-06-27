from interfaces.pubs.author import Author
from interfaces.northwind.client import Client


class Menu:
    @staticmethod
    def display(options):
        print("------ Menu ------")
        for key, value in options.items():
            print(f"{key}. {value}")

    @staticmethod
    def getChoice(options):
        choice = None
        while choice is None:
            try:
                choice = int(input("Selecciona una opción: "))
                if not choice in options:
                    print("\nPor favor, seleccione un número válido.")
                    choice = None
            except ValueError:
                print("\nPor favor, seleccione un número válido.")
                choice = None
        return choice

    @staticmethod
    def executeChoice(choice, sys):
        try:
            if choice == 1:
                Author.pubsAuthorEarnings()
            if choice == 2:
                Client.northwindClientEarnings()
            sys.exit(0)
        except Exception as err:
            print(f"Err: {err}")
            sys.exit(1)
