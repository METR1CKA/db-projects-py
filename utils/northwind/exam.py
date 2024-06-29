import pandas as pd


class NorthwindExamUtils:
    @staticmethod
    def getYears(orders: pd.DataFrame):
        years = orders["OrderDate"].dt.year
        years = years.unique().tolist()
        return years

    @staticmethod
    def getTopProducts(
        orders: pd.DataFrame,
        products: pd.DataFrame,
        order_details: pd.DataFrame,
        categories: pd.DataFrame,
        customers: pd.DataFrame,
        years: pd.DataFrame,
    ):
        # Filtrar los pedidos por los años seleccionados
        ordersFiltered = orders[orders["OrderDate"].dt.year.isin(years)]
        # Eliminar la columna 'UnitPrice' de 'products' antes del merge
        products = products.drop(columns=["UnitPrice"])
        # Unir las tablas para obtener los productos con más ganancias
        dataFrameMerged = pd.merge(order_details, ordersFiltered, on="OrderID")
        dataFrameMerged = pd.merge(dataFrameMerged, products, on="ProductID")
        dataFrameMerged = pd.merge(dataFrameMerged, categories, on="CategoryID")
        dataFrameMerged = pd.merge(dataFrameMerged, customers, on="CustomerID")
        dataFrameMerged["Ganancias"] = dataFrameMerged["Quantity"] * (
            dataFrameMerged["UnitPrice"] - dataFrameMerged["Discount"]
        )
        topProducts = (
            dataFrameMerged.groupby(
                [
                    "CategoryName",
                    "ProductName",
                    dataFrameMerged["OrderDate"].dt.year,
                    "CustomerID",
                    "ContactName",
                ]
            )["Ganancias"]
            .sum()
            .reset_index()
        )
        # Añadir números de fila para identificar los productos con mayores y menores ganancias
        topProducts["MaxRowNum"] = topProducts.groupby(["CategoryName", "OrderDate"])[
            "Ganancias"
        ].rank(method="first", ascending=False)
        topProducts["MinRowNum"] = topProducts.groupby(["CategoryName", "OrderDate"])[
            "Ganancias"
        ].rank(method="first", ascending=True)
        # Filtrar para obtener solo los productos con mayores y menores ganancias
        topProducts = topProducts[
            (topProducts["MaxRowNum"] == 1) | (topProducts["MinRowNum"] == 1)
        ]
        return topProducts

    @staticmethod
    def getMainQuery(topProducts: pd.DataFrame, years: pd.DataFrame, format):
        # Pivotar la tabla para obtener las columnas necesarias
        pivotTable = topProducts.pivot_table(
            index="CategoryName",
            columns="OrderDate",
            values=["ProductName", "ContactName", "CustomerID", "Ganancias"],
            aggfunc="first",
        )
        # Crear las columnas para los tres últimos años
        ultimo = f"{years[0]}"
        penultimo = f"{years[1]}"
        antepenultimo = f"{years[2]}"
        # Filtrar las columnas necesarias y formatearlas correctamente
        result = pivotTable[
            ["ProductName", "ContactName", "CustomerID", "Ganancias"]
        ].reset_index()
        result.columns = [
            f"{col[1]}_{col[0]}" if col[1] != "" else col[0] for col in result.columns
        ]
        # Formatear las columnas Producto, ContactName y Ganancias para cada año
        result[f"{ultimo}"] = (
            "(Producto: "
            + result[f"{ultimo}_ProductName"].astype(str)
            + ") - (Cliente: "
            + result[f"{ultimo}_ContactName"].astype(str)
            + ") - (Ganancias: "
            + result[f"{ultimo}_Ganancias"].apply(format).astype(str)
            + ")"
        )
        result[f"{penultimo}"] = (
            "(Producto: "
            + result[f"{penultimo}_ProductName"].astype(str)
            + ") - (Cliente: "
            + result[f"{penultimo}_ContactName"].astype(str)
            + ") - (Ganancias: "
            + result[f"{penultimo}_Ganancias"].apply(format).astype(str)
            + ")"
        )
        result[f"{antepenultimo}"] = (
            "(Producto: "
            + result[f"{antepenultimo}_ProductName"].astype(str)
            + ") - (Cliente: "
            + result[f"{antepenultimo}_ContactName"].astype(str)
            + ") - (Ganancias: "
            + result[f"{antepenultimo}_Ganancias"].apply(format).astype(str)
            + ")"
        )
        # Seleccionar solo las columnas necesarias
        result = result[
            ["CategoryName", f"{ultimo}", f"{penultimo}", f"{antepenultimo}"]
        ]
        return result
