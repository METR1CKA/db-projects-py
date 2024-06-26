from config.database import DatabaseConfig
import pandas as pd, os


class UtilsDataFrame:
    @staticmethod
    def getDataFrame(query: str):
        connection = DatabaseConfig.getEngine()
        data_frame = pd.read_sql(query, connection)
        connection.dispose()
        return data_frame
