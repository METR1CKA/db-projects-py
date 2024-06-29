-- Active: 1717300958354@@127.0.0.1@3306@northwind

# Generar las ganancias por región.
SELECT reg.`RegionDescription` AS 'REGION', SUM(
        od.`UnitPrice` * od.`Quantity`
    ) AS 'GANANCIAS'
FROM
    `Region` AS reg
    JOIN `Territories` AS te ON reg.`RegionID` = te.`RegionID`
    JOIN `EmployeeTerritories` AS emt ON te.`TerritoryID` = emt.`TerritoryID`
    JOIN `Orders` AS ord ON emt.`EmployeeID` = ord.`EmployeeID`
    JOIN `Order Details` AS od ON ord.`OrderID` = od.`OrderID`
GROUP BY
    reg.`RegionDescription`;