SHOW databases;
use sakila;

describe address;
describe film;

select * from address limit 10;
select * from film limit 10;
show tables;

# Example 1
SELECT title, rating, length
FROM film
WHERE rating = 'PG'
  AND length > 100
ORDER BY length DESC;

# Example 2
SELECT
    rating,
    AVG(rental_rate) as avg_rental_rate,
    COUNT(*) as film_count
FROM
    film
GROUP BY
    rating;

# Example 3
SELECT *
FROM film
WHERE film_id NOT IN (
    SELECT DISTINCT film_id
    FROM inventory
);

# Example 4
SELECT customer_id, SUM(amount) AS total_spent
FROM payment
GROUP BY customer_id
HAVING SUM(amount) > 100;

# Example 5 - JOIN
SELECT 
    f.title,
    a.first_name,
    a.last_name
FROM film f
INNER JOIN film_actor fa
    ON f.film_id = fa.film_id
INNER JOIN actor a
    ON fa.actor_id = a.actor_id
LIMIT 10;


# Example 6 -- CTE
SELECT customer_id, SUM(amount) AS total_spent
FROM payment
GROUP BY customer_id
HAVING SUM(amount) > 100;

WITH top_customers AS (
    SELECT customer_id, SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
)
SELECT * FROM top_customers 
WHERE total_spent > 100;

# Example 7
SELECT 
    customer_id,
    total_spent
FROM (
    SELECT 
        customer_id,
        SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
) AS total_payments
WHERE 
    total_spent > (
        SELECT AVG(total_spent)
        FROM (
            SELECT 
                customer_id,
                SUM(amount) AS total_spent
            FROM payment
            GROUP BY customer_id
        ) AS avg_query
    )
ORDER BY total_spent DESC;

WITH total_payments AS (
    SELECT 
        customer_id,
        SUM(amount) AS total_spent
    FROM payment
    GROUP BY customer_id
)
SELECT 
    customer_id,
    total_spent
FROM 
    total_payments
WHERE 
    total_spent > (
        SELECT AVG(total_spent) FROM total_payments
    )
ORDER BY 
    total_spent DESC;

# Example 8 -- Window Function
SELECT 
  customer_id,
  amount,
  SUM(amount) OVER (PARTITION BY customer_id) AS total_spent
FROM payment;

# Example 9
SELECT 
  customer_id,
  payment_date,
  amount,
  SUM(amount) OVER (PARTITION BY customer_id ORDER BY payment_date, payment_id) AS spent_so_far
FROM payment
ORDER BY customer_id, payment_date, payment_id;

# Example 10
SELECT 
  customer_id,
  SUM(amount) AS total_spent,
  RANK() OVER (ORDER BY SUM(amount) DESC) AS spending_rank
FROM payment
GROUP BY customer_id
ORDER BY total_spent DESC;

# Example 11
SELECT
    customer_id,
    payment_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY customer_id
        ORDER BY payment_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS last_3_payments_total
FROM payment
ORDER BY customer_id, payment_date;

# Example 12 -- Correlated Subquery
SELECT payment_id, customer_id, amount
FROM payment p1
WHERE amount > (
    SELECT AVG(amount) 
    FROM payment p2
    WHERE p2.customer_id = p1.customer_id
);

SELECT payment_id, customer_id, amount
FROM (
    SELECT
        payment_id,
        customer_id,
        amount,
        AVG(amount) OVER (PARTITION BY customer_id) AS avg_amount
    FROM payment
) t
WHERE amount > avg_amount;

# Example 13
SELECT customer_id, first_name, last_name
FROM customer c
WHERE NOT EXISTS (
    SELECT 1
    FROM payment p
    WHERE p.customer_id = c.customer_id
      AND p.amount > 10
);

