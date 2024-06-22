-- BD NorthWind
use northwind;

-- Muestra la Ganancia del Producto mas Vendido por Region
SELECT p.ProductName, cer.RegionDescription, cer.CantidadFinal
FROM (
    SELECT od.ProductID, er.RegionDescription, SUM(od.Quantity * od.UnitPrice) AS CantidadFinal,
           ROW_NUMBER() OVER (PARTITION BY er.RegionDescription ORDER BY SUM(od.Quantity * od.UnitPrice) DESC) AS RowNum
    FROM `order details` od
    INNER JOIN orders o ON od.OrderId = o.OrderID
    INNER JOIN (
        SELECT et.EmployeeID, r.RegionID, r.RegionDescription
        FROM employeeterritories et
        INNER JOIN territories t ON et.TerritoryID = t.TerritoryID
        INNER JOIN region r ON t.RegionID = r.RegionID
        GROUP BY et.EmployeeID, r.RegionID, r.RegionDescription
    ) AS er ON er.EmployeeID = o.EmployeeID
    GROUP BY od.ProductID, er.RegionDescription
) AS cer
INNER JOIN products p ON cer.ProductID = p.ProductID
WHERE cer.RowNum = 1;

-- Producto mas Vendido por Region
select cer.ProductID, cer.RegionDescription,sum(cer.VendidoProducto) as CantidadFinal
from (select o.EmployeeID, od.ProductID, sum(od.Quantity) as VendidoProducto, er.RegionDescription
from `order details` od
inner join orders o on od.OrderId = o.OrderID
inner join (select et.EmployeeID, r.RegionID, r.RegionDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID) as er on er.EmployeeID = o.EmployeeID
group by o.EmployeeID, od.ProductID) as cer
group by cer.ProductId, cer.RegionDescription;

-- Cantidad de Producto Vendido por Empleado con su Region
select o.EmployeeID, od.ProductID, sum(od.Quantity) as VendidoProducto, er.RegionDescription
from `order details` od
inner join orders o on od.OrderId = o.OrderID
inner join (select et.EmployeeID, r.RegionID, r.RegionDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID) as er on er.EmployeeID = o.EmployeeID
group by o.EmployeeID, od.ProductID;

-- Empleados con su Region
select et.EmployeeID, r.RegionID, r.RegionDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID;

-- Verificación (Consulta para verificar la cantidad vendida por producto)
select *
from `order details` od
inner join orders o on od.OrderId = o.OrderID
where od.ProductId = 1;

select *
from `order details` od
inner join orders o on od.OrderId = o.OrderID
where od.ProductId = 60;