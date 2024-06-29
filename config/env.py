import os


class Env:
    @staticmethod
    def loadEnv():
        # Cargar las variables de entorno
        file = ".env"
        files = os.listdir()
        if file not in files:
            raise ValueError("No se encontró el archivo .env")
        with open(file) as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    Env.setEnv(key, value)

    @staticmethod
    def setEnv(key, value):
        os.environ[key] = value

    @staticmethod
    def getEnv(key):
        return os.environ.get(key)
