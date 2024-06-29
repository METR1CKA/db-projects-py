import pandas as pd


class NorthwindClientUtils:
    @staticmethod
    def getEmployeeRegion(
        employees: pd.DataFrame,
        employeeTerritories: pd.DataFrame,
        territories: pd.DataFrame,
        region: pd.DataFrame,
    ):
        regions = (
            employees.merge(employeeTerritories, on="EmployeeID")
            .merge(territories, on="TerritoryID")
            .merge(region, on="RegionID")
        )
        employeeRegion = regions[["EmployeeID", "RegionDescription"]]
        employeeRegion = employeeRegion.drop_duplicates()
        return employeeRegion

    @staticmethod
    def getCustomerPurchase(
        customers: pd.DataFrame,
        orders: pd.DataFrame,
        orderDetails: pd.DataFrame,
        employees: pd.DataFrame,
    ):
        customerPurchase = (
            customers.merge(orders, on="CustomerID")
            .merge(orderDetails, on="OrderID")
            .merge(employees, on="EmployeeID")
        )
        return customerPurchase

    @staticmethod
    def getTotalPurchase(customerPurchase: pd.DataFrame):
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
    def getMaxTotalPurchase(totalPurchase: pd.DataFrame):
        maxPurchases = (
            totalPurchase.groupby(["OrderYear", "RegionDescription"], as_index=False)
            .agg({"TotalPurchase": "max"})
            .rename(columns={"TotalPurchase": "MaxTotalPurchase"})
        )
        return maxPurchases

    @staticmethod
    def getResult(totalPurchase: pd.DataFrame, maxPurchases: pd.DataFrame):
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
    def getResultPivot(result: pd.DataFrame):
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
