-- BD NorthWind
use northwind;

-- TOTOAL DE GANANCIAS (Para verificar la Cantidad Final)
select sum(UnitPrice * Quantity) as total from northwind.`order details`;

-- GANANCIA GENERADA POR REGION (Consulta Final)
select er.RegionDescription, sum(eg.ganancia) as GananciaRegion
from (select o.EmployeeID, sum(od.UnitPrice * od.Quantity * (1 - od.Discount)) as ganancia
from `order details` od
inner join orders o on o.OrderId = od.OrderID
group by o.EmployeeID
order by o.OrderID asc) as eg
inner join (select et.EmployeeID, r.RegionID, r.RegionDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID) as er on eg.EmployeeID = er.EmployeeID
group by er.RegionID;

-- GANANCIA POR ORDEN
select o.EmployeeID, sum(od.UnitPrice * od.Quantity * (1 - od.Discount)) as ganancia
from `order details` od
inner join orders o on o.OrderId = od.OrderID
group by o.EmployeeID
order by o.OrderID asc;

-- EMPLEADOS CON SU REGION CORRESPONDIENTE
select et.EmployeeID, r.RegionID, r.RegionDescription
from employeeterritories et
inner join territories t on et.TerritoryID = t.TerritoryID
inner join region r on t.RegionID = r.RegionID
group by et.EmployeeID;