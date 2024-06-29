from database.queries import Query
from utils.pubs.author import PubsAuthorUtils
from utils.dataframe import UtilsDataFrame


class Author:
    @staticmethod
    def pubsAuthorEarnings():
        # Construir las consultas y checar si hay errores
        try:
            query_sales = Query.select(columns=["*"], table="sales")
            query_titles = Query.select(columns=["*"], table="titles")
            query_titleauthor = Query.select(columns=["*"], table="titleauthor")
        except Exception as Err:
            raise Exception("Error al construir la consulta: ", Err)

        # Obtener los datos de las tablas sales, titles y titleauthor en dataframes
        sales = UtilsDataFrame.getDataFrame(query=query_sales)
        titles = UtilsDataFrame.getDataFrame(query=query_titles)
        titleauthor = UtilsDataFrame.getDataFrame(query=query_titleauthor)

        # Obtener las ganancias de los libros con sus autores
        ganancias = PubsAuthorUtils.getGanancias(sales, titles, titleauthor)

        # Obtener las ganancias de los libros sin autores
        regalias = PubsAuthorUtils.getRegalias(titles, titleauthor)

        # Obtener las ganancias de los libros anonimos
        anonimo = PubsAuthorUtils.getAnonimo(sales, regalias)

        # Obtener el resultado de las ganancias por autor
        first_result = PubsAuthorUtils.getResultadoGanancias(ganancias)

        # Obtener el resultado de las ganancias de los libros anonimos
        second_result = PubsAuthorUtils.getResultadoAnonimoRegalias(anonimo)

        # Obtener el resultado final
        table = PubsAuthorUtils.getResultadoFinal(first_result, second_result)

        # Exportar el resultado final
        file = UtilsDataFrame.exportToExcel(
            table, folders=["pubs"], filename="AuthorProfits"
        )

        print("\nEl archivo se ha guardado en:", file)
        print("\nCon el siguiente contenido:\n")
        print(table)
