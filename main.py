from config.database import DatabaseConfig
from interfaces.menu import Menu
from config.env import Env
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
            2: "Ganancias por región",
            3: "Ganancias por categoría, año, cliente",
            4: "Salir",
        },
    },
    3: {
        "name": "Salir",
    },
}


def main():
    try:
        Env.loadEnv()
    except Exception as Err:
        print(f"\n[-] {Err}\n")
        sys.exit(1)

    os.system("clear")

    Menu.display(
        options={key: value["name"] for key, value in db_options.items()},
        title="Seleccione una base de datos",
    )

    while True:
        choice_db = Menu.getChoice(db_options)
        choice = db_options[choice_db]
        if choice["name"] == "Salir":
            print("\nSaliendo del programa...\n")
            sys.exit(0)
        DatabaseConfig.setDatabaseName(choice["name"])
        break

    try:
        DatabaseConfig.checkConnection()
    except Exception as Err:
        print("\n[-] Error al conectar con la base de datos:\n", Err)
        sys.exit(1)

    os.system("clear")

    options = choice["options"]

    Menu.display(options, title="Seleccione una query a ejecutar")

    while True:
        choice_query = Menu.getChoice(options)
        choice_option = options[choice_query]
        if choice_option == "Salir":
            print("\nSaliendo del programa...\n")
            break
        Menu.executeChoice(db_name=Env.getEnv("DB_NAME"), option=choice_option, sys=sys)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaliendo...\n")
        sys.exit(0)
