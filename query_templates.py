# Поиск фильмов по ключевому слову
search_by_keyword_query = """
SELECT title, description
FROM film 
WHERE title LIKE %s OR description LIKE %s 
LIMIT 10;
"""

# Поиск фильмов по жанру
search_by_genre_query = """
SELECT f.title, c.name AS genre, f.release_year
FROM film f
LEFT JOIN film_category fc ON f.film_id = fc.film_id
LEFT JOIN category c ON fc.category_id = c.category_id
WHERE c.name = %s
ORDER BY f.release_year
LIMIT 10;
"""

# Поиск фильмов по жанру и годам
search_by_genre_and_years_query = """
SELECT f.title, c.name AS genre, f.release_year
FROM film f
LEFT JOIN film_category fc ON f.film_id = fc.film_id
LEFT JOIN category c ON fc.category_id = c.category_id
WHERE c.name = %s AND f.release_year IN ({})
ORDER BY f.release_year;
"""

# Получение списка категорий (жанров)
get_categories_query = """
SELECT name FROM category;
"""

# Создание таблицы для хранения поисковых запросов по ключевым словам
create_search_keywords_table = """
CREATE TABLE IF NOT EXISTS search_keywords_sv (
    id INT AUTO_INCREMENT PRIMARY KEY,
    keyword VARCHAR(255) UNIQUE NOT NULL,
    search_count INT DEFAULT 1,
    last_search DATETIME DEFAULT NOW());
"""

# Создание таблицы для хранения поисковых запросов по жанрам и годам
create_search_genre_year_table = """
CREATE TABLE IF NOT EXISTS search_genre_year_sv (
    id INT AUTO_INCREMENT PRIMARY KEY,
    genre VARCHAR(255),
    year INT,
    search_count INT DEFAULT 1,
    last_search DATETIME DEFAULT NOW());
"""

# Проверка существования таблицы
get_tables_name_query = "SHOW TABLES LIKE %s;"

# Запрос для получения популярных ключевых слов
get_popular_keywords_query = """
SELECT keyword, search_count
FROM search_keywords_sv
ORDER BY search_count DESC
LIMIT 10;
"""

# Запрос для получения популярных жанров и годов
get_popular_genres_query = """
SELECT CONCAT(genre, ', Year: ', year) AS genre_year, search_count
FROM search_genre_year_sv
ORDER BY search_count DESC
LIMIT 10;
"""

# Сохранение поискового запроса по ключевому слову
save_search_keyword_query = """
INSERT INTO search_keywords_sv (keyword, search_count, last_search)
VALUES (%s, 1, NOW())
ON DUPLICATE KEY UPDATE 
search_count = search_count + 1, 
last_search = NOW();
"""

# Сохранение поискового запроса по жанру и году
save_search_genre_year_query = """
INSERT INTO search_genre_year_sv (genre, year, search_count, last_search)
VALUES (%s, %s, 1, NOW())
ON DUPLICATE KEY UPDATE 
search_count = search_count + 1, 
last_search = NOW();
"""