.print Question 2 - zhengyao

SELECT sales.sid, sales.lister, sales.cond, sales.rprice
FROM sales
WHERE sales.descr LIKE '%ticket%' OR sales.descr LIKE '%voucher%'

INTERSECT

SELECT sales.sid, sales.lister, sales.cond, sales.rprice
FROM sales, bids, users
WHERE sales.sid = bids.sid 
      AND bids.bidder = users.email 
      AND users.city LIKE '%Edmonton%';