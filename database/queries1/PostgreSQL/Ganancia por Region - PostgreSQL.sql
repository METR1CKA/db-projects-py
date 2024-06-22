-- TOTOAL DE GANANCIAS (Para verificar la Cantidad Final)
select sum(od.unit_price * od.quantity * (1 - od.discount)) as total from order_details od;

-- EMPLEADOS CON SUS TERRITORIOS CORRESPONDIENTEs (View emp_reg)
select et.employee_id, r.region_id, r.region_description
from employee_territories et
inner join territories t on et.territory_id = t.territory_id
inner join region r on t.region_id = r.region_id
group by et.employee_id, r.region_id, r.region_description;

-- GANANCIA POR ORDEN (View gan_reg)
select o.employee_id, sum(od.unit_price * od.quantity * (1 - od.discount)) as ganancia
from order_details od
inner join orders o on o.order_id = od.order_id
group by o.employee_id, o.order_id
order by o.order_id asc;

-- GANANCIA POR REGION
select er.region_description, sum(eg.ganancia) as GananciaRegion
from gan_reg eg
inner join emp_reg er on eg.employee_id = er.employee_id
group by er.region_description;