#SQL queries

# Поиск фильмов по ключевому слову
search_by_keyword_query = """
SELECT title, description
FROM film 
WHERE title LIKE %s OR description LIKE %s 
LIMIT 10;
"""

# SQL-запрос для поиска фильмов по жанру и году
search_by_genre_year_query = """
SELECT 
    f.title, 
    f.description, 
    f.release_year
FROM 
    film f
JOIN 
    film_category fc ON f.film_id = fc.film_id
JOIN 
    category c ON fc.category_id = c.category_id
WHERE 
    c.name = %s AND f.release_year = %s
LIMIT 10;
"""
