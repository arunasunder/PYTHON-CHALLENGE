/*  **********************************************************************************
SQL Queries 
Written By: 				Aruna Amaresan
Created on: 			Jan 11th 2018 
Last updated: 			Jan 29th 2018

Pre-requistes: Ensure that sakila DB is unzipped and loaded on SQL Workbench or your SQL Editor
						on you local drive. Also ensure all SQL installs for SQL Server are completed 

**************************************************************************************         */

USE sakila; 

SELECT first_name, last_name FROM actor; -- Returns 200 rows 


-- 1b Display the first and last name of each actor in a single column in upper case letters. 
--       Name the column Actor Name.
SELECT concat (first_name, ' ', last_name) AS 'Actor Name' FROM actor; 

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
--        Returns one row Joe Swank with that value 
SELECT actor_id, first_name, last_name 
FROM actor
WHERE first_name = 'Joe';  

-- 2b. Find all actors whose last name contain the letters GEN:
SELECT actor_id, first_name, last_name 
FROM actor
WHERE last_name LIKE '%GEN%'; 

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT actor_id, first_name, last_name 
FROM actor
WHERE last_name LIKE '%LI%'
ORDER BY last_name, first_name; 

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT country_id, country 
FROM country
WHERE country IN ('Afghanistan', 'Bangladesh', 'China'); 

-- 3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type.
ALTER TABLE actor
ADD middle_name VARCHAR(45) 
AFTER first_name;

SELECT * 
FROM actor; 

SELECT version();
SELECT @@GLOBAL.sql_mode;
SELECT @@SESSION.sql_mode;

-- 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.
ALTER TABLE actor 
MODIFY COLUMN middle_name BLOB;

SELECT * 
FROM actor
ORDER by last_name, first_name; 

-- 3c. Now delete the middle_name column.
ALTER TABLE actor
DROP COLUMN middle_name; 

SELECT *
FROM actor
ORDER by last_name, first_name; 

-- 4a. List the last names of actors, as well as how many actors have that last name.
SELECT DISTINCT last_name AS 'Last Name', COUNT('Last Name') AS 'Count'
FROM actor
GROUP BY last_name;


-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors
SELECT DISTINCT last_name AS 'Last Name', COUNT('Last Name') AS 'Count'
FROM actor
GROUP BY last_name
HAVING COUNT('Last Name') >= 2;

-- 4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS, the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.
SELECT * 
FROM actor
WHERE ((last_name = 'Williams') AND (first_name = 'Groucho') );

UPDATE actor
SET first_name = 'HARPO'
WHERE ((last_name = 'Williams') AND (first_name = 'Groucho') );

SELECT * 
FROM actor 
WHERE last_name = 'Williams';

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO. Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.)
UPDATE actor
SET first_name =
CASE WHEN first_name = 'HARPO' THEN 'GROUCHO'
ELSE 'MUCHO GROUCHO' END
WHERE actor_id = 172;

SELECT * 
FROM actor 
WHERE last_name = 'Williams';

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
SHOW CREATE TABLE address;

CREATE TABLE address_Copy LIKE address; 

SHOW CREATE TABLE address_Copy;

-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:
SELECT first_name, last_name, address, district, postal_code
FROM staff 
INNER JOIN address
ON staff.address_id = address.address_id;

-- SELECT * from staff; 

-- SELECT * from address; 

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment
SELECT * 
FROM payment 
WHERE payment_date >= '20050801' and payment_date <= '20050831'
ORDER BY payment_date;  

SELECT payment.staff_id, first_name, last_name, SUM(amount)
FROM payment 
INNER JOIN staff
ON payment.staff_id = staff.staff_id
WHERE payment_date >= '20050801' and payment_date <= '20050831'
GROUP BY payment.staff_id;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.
SELECT film.film_id, title, COUNT(actor_id) 
FROM film
INNER JOIN film_actor
ON film.film_id = film_actor.film_id
GROUP BY film_actor.film_id;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?
-- He has 6 copies 
/*SELECT * 
FROM film 
WHERE title = 'Hunchback Impossible';

SELECT * 
FROM inventory 
WHERE film_id = '439'; */

SELECT film.film_id, film.title, COUNT(inventory_id)
FROM film 
INNER JOIN inventory
ON film.film_id = inventory.film_id
WHERE film.title = 'Hunchback Impossible'
GROUP BY inventory.film_id;

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. 
-- List the customers alphabetically by last name:
SELECT first_name, last_name, SUM(amount)
FROM customer
INNER JOIN payment
ON customer.customer_id = payment.customer_id
GROUP BY payment.customer_id
ORDER BY customer.last_name;

-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. 
-- As an unintended consequence, films starting with the letters K and Q have also soared in 
-- popularity. Use subqueries to display the titles of movies starting with the letters K and Q 
-- whose language is English.

SELECT film.title FROM film 
WHERE
(film.title LIKE 'K%' OR film.title LIKE 'Q%' ) AND 
(language_id = 
(SELECT language.language_id FROM sakila.language WHERE language.name = 'English')
);

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.
/* SELECT film.film_id from film 
WHERE film.title = 'Alone Trip' ;

SELECT film_actor.actor_id FROM film_actor
WHERE film_actor.film_id = 17;

SELECT actor.first_name, actor.last_name FROM actor 
WHERE actor.actor_id IN (3,12,13,82,100, 160, 167,187); */

SELECT actor.first_name, actor.last_name FROM actor 
WHERE actor.actor_id IN (
(SELECT film_actor.actor_id FROM film_actor
WHERE film_actor.film_id = 
(SELECT film.film_id from film 
WHERE film.title = 'Alone Trip' )
)
);

-- 7c. You want to run an email marketing campaign in Canada, for which you will need 
-- the names and email addresses of all Canadian customers. Use joins to retrieve this 
-- information.

SELECT customer.first_name, customer.last_name, customer.email 
FROM customer
INNER JOIN address
ON customer.address_id = address.address_id 
WHERE address.address_id IN 

(
SELECT address.address_id from address 
WHERE address.city_id  
IN 

(
(SELECT city.city_id
FROM city 
WHERE city.country_id = 
(SELECT country.country_id from country where country.country = 'Canada')
)
)
)
;

-- 7d. Sales have been lagging among young families, and you wish to target all 
-- family movies for a promotion. Identify all movies categorized as famiy films.
SELECT * FROM film 
INNER JOIN film_category
ON film_category.film_id = film.film_id
WHERE film_category.film_id IN 
(

SELECT film_category.film_id FROM film_category 
WHERE film_category.category_id = 
(

SELECT category.category_id FROM category
WHERE category.name = 'Family'

)

);

-- 7e. Display the most frequently rented movies in descending order.
SELECT film.film_id, film.title, COUNT(rental.rental_id) AS 'RentalCount', film.release_year, film.rating
FROM film
INNER JOIN inventory
ON film.film_id = inventory.film_id
INNER JOIN rental
ON  inventory.inventory_id = rental.inventory_id
GROUP BY inventory.film_id
ORDER BY COUNT(rental.rental_id) DESC;

-- 7f. Write a query to display how much business, in dollars, each store brought in.
SELECT store.store_id, SUM(payment.amount) AS 'TotalRevenue'
FROM payment 
INNER JOIN customer
ON payment.customer_id = customer.customer_id
INNER JOIN store 
ON customer.store_id = store.store_id
GROUP BY store.store_id
ORDER BY SUM(payment.amount) DESC;

-- 7g. Write a query to display for each store its store ID, city, and country.
SELECT store.store_id, city.city, country.country
FROM store 
INNER JOIN address
ON store.address_id = address.address_id
INNER JOIN city 
ON address.city_id = city.city_id
INNER JOIN country
ON city.country_id = country.country_id
GROUP BY store.store_id;

-- 7h. List the top five genres in gross revenue in descending order. 
-- (Hint: you may need to use the following tables: category, film_category, inventory, 
-- payment, and rental.)
SELECT category.category_id, category.name, SUM(payment.amount)
FROM category 
INNER JOIN film_category
ON category.category_id = film_category.category_id
INNER JOIN inventory
ON inventory.film_id = film_category.film_id
INNER JOIN rental 
ON rental.inventory_id = inventory.inventory_id
INNER JOIN payment 
ON payment.rental_id = rental.rental_id
GROUP BY category.category_id
ORDER BY SUM(payment.amount) DESC 
LIMIT 5;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the 
-- Top five genres by gross revenue. Use the solution from the problem above to create a view. 
-- If you haven't solved 7h, you can substitute another query to create a view.
CREATE VIEW top_5_grossrevenue_genres as
(
SELECT category.category_id, category.name, SUM(payment.amount)
FROM category 
INNER JOIN film_category
ON category.category_id = film_category.category_id
INNER JOIN inventory
ON inventory.film_id = film_category.film_id
INNER JOIN rental 
ON rental.inventory_id = inventory.inventory_id
INNER JOIN payment 
ON payment.rental_id = rental.rental_id
GROUP BY category.category_id
ORDER BY SUM(payment.amount) DESC 
LIMIT 5
);

-- 8b. How would you display the view that you created in 8a?
SELECT * from top_5_grossrevenue_genres;

SHOW CREATE VIEW top_5_grossrevenue_genres;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.
DROP VIEW top_5_grossrevenue_genres;




