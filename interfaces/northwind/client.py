from utils.northwind.client import NorthwindClientUtils
from utils.dataframe import UtilsDataFrame
from database.queries import Query


class Client:
    @staticmethod
    def northwindClientEarnings():
        # Construir las consultas
        customers_query = Query.select(columns=["*"], table="Customers")
        orders_query = Query.select(columns=["*"], table="Orders")
        order_details_query = Query.select(columns=["*"], table="`Order Details`")
        employees_query = Query.select(columns=["*"], table="Employees")
        employee_territories_query = Query.select(
            columns=["*"], table="EmployeeTerritories"
        )
        territories_query = Query.select(columns=["*"], table="Territories")
        region_query = Query.select(columns=["*"], table="Region")

        # Empleados, Regiones y Territorios
        employees = UtilsDataFrame.getDataFrame(query=employees_query)
        employeeTerritories = UtilsDataFrame.getDataFrame(
            query=employee_territories_query
        )
        territories = UtilsDataFrame.getDataFrame(query=territories_query)
        region = UtilsDataFrame.getDataFrame(query=region_query)

        # Ordenes, Detalles de Ordenes y Clientes
        customers = UtilsDataFrame.getDataFrame(query=customers_query)
        orders = UtilsDataFrame.getDataFrame(query=orders_query)
        orderDetails = UtilsDataFrame.getDataFrame(query=order_details_query)

        # Obtener los empleados por region
        employees = NorthwindClientUtils.getEmployeeRegion(
            employees, employeeTerritories, territories, region
        )

        # Compras de los clientes
        customerPurchases = NorthwindClientUtils.getCustomerPurchase(
            customers, orders, orderDetails, employees
        )

        # Calcular el total de las compras
        totalPurchase = NorthwindClientUtils.getTotalPurchase(customerPurchases)

        # Calcular la compra máxima
        maxPurchase = NorthwindClientUtils.getMaxTotalPurchase(totalPurchase)

        # Obtener resultados
        result = NorthwindClientUtils.getResult(totalPurchase, maxPurchase)

        # Formatear los resultados
        table = NorthwindClientUtils.getResultPivot(result)

        array_folders = ["northwind", "client"]

        # Exportar el resultado final
        file_result = UtilsDataFrame.exportToExcel(
            table, folders=array_folders, filename="ClientEarningsResult"
        )

        print("\nEl archivo se ha guardado en:", file_result)
        print("\nCon el siguiente contenido:\n")
        print(result)

        # Exportar la tabla final
        file_table = UtilsDataFrame.exportToExcel(
            result, folders=array_folders, filename="ClientEarningsTable"
        )

        print("\nEl archivo se ha guardado en:", file_table)
        print("\nCon el siguiente contenido:\n")
        print(table)
