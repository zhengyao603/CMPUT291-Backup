.echo on

--Question 1
.print Question 1 - zhengyao

SELECT users.email, users.name
FROM bids, sales, users
WHERE bids.sid = sales.sid 
      AND bids.bidder = users.email
      AND bids.bidder = sales.lister;


--Question 2
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



--Question 3
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



--Question 4
.print Question 4 - zhengyao

SELECT sales.sid, sales.descr, sales.cond, COUNT(bids.sid) as num_bids, MAX(bids.amount) as highest_bid, 
       julianday(sales.edate) - julianday(date('now')) as day_left
FROM sales left outer join bids using (sid)
WHERE day_left >= 0
GROUP BY sales.sid, sales.descr, sales.cond, day_left;



--Question 5
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



--Question 6
.print Question 6 - zhengyao

SELECT sales.sid
FROM sales, reviews
WHERE sales.lister = reviews.reviewee AND sales.descr LIKE '%PS4%'
GROUP BY sales.sid
HAVING COUNT(*) >= 3 AND AVG(reviews.rating) > 4;



--Question 7
.print Question 7 - zhengyao

SELECT email, distinct_sale, ifnull(wins, 0), ifnull(bid_amount, 0)
FROM (SELECT users.email, COUNT(DISTINCT bids.sid) as distinct_sale
	  FROM users, bids
	  WHERE users.email = bids.bidder
	  GROUP BY users.email)
      left outer join
     (SELECT email, COUNT(bid) as wins, SUM(h_bid) as bid_amount
      FROM (SELECT users.email, bids.bid
            FROM users, bids
            WHERE users.email = bids.bidder)
            join
           (SELECT bids.bid, MAX(bids.amount) as h_bid
            FROM bids
            WHERE bids.sid IN (SELECT sales.sid
                               FROM sales
                               WHERE sales.edate < date('now'))
            GROUP BY bids.sid) using (bid)
      GROUP BY email) using (email);



--Question 8
.print Question 8 - zhengyao

SELECT users.email, AVG(reviews.rating) as avg_rating
FROM users, reviews
WHERE users.email = reviews.reviewee
GROUP BY users.email
HAVING COUNT(*) >= 3
ORDER BY avg_rating DESC
LIMIT 5;



--Qeustion 9
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



--Question 10
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