.print Question 5 - zhengyao

SELECT s1.sid, s1.lister, p1.pid, p1.highest_bid
FROM (SELECT sales.sid, sales.lister, products.pid, sales.descr, MAX(bids.amount) as highest_bid
	  FROM bids, sales, products
      WHERE bids.sid = sales.sid AND sales.pid = products.pid
      GROUP BY sales.sid) as s1
      join
     (SELECT products.pid, MAX(bids.amount) as highest_bid
      FROM bids, sales, products
      WHERE bids.sid = sales.sid AND sales.pid = products.pid
      GROUP BY products.pid) as p1 using (pid)
WHERE s1.highest_bid * 2 < p1.highest_bid AND s1.descr LIKE '%xbox%';