from config.database import DatabaseConfig
import pandas as pd, os


class PubsUtils:
    @staticmethod
    def getDataFrame(query: str):
        connection = DatabaseConfig.getEngine()

        data_frame = pd.read_sql(query, connection)

        connection.dispose()

        return data_frame

    @staticmethod
    def getGanancias(sales, titles, titleauthor):
        ganancias = sales.merge(titles, on="title_id").merge(titleauthor, on="title_id")

        ganancias["Ganancia"] = (
            ganancias["price"] * ganancias["royaltyper"] * ganancias["qty"] / 100
        )

        return ganancias

    @staticmethod
    def getRegalias(titles, titleauthor):
        regalias = (
            titles.merge(titleauthor, on="title_id", how="left")
            .groupby(["title_id", "price"], as_index=False)
            .agg({"royaltyper": "sum"})
        )

        regalias["Regalias"] = 100 - regalias["royaltyper"].fillna(0)

        regalias = regalias[regalias["Regalias"] > 0]

        return regalias

    @staticmethod
    def getAnonimo(sales, regalias):
        anonimo = sales.merge(regalias, on="title_id")

        anonimo["Ganancia"] = (
            anonimo["Regalias"] * anonimo["qty"] * anonimo["price"] / 100.0
        )

        return anonimo

    @staticmethod
    def getResultadoGanancias(ganancias):
        return ganancias.groupby("au_id")["Ganancia"].sum().reset_index()

    @staticmethod
    def getResultadoAnonimoRegalias(anonimo):
        return pd.DataFrame(
            {"au_id": ["Anonimo"], "Ganancia": [anonimo["Ganancia"].sum()]}
        )

    @staticmethod
    def getResultadoFinal(first_result, second_result):
        return pd.concat([first_result, second_result], ignore_index=True)

    @staticmethod
    def exportToExcel(table: pd.DataFrame, filename: str):
        docs = "docs"
        files = os.listdir()

        if docs not in files:
            os.mkdir(docs)

        dirname = os.getcwd()

        path = os.path.join(dirname, docs, f"{filename}.xlsx")

        table.to_excel(path, index=False)

        return os.path.join("./", docs, f"{filename}.xlsx")
