-- Productos con su ganancia por region (prod_gan_reg)
SELECT emp.region_description as Region, p.product_name as Producto,sum(od.quantity * od.unit_price *(1 - od.Discount)) as Cantidad FROM order_details od 
INNER JOIN products p on od.product_id = p.product_id
INNER JOIN orders o on od.order_id=o.order_id
INNER JOIN emp_reg as emp on o.employee_id = emp.employee_id
group by emp.region_description, p.product_name;

-- Ganancia Maxima de un Producto Region (prod_ganmax_reg)
select region, max(cantidad) as max_ganancia from prod_gan_reg
group by region;

-- Maximo Ganancia del Producto mas Vendido por Region (maxganprod_region)
SELECT pgr.region, string_agg(pgr.producto,', ') as producto, pgr.cantidad 
FROM prod_gan_reg pgr
inner join prod_ganmax_reg pgmr on pgr.region = pgmr.region and pgr.cantidad = pgmr.max_ganancia
group by pgr.region, pgr.cantidad;