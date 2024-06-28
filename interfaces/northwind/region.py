from config.database import DatabaseConfig
from database.queries import Query
from utils.northwind.region import NorthwindRegionUtils
from utils.dataframe import UtilsDataFrame


class Region:
    @staticmethod
    def northwindRegionEarnings():
        # Checar la conexión a la base de datos
        connection = DatabaseConfig.checkConnection()

        if connection is not None:
            raise Exception("Error en la conexión a la base de datos: ", connection)

        # Construir las consultas
        try:
            region_query = Query.select(columns=["*"], table="Region")
            employee_territories_query = Query.select(
                columns=["*"], table="EmployeeTerritories"
            )
            territories_query = Query.select(columns=["*"], table="Territories")
            orders_query = Query.select(columns=["*"], table="Orders")
            order_details_query = Query.select(columns=["*"], table="`Order Details`")
        except Exception as Err:
            raise Exception("Error al construir la consulta: ", Err)

        # Obtener los dataframes de las consultas
        region = UtilsDataFrame.getDataFrame(query=region_query)
        employeeTerritories = UtilsDataFrame.getDataFrame(
            query=employee_territories_query
        )
        territories = UtilsDataFrame.getDataFrame(query=territories_query)
        orders = UtilsDataFrame.getDataFrame(query=orders_query)
        orderDetails = UtilsDataFrame.getDataFrame(query=order_details_query)

        # Obtener las ganancias por región
        regionEarnings = NorthwindRegionUtils.getRegionEarnings(
            region,
            employeeTerritories,
            territories,
            orders,
            orderDetails,
        )

        result = NorthwindRegionUtils.getResult(regionEarnings)

        array_folders = ["northwind", "region"]

        # Exportar el resultado final
        file_result = UtilsDataFrame.exportToExcel(
            result, folders=array_folders, filename="RegionEarningsResult"
        )

        print("\nEl archivo se ha guardado en:", file_result)
        print("\nCon el siguiente contenido:\n")
        print(result)
