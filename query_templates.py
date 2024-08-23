# Поиск фильмов по ключевому слову
search_by_keyword_query = """
SELECT title, description
FROM film 
WHERE title LIKE %s OR description LIKE %s 
LIMIT 10;
"""

# Поиск фильмов по жанру и году
search_by_genre_year_query = """
SELECT f.title, c.name AS genre, f.release_year
FROM film f
LEFT JOIN film_category fc ON f.film_id = fc.film_id
LEFT JOIN category c ON fc.category_id = c.category_id
WHERE c.name = %s AND f.release_year = %s
ORDER BY f.release_year, c.name;
"""


# Получение списка категорий
get_categories_query = """
SELECT name FROM category;
"""

# Получение доступных годов для выбранной категории
get_years_for_category_query = """
SELECT DISTINCT f.release_year
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
WHERE c.name = %s
ORDER BY f.release_year;
"""


# Получение фильмов по выбранной категории и году
search_by_genre_year_query = """
SELECT f.title, c.name, f.release_year
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id
WHERE c.name = %s AND f.release_year = %s
ORDER BY f.title;
"""

# Создание таблицы для хранения поисковых запросов
create_search_keywords_table = """
CREATE TABLE IF NOT EXISTS search_keywords_sv (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) UNIQUE NOT NULL,
    search_count INT DEFAULT 1);
"""

# Проверка существования таблицы
get_tables_name_query = "SHOW TABLES LIKE %s;"

# Запрос для получения популярных запросов
get_popular_queries = """
SELECT keyword, search_count
FROM search_keywords_sv
ORDER BY search_count DESC
LIMIT 10;
"""

# Сохранение поискового запроса
save_search_query = """
INSERT INTO search_keywords_sv (keyword, search_count)
VALUES (%s, 1)
ON DUPLICATE KEY UPDATE search_count = search_count + 1;
"""
