from database.queries import Query
from utils.dataframe import UtilsDataFrame
from utils.northwind.exam import NorthwindExamUtils


class Exam:
    @staticmethod
    def northwindExam():
        # Construir las consultas
        try:
            products_query = Query.select(columns=["*"], table="Products")
            order_details_query = Query.select(columns=["*"], table="`Order Details`")
            orders_query = Query.select(columns=["*"], table="Orders")
            categories_query = Query.select(columns=["*"], table="Categories")
            customers_query = Query.select(columns=["*"], table="Customers")
        except Exception as Err:
            raise Exception("Error al construir la consulta: ", Err)

        # Obtener los dataframes de las consultas
        products = UtilsDataFrame.getDataFrame(query=products_query)
        orderDetails = UtilsDataFrame.getDataFrame(query=order_details_query)
        orders = UtilsDataFrame.getDataFrame(query=orders_query)
        categories = UtilsDataFrame.getDataFrame(query=categories_query)
        customers = UtilsDataFrame.getDataFrame(query=customers_query)

        # Obtener los años
        years = NorthwindExamUtils.getYears(orders)
        topProducts = NorthwindExamUtils.getTopProducts(
            orders, products, orderDetails, categories, customers, years
        )
        mainQuery = NorthwindExamUtils.getMainQuery(
            topProducts, years, UtilsDataFrame.formatEarnings
        )

        array_folders = ["northwind", "exam"]

        # Exportar el resultado final
        file_result = UtilsDataFrame.exportToExcel(
            mainQuery, folders=array_folders, filename="ExamResult"
        )

        print("\nEl archivo se ha guardado en:", file_result)
        print("\nCon el siguiente contenido:\n")
        print(mainQuery.head(4))
