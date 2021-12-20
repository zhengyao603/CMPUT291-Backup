.print Question 4 - zhengyao

SELECT sales.sid, sales.descr, sales.cond, COUNT(bids.sid) as num_bids, MAX(bids.amount) as highest_bid, 
       julianday(sales.edate) - julianday(date('now')) as day_left
FROM sales left outer join bids using (sid)
WHERE day_left >= 0
GROUP BY sales.sid, sales.descr, sales.cond, day_left;