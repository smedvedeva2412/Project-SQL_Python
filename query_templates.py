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

# Создание таблицы для хранения поисковых запросов
create_search_keywords_table_query = """
CREATE TABLE IF NOT EXISTS search_keywords_sv (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) NOT NULL,
    search_count INT DEFAULT 1,
    last_search DATETIME DEFAULT NOW()
);
"""

# Сохранение поискового запроса или обновление счетчика и времени поиска
save_search_query = """
INSERT INTO search_keywords_sv (keyword, search_count)
VALUES (%s, 1)
ON DUPLICATE KEY UPDATE search_count = search_count + 1, last_search = NOW();
"""
