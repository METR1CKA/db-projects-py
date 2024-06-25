from config.database import DatabaseConfig
from database.queries import Query
from utils.pubs import PubsUtils


class Author:
    @staticmethod
    def pubsAuthorEarnings():
        # Checar la conexión a la base de datos
        connection = DatabaseConfig.checkConnection()

        if connection is not None:
            raise Exception("Error en la conexión a la base de datos: ", connection)

        # Construir las consultas y checar si hay errores
        try:
            query_sales = Query.select(columns=["*"], table="sales")
            query_titles = Query.select(columns=["*"], table="titles")
            query_titleauthor = Query.select(columns=["*"], table="titleauthor")
        except Exception as Err:
            raise Exception("Error al construir la consulta: ", Err)

        # Obtener los datos de las tablas sales, titles y titleauthor en dataframes
        sales = PubsUtils.getDataFrame(query=query_sales)
        titles = PubsUtils.getDataFrame(query=query_titles)
        titleauthor = PubsUtils.getDataFrame(query=query_titleauthor)

        # Obtener las ganancias de los libros con sus autores
        ganancias = PubsUtils.getGanancias(sales, titles, titleauthor)

        # Obtener las ganancias de los libros sin autores
        regalias = PubsUtils.getRegalias(titles, titleauthor)

        # Obtener las ganancias de los libros anonimos
        anonimo = PubsUtils.getAnonimo(sales, regalias)

        # Obtener el resultado de las ganancias por autor
        first_result = PubsUtils.getResultadoGanancias(ganancias)

        # Obtener el resultado de las ganancias de los libros anonimos
        second_result = PubsUtils.getResultadoAnonimoRegalias(anonimo)

        # Obtener el resultado final
        table = PubsUtils.getResultadoFinal(first_result, second_result)

        # Exportar el resultado final
        file = PubsUtils.exportToExcel(table, filename="PubsResultAuthorProfits")

        print("\nEl archivo se ha guardado en:", file)
        print("\nCon el siguiente contenido:\n")
        print(table)
