from interfaces.menu import Menu
from config.database import DatabaseConfig
import sys, os


db_options = {
    1: {
        "name": "Pubs",
        "options": {
            1: "Ganancias por autor",
            2: "Salir",
        },
    },
    2: {
        "name": "Northwind",
        "options": {
            1: "Clientes con mas ganancia por año y región",
            2: "Salir",
        },
    },
    3: {
        "name": "Salir",
    },
}


def main():
    os.system("clear")

    Menu.display(
        {key: value["name"] for key, value in db_options.items()},
        "Seleccione una base de datos",
    )

    while True:
        choice_db = Menu.getChoice(db_options)
        choice = db_options[choice_db]
        if choice["name"] == "Salir":
            print("\nSaliendo del programa...\n")
            sys.exit(0)
        DatabaseConfig.setDatabaseName(choice["name"])
        break

    os.system("clear")

    options = choice["options"]

    Menu.display(options, "Seleccione una query a ejecutar")

    while True:
        choice_query = Menu.getChoice(options)
        if options[choice_query] == "Salir":
            print("\nSaliendo del programa...\n")
            break
        Menu.executeChoice(
            db_name=choice["name"], option=choice["options"][choice_query], sys=sys
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaliendo...\n")
        sys.exit(0)
