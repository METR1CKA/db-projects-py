class NorthwindRegionUtils:
    @staticmethod
    def getRegionEarnings(
        region, employeeTerritories, territories, orders, orderDetails
    ):
        regionEarnings = (
            region.merge(territories, on="RegionID")
            .merge(employeeTerritories, on="TerritoryID")
            .merge(orders, on="EmployeeID")
            .merge(orderDetails, on="OrderID")
        )
        regionEarnings["Ganancias"] = (
            regionEarnings["UnitPrice"] * regionEarnings["Quantity"]
        )
        regionEarnings = regionEarnings.groupby(
            "RegionDescription", as_index=False
        ).agg({"Ganancias": "sum"})
        return regionEarnings

    @staticmethod
    def formatEarnings(value):
        return f"${value:,.2f}"

    @staticmethod
    def getResult(regionEarnings):
        regionEarnings["Ganancias"] = regionEarnings["Ganancias"].apply(
            NorthwindRegionUtils.formatEarnings
        )
        result = regionEarnings.rename(
            columns={"RegionDescription": "REGION", "Ganancias": "GANANCIAS"}
        )
        return result
