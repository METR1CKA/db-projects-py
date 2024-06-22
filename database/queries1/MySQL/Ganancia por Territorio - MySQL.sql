-- BD NorthWind
use northwind;

-- Total de Ganancias 
select sum(UnitPrice * Quantity) as total from northwind.`order details`;

-- Ganancia por Territorios que tenga el Empleado
select concat(e.FirstName, ' ',e.LastName) as Nombre,group_concat(empter.TerritoryDescription) as Territories, empter.GananciaTerritory
from(select eg.EmployeeID, et.TerritoryDescription, sum(eg.ganancia) as GananciaTerritory
from (select o.EmployeeID, o.OrderID,sum(od.UnitPrice * od.Quantity * (1 - od.Discount)) as ganancia
from `order details` od
inner join orders o on o.OrderId = od.OrderID
group by o.OrderID) as eg
inner join (select et.EmployeeID, t. TerritoryID, t.TerritoryDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID) as et on eg.EmployeeID = et.EmployeeID
group by et.TerritoryID) as empter
inner join employees e on empter.EmployeeID = e.EmployeeID
group by empter.GananciaTerritory;

-- Ganancia por Territorio (Territorios Duplicados)
select eg.EmployeeID, et.TerritoryDescription, sum(eg.ganancia) as GananciaTerritory
from (select o.EmployeeID, o.OrderID,sum(od.UnitPrice * od.Quantity * (1 - od.Discount)) as ganancia
from `order details` od
inner join orders o on o.OrderId = od.OrderID
group by o.OrderID) as eg
inner join (select et.EmployeeID, t. TerritoryID, t.TerritoryDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID) as et on eg.EmployeeID = et.EmployeeID
group by et.TerritoryID;

-- Ganancia por Orden
select o.EmployeeID, o.OrderID,sum(od.UnitPrice * od.Quantity * (1 - od.Discount)) as ganancia
from `order details` od
inner join orders o on o.OrderId = od.OrderID
group by o.OrderID;

-- Empleados con su Territorio
select et.EmployeeID, t. TerritoryID, t.TerritoryDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID;