import pandas as pd


class PubsAuthorUtils:
    @staticmethod
    def getGanancias(
        sales: pd.DataFrame, titles: pd.DataFrame, titleauthor: pd.DataFrame
    ):
        ganancias = sales.merge(titles, on="title_id").merge(titleauthor, on="title_id")
        ganancias["Ganancia"] = (
            ganancias["price"] * ganancias["royaltyper"] * ganancias["qty"] / 100
        )
        return ganancias

    @staticmethod
    def getRegalias(titles: pd.DataFrame, titleauthor: pd.DataFrame):
        regalias = (
            titles.merge(titleauthor, on="title_id", how="left")
            .groupby(["title_id", "price"], as_index=False)
            .agg({"royaltyper": "sum"})
        )
        regalias["Regalias"] = 100 - regalias["royaltyper"].fillna(0)
        regalias = regalias[regalias["Regalias"] > 0]
        return regalias

    @staticmethod
    def getAnonimo(sales: pd.DataFrame, regalias: pd.DataFrame):
        anonimo = sales.merge(regalias, on="title_id")
        anonimo["Ganancia"] = (
            anonimo["Regalias"] * anonimo["qty"] * anonimo["price"] / 100.0
        )
        return anonimo

    @staticmethod
    def getResultadoGanancias(ganancias: pd.DataFrame):
        return ganancias.groupby("au_id")["Ganancia"].sum().reset_index()

    @staticmethod
    def getResultadoAnonimoRegalias(anonimo: pd.DataFrame):
        return pd.DataFrame(
            {"au_id": ["Anonimo"], "Ganancia": [anonimo["Ganancia"].sum()]}
        )

    @staticmethod
    def getResultadoFinal(first_result: pd.DataFrame, second_result: pd.DataFrame):
        final = pd.concat([first_result, second_result], ignore_index=True)
        final.columns = ["AUTOR", "GANANCIA"]
        final = final.sort_values(
            by=["AUTOR"], ascending=False, key=lambda x: x == "Anonimo"
        ).reset_index(drop=True)
        return final
