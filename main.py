from config.database import DatabaseConfig
from database.queries import Query
from utils.pubs import PubsUtils
import sys

if __name__ == "__main__":
    # Checar la conexión a la base de datos
    connection = DatabaseConfig.checkConnection()

    if connection is not None:
        print("Error en la conexión:", connection)
        sys.exit(1)

    # Construir las consultas y checar si hay errores
    try:
        query_sales = Query.select(columns=["*"], table="sales")
        query_titles = Query.select(columns=["*"], table="titles")
        query_titleauthor = Query.select(columns=["*"], table="titleauthor")
    except Exception as Err:
        print("Error al construir la consulta:", Err)
        sys.exit(1)

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
    file = PubsUtils.exportToExcel(table, filename="resultado_final")

    print("\nEl archivo se ha guardado en:", file)
    print("\nCon el siguiente contenido:\n")
    print(table)
