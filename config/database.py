from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os


class DatabaseConfig:
    _engine = None

    @staticmethod
    def setDatabaseName(database):
        os.environ["DB_NAME"] = database

    @staticmethod
    def getEngine():
        # Si ya existe una conexión, retornarla
        if DatabaseConfig._engine is not None:
            return DatabaseConfig._engine
        # Cargar las variables de entorno
        file = ".env"
        files = os.listdir()
        if file not in files:
            raise ValueError("No se encontró el archivo .env")
        with open(file) as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
        # Obtener los datos de conexión
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")
        host = os.environ.get("DB_HOST")
        port = os.environ.get("DB_PORT")
        database = os.environ.get("DB_NAME")
        # Crear la cadena de conexión
        connection_string = (
            f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        )
        # Crear y retornar la conexión
        DatabaseConfig._engine = create_engine(connection_string)
        return DatabaseConfig._engine

    @staticmethod
    def checkConnection():
        try:
            engine = DatabaseConfig.getEngine()
            connection = engine.connect()
            connection.close()
            return None
        except SQLAlchemyError as Err:
            return Err
