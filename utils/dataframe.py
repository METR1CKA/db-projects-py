from config.database import DatabaseConfig
import pandas as pd, os


class UtilsDataFrame:
    @staticmethod
    def getDataFrame(query):
        connection = DatabaseConfig.getEngine()
        data_frame = pd.read_sql(query, connection)
        connection.dispose()
        return data_frame

    @staticmethod
    def exportToExcel(table: pd.DataFrame, folders: list, filename: str):
        docs = "docs"
        dirname = os.getcwd()
        full_folder_path = os.path.join(dirname, docs, *folders)
        if not os.path.exists(full_folder_path):
            os.makedirs(full_folder_path)
        path = os.path.join(full_folder_path, f"{filename}.xlsx")
        table.to_excel(path, index=False)
        return os.path.join("./", docs, *folders, f"{filename}.xlsx")
