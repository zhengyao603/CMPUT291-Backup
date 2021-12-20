.print Question 8 - zhengyao

SELECT users.email, AVG(reviews.rating) as avg_rating
FROM users, reviews
WHERE users.email = reviews.reviewee
GROUP BY users.email
HAVING COUNT(*) >= 3
ORDER BY avg_rating DESC
LIMIT 5;