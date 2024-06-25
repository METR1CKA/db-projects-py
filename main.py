from interfaces.menu import Menu
import sys, os

options = {
    1: "Ganancias por autor",
    2: "Clientes con mas ganancia por año y región",
    3: "Salir",
}


def main():
    os.system("clear")

    Menu.display(options)

    while True:
        choice = Menu.getChoice(options)

        if options[choice] == "Salir":
            print("\nSaliendo del programa...")
            break

        Menu.executeChoice(choice, sys)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSaliendo...")
        sys.exit(0)
