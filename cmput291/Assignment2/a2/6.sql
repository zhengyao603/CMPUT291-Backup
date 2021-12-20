.print Question 6 - zhengyao

SELECT sales.sid
FROM sales, reviews
WHERE sales.lister = reviews.reviewee AND sales.descr LIKE '%PS4%'
GROUP BY sales.sid
HAVING COUNT(*) >= 3 AND AVG(reviews.rating) > 4;