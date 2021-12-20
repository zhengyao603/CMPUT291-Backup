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