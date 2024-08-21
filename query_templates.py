# Поиск фильмов по ключевому слову
search_by_keyword_query = """
SELECT title, description
FROM film 
WHERE title LIKE %s OR description LIKE %s 
LIMIT 10;
"""

# Поиск фильмов по жанру и году
search_by_genre_year_query = """
SELECT 
    f.title, 
    c.name AS genre, 
    f.release_year
FROM 
    film f
LEFT JOIN 
    film_category fc ON f.film_id = fc.film_id
LEFT JOIN 
    category c ON fc.category_id = c.category_id
WHERE
    c.name = %s AND f.release_year = %s
ORDER BY 
    f.release_year, c.name;
"""

get_categories_query = """
SELECT name FROM category;
"""

# Создание таблицы для хранения поисковых запросов
create_search_keywords_table = """
CREATE TABLE IF NOT EXISTS search_keywords_sv (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) UNIQUE NOT NULL,
    search_count INT DEFAULT 1,
    last_search DATETIME DEFAULT NOW()
);
"""

# Проверка существования таблицы
get_tables_name_query = "SHOW TABLES LIKE %s;"

# Запрос для получения популярных запросов
get_popular_queries = """
SELECT keyword, COUNT(*) AS search_count
FROM search_keywords_sv
GROUP BY keyword
ORDER BY search_count DESC
LIMIT 10;
"""

# Сохранение поискового запроса
save_search_query = """
INSERT INTO search_keywords_sv (keyword, search_count)
VALUES (%s, 1)
ON DUPLICATE KEY UPDATE search_count = search_count + 1, last_search = NOW();
"""