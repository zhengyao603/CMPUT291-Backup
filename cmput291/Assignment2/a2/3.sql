.print Question 3 - zhengyao

SELECT sales.sid, sales.lister
FROM sales
WHERE strftime('%Y', sales.edate) - strftime('%Y', 'now') = 0
      AND strftime('%m', sales.edate) - strftime('%m', 'now') = 0
      AND strftime('%d', sales.edate) - strftime('%d', 'now') <= 3
      AND strftime('%d', sales.edate) - strftime('%d', 'now') >= 0

EXCEPT

SELECT sales.sid, sales.lister
FROM bids, sales
WHERE sales.sid = bids.sid AND bids.amount >= sales.rprice;