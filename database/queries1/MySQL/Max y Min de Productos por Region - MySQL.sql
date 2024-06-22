-- BD Northwind
use northwind;

-- Empleados con su Region
select et.EmployeeID, r.RegionID, r.RegionDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID;

-- Consulta de Productos por Region con su Ganancia
select er.RegionDescription, p.ProductName,sum(od.Quantity * od.UnitPrice) as Ganancia 
from `order details` od 
inner join products p on od.ProductID = p.ProductID
inner join orders o on od.OrderID=o.OrderID
inner join (select et.EmployeeID,r.RegionID,r.RegionDescription  
FROM employeeterritories et 
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID) as er on o.EmployeeID = er.EmployeeID
group by er.RegionDescription, p.ProductName;

-- Region con Maxima Ganancia y Minima Ganancia
select q1.RegionDescription,max(ganancia) as MaxGanancia, min(ganancia) as MinGanancia
from (select er.RegionDescription, p.ProductName,sum(od.Quantity * od.UnitPrice) as Ganancia 
from `order details` od 
inner join products p on od.ProductID = p.ProductID
inner join orders o on od.OrderID=o.OrderID
inner join (select et.EmployeeID,r.RegionID,r.RegionDescription  
FROM employeeterritories et 
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID) as er on o.EmployeeID = er.EmployeeID
group by er.RegionDescription, p.ProductName) as q1 
group by q1.RegionDescription;