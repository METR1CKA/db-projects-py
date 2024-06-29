from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from config.env import Env
import os


class DatabaseConfig:
    _engine = None

    @staticmethod
    def setDatabaseName(database):
        Env.setEnv("DB_NAME", database)

    @staticmethod
    def getEngine():
        # Si ya existe una conexión, retornarla
        if DatabaseConfig._engine is not None:
            return DatabaseConfig._engine
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
            return
        except SQLAlchemyError as Err:
            return Err
