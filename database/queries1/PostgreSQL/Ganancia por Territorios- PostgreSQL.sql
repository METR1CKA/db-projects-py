-- TOTOAL DE GANANCIAS (Para verificar la Cantidad Final)
select sum(od.unit_price * od.quantity * (1 - od.discount)) as total from order_details od;

-- EMPLEADOS CON SU REGION CORRESPONDIENTE (View emp_reg)
select et.employee_id, r.region_id, r.region_description
from employee_territories et
inner join territories t on et.territory_id = t.territory_id
inner join region r on t.region_id = r.region_id
group by et.employee_id, r.region_id;

-- GANANCIA POR ORDEN (View gan_reg)
select o.employee_id, sum(od.unit_price * od.quantity * (1 - od.discount)) as ganancia
from order_details od
inner join orders o on o.order_id = od.order_id
group by o.employee_id, o.order_id
order by o.order_id asc;

-- GANANCIA POR TERRITORIOS
select concat(e.first_name, ' ',e.last_name) as Nombre,string_agg(empter.territory_description, ',') as Territories, empter.GananciaTerritory
from(
	select eg.employee_id, et.territory_description, sum(eg.ganancia) as GananciaTerritory
	from gan_reg as eg
	inner join emp_ter as et on eg.employee_id = et.employee_id
	group by et.territory_id,eg.employee_id,et.territory_description) as empter
	inner join employees e on empter.employee_id = e.employee_id
	group by e.first_name,e.last_name,empter.GananciaTerritory;