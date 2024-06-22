-- Menor ganancia por region (gan_min_reg)
-- create view gan_min_reg as
select region, min(cantidad) as min_ganancia 
from prod_gan_reg
group by region;


-- Prodcutos con menor ganancia por region (gan_min_prod_reg)
-- create view gan_min_prod_reg as
select pgr.region, string_agg(pgr.producto,', ') as producto, pgr.cantidad 
from prod_gan_reg pgr
inner join gan_min_reg gmr on pgr.region = gmr.region and pgr.cantidad = gmr.min_ganancia
group by pgr.region, pgr.cantidad;


-- Maxima y minima ganancia de un producto por region (max_min_prod_region)
-- create view max_min_prod_region as
select mgpr.region, 'Maximo: ' || mgpr.producto || ' $' || mgpr.cantidad || E'\n' || 'Minimo: ' || gmpr.producto || ' $' || gmpr.cantidad as productos 
from maxganprod_region mgpr
inner join gan_min_prod_reg gmpr on mgpr.region = gmpr.region
group by mgpr.region, mgpr.producto,mgpr.cantidad,gmpr.producto,gmpr.cantidad;