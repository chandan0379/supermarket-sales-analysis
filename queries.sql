SELECT * FROM supermarket_sales;

SELECT city, SUM(sales) AS total_sales
FROM supermarket_sales
GROUP BY city;

SELECT product_line, AVG(rating) AS avg_rating
FROM supermarket_sales
GROUP BY product_line
ORDER BY avg_rating DESC;