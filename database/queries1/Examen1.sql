-- BD NORTWIND
use northwind;

-- Categorias
select * from categories;

-- Producto, Region, Categoria y Año con ganancia
-- CREATE VIEW gan_reg_cat_pro AS
SELECT er.RegionDescription AS Region, p.CategoryID AS Categoria,p.ProductName AS Producto,sum(od.Quantity * od.UnitPrice) AS Cantidad , YEAR(o.OrderDate) AS Fecha 
FROM `order details` od 
INNER JOIN products p ON od.ProductID = p.ProductID
INNER JOIN orders o ON od.OrderID=o.OrderID
INNER JOIN emp_reg er ON o.EmployeeID = er.EmployeeID
GROUP BY Region, Producto, Fecha;

-- Productos con su region por categoria y su ganancia
-- CREATE VIEW prod_cat_gan AS
SELECT Region, Categoria, Producto, SUM(Cantidad) as CantidadTotal 
FROM gan_reg_cat_pro
GROUP BY Region, Categoria, Producto
HAVING SUM(Cantidad) = (
  SELECT MAX(sub.CantidadTotal)
  FROM (
    SELECT Region, Categoria, SUM(Cantidad) AS CantidadTotal
    FROM gan_reg_cat_pro
    GROUP BY Region, Categoria, Producto
  ) AS sub
  WHERE sub.Region = gan_reg_cat_pro.Region
  AND sub.Categoria = gan_reg_cat_pro.Categoria
);

SELECT grcp.Region, grcp.Categoria, grcp.Producto, grcp.Fecha, grcp.Cantidad
FROM gan_reg_cat_pro grcp
INNER JOIN prod_cat_gan pcg ON grcp.Region = pcg.Region AND grcp.Categoria = pcg.Categoria
ORDER BY grcp.Categoria ASC;




-- Maximo producto vendido con el año
-- CREATE VIEW max_vent AS
SELECT g.Region, g.Categoria, g.Producto, g.Fecha FROM gan_reg_cat_pro g
INNER JOIN (
	SELECT Region , Producto,MAX(Cantidad) as MaxGan, Fecha, Categoria FROM gan_reg_cat_pro ga
	GROUP BY Region , Producto, Categoria
) gao ON g.Region = gao.Region AND g.Cantidad = gao.MaxGan
GROUP BY g.Region, g.Producto, g.Categoria;

-- Union de estas dos vistas prod_cat_gan y max_vent
-- CREATE VIEW union_prod_vent AS
SELECT pcg.Region, mv.Categoria, concat(pcg.Producto," ", mv.Fecha) AS Producto FROM prod_cat_gan pcg
INNER JOIN max_vent mv ON pcg.Region = mv.Region AND pcg.Producto = mv.Producto
GROUP BY pcg.Region, pcg.Categoria;

--  Mostrando cada categoria con el producto mas vendido por region (Consulta Final)
SELECT c.CategoryName,
(Select Producto FROM union_prod_vent upv WHERE upv.Region = "Eastern" AND upv.Categoria = upvf.Categoria ) AS Eastern,
(Select Producto FROM union_prod_vent upv WHERE upv.Region = "Northern" AND upv.Categoria = upvf.Categoria ) AS Northern,
(Select Producto FROM union_prod_vent upv WHERE upv.Region = "Southern" AND upv.Categoria = upvf.Categoria ) AS Southern,
(Select Producto FROM union_prod_vent upv WHERE upv.Region = "Westerns" AND upv.Categoria = upvf.Categoria ) AS Westerns
FROM union_prod_vent upvf
INNER JOIN categories c ON c.CategoryID = upvf.Categoria
group by Categoria;












###############################################################################

-- Mostrando cada categoria con el producto mas vendido por region (Consulta Final (Falsa))
SELECT c.CategoryName, 
concat(
	(SELECT Producto FROM prod_cat_gan pcg WHERE pcg.Region = "Eastern" AND pcg.Categoria = grcp.Categoria),
    ' ',
    (SELECT Fecha FROM max_vent mv WHERE mv.Region = "Eastern" AND mv.Categoria = grcp.Categoria AND mv.Producto = grcp.Producto)
) as Eastern,
concat(
	(SELECT Producto FROM prod_cat_gan pcg WHERE pcg.Region = "Northern" AND pcg.Categoria = grcp.Categoria),
    ' ',
    (SELECT Fecha FROM max_vent mv WHERE mv.Region = "Northern" AND mv.Categoria = grcp.Categoria AND mv.Producto = grcp.Producto)
) as Northern,
concat(
	(SELECT Producto FROM prod_cat_gan pcg WHERE pcg.Region = "Southern" AND pcg.Categoria = grcp.Categoria),
    ' ',
    (SELECT Fecha FROM max_vent mv WHERE mv.Region = "Southern" AND mv.Categoria = grcp.Categoria AND mv.Producto = grcp.Producto)
) as Southern,
concat(
	(SELECT Producto FROM prod_cat_gan pcg WHERE pcg.Region = "Westerns" AND pcg.Categoria = grcp.Categoria),
    ' ',
    (SELECT Fecha FROM max_vent mv WHERE mv.Region = "Westerns" AND mv.Categoria = grcp.Categoria AND mv.Producto = grcp.Producto)
) as Westerns
FROM gan_reg_cat_pro grcp
INNER JOIN categories c ON c.CategoryID = grcp.Categoria
GROUP BY Categoria;

-- Maximo Producto por region y categoria 
-- CREATE VIEW reg_cat_prod AS
SELECT pcg.Region, pcg.Categoria, pcg.Producto, pcg.CantidadTotal
FROM prod_cat_gan pcg
INNER JOIN (
    SELECT Region, Categoria, MAX(CantidadTotal) AS MaxGan
    FROM prod_cat_gan
    GROUP BY Region, Categoria
) q1 ON q1.Region = pcg.Region AND q1.Categoria = pcg.Categoria AND q1.MaxGan = pcg.CantidadTotal;


-- Apartir de aqui es la consulta que me corrigio y lo tenia por año, no por toda la historia
-- Maximo producto por categoria y region
-- CREATE VIEW prod_ano_cat_new AS
SELECT g.Region, g.Categoria, group_concat(g.Producto, ' ' , g.Fecha ) AS Producto, g.Cantidad FROM gan_reg_cat_pro g
INNER JOIN (
	SELECT Region , Producto,MAX(Cantidad) as MaxGan, Fecha FROM gan_reg_cat_pro ga
	GROUP BY Region , Categoria
) gao ON g.Region = gao.Region AND g.Cantidad = gao.MaxGan
GROUP BY g.Region, g.Fecha, g.Producto, g.Categoria;

-- Maxima cantidad por producto con su categoria y Region con año
-- CREATE VIEW consu_final as
SELECT c.CategoryName, 
(select Producto from prod_ano_cat_new q1
where q1.Region = "Eastern" and q1.Categoria = pac.Categoria) as Eastern,
(select Producto from prod_ano_cat_new q1
where q1.Region = "Southern" and q1.Categoria = pac.Categoria) as Southern,
(select Producto from prod_ano_cat_new q1
where q1.Region = "Northern" and q1.Categoria = pac.Categoria) as Northern,
(select Producto from prod_ano_cat_new q1
where q1.Region = "Westerns" and q1.Categoria = pac.Categoria) as Westerns
FROM prod_ano_cat pac
INNER JOIN  categories c on pac.Categoria = c.CategoryID 
GROUP BY pac.Categoria;