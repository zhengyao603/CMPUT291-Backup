.print Question 1 - zhengyao

SELECT users.email, users.name
FROM bids, sales, users
WHERE bids.sid = sales.sid 
      AND bids.bidder = users.email
      AND bids.bidder = sales.lister;