.print Question 10 - zhengyao

SELECT sales.lister
FROM product_info, sales
WHERE product_info.pid = sales.pid
      AND product_info.rating > 4
      AND product_info.salecnt > (SELECT AVG(product_info.salecnt)
                                  FROM product_info)

EXCEPT

SELECT sales.lister
FROM product_info, sales
WHERE product_info.pid = sales.pid
      AND (product_info.rating <= 4
      OR product_info.salecnt < (SELECT AVG(product_info.salecnt)
                                  FROM product_info));