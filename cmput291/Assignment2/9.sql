.print Question 9 - zhengyao

CREATE VIEW product_info(pid, descr, revcnt, rating, rating6, salecnt) AS
SELECT pid, descr, revcnt, rating, rating6, salecnt
FROM (SELECT products.pid, products.descr, COUNT(previews.rid) as revcnt, AVG(previews.rating) as rating
      FROM products left outer join previews using (pid)
      GROUP BY products.pid, products.descr)
      left outer join
     (SELECT products.pid, AVG(previews.rating) as rating6
      FROM products left outer join previews using (pid)
      WHERE date('now', '-6 months') <= previews.rdate
      GROUP BY products.pid) using (pid)
      left outer join
     (SELECT pid, COUNT(sid) as salecnt
      FROM (SELECT products.pid, sales.sid
            FROM products left outer join sales using (pid)
     
            UNION
      
            SELECT products.pid, items.sid
            FROM products left outer join items using (pid))
      GROUP BY pid) using (pid);