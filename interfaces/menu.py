from interfaces.pubs.author import Author
from interfaces.northwind.client import Client
from interfaces.northwind.region import Region
from interfaces.northwind.exam import Exam


class Menu:
    choice = {
        "Pubs": {
            "Ganancias por autor": Author.pubsAuthorEarnings,
        },
        "Northwind": {
            "Clientes con mas ganancia por año y región": Client.northwindClientEarnings,
            "Ganancias por región": Region.northwindRegionEarnings,
            "Ganancias por categoría, año, cliente": Exam.northwindExam,
        },
    }

    @staticmethod
    def display(options, title):
        print(f"------ {title} ------")
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
    def executeChoice(db_name, option, sys):
        try:
            Menu.choice[db_name][option]()
            sys.exit(0)
        except ValueError as err:
            print(f"Err: {err}")
            sys.exit(1)
