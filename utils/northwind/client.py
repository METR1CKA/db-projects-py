import pandas as pd


class NorthwindClientUtils:
    @staticmethod
    def getEmployeeRegion(employees, employeeTerritories, territories, region):
        regions = (
            employees.merge(employeeTerritories, on="EmployeeID")
            .merge(territories, on="TerritoryID")
            .merge(region, on="RegionID")
        )
        employeeRegion = regions[["EmployeeID", "RegionDescription"]]
        employeeRegion = employeeRegion.drop_duplicates()
        return employeeRegion

    @staticmethod
    def getCustomerPurchase(customers, orders, orderDetails, employees):
        customerPurchase = (
            customers.merge(orders, on="CustomerID")
            .merge(orderDetails, on="OrderID")
            .merge(employees, on="EmployeeID")
        )
        return customerPurchase

    @staticmethod
    def getTotalPurchase(customerPurchase):
        customerPurchase["OrderYear"] = pd.to_datetime(
            customerPurchase["OrderDate"]
        ).dt.year
        customerPurchase["TotalPurchase"] = (
            customerPurchase["Quantity"] * customerPurchase["UnitPrice"]
        )
        totalPurchase = customerPurchase.groupby(
            [
                "CustomerID",
                "CompanyName",
                "ContactName",
                "OrderYear",
                "RegionDescription",
            ],
            as_index=False,
        ).agg({"TotalPurchase": "sum"})
        return totalPurchase

    @staticmethod
    def getMaxTotalPurchase(totalPurchase):
        maxPurchases = (
            totalPurchase.groupby(["OrderYear", "RegionDescription"], as_index=False)
            .agg({"TotalPurchase": "max"})
            .rename(columns={"TotalPurchase": "MaxTotalPurchase"})
        )
        return maxPurchases

    @staticmethod
    def getResult(totalPurchase, maxPurchases):
        result = totalPurchase.merge(
            maxPurchases, on=["OrderYear", "RegionDescription"]
        )
        result = result[result["TotalPurchase"] == result["MaxTotalPurchase"]]
        result = result[
            [
                "OrderYear",
                "RegionDescription",
                "CustomerID",
                "CompanyName",
                "ContactName",
                "TotalPurchase",
            ]
        ]
        result = result.sort_values(by=["OrderYear", "RegionDescription"])
        return result

    @staticmethod
    def getResultPivot(result):
        resultPivot = result.pivot_table(
            index="OrderYear",
            columns="RegionDescription",
            values="ContactName",
            aggfunc=lambda x: ", ".join(x),
        ).reset_index()
        resultPivot.columns.name = None
        resultPivot.rename(
            columns={
                "Eastern": "Este",
                "Northern": "Norte",
                "Southern": "Sur",
                "Westerns": "Oeste",
            },
            inplace=True,
        )
        return resultPivot
