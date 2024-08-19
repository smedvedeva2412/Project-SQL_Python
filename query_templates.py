#SQL queries

# Поиск фильмов по ключевому слову
search_by_keyword_query = """
SELECT title, description
FROM film 
WHERE title LIKE %s OR description LIKE %s 
LIMIT 10;
"""

# SQL-запрос для поиска фильмов по жанру и году
search_by_genre_year_query = ("\n"
                              "SELECT \n"
                              "    f.title, \n"
                              "    f.description, \n"
                              "    f.release_year\n"
                              "FROM \n"
                              "    film f\n"
                              "JOIN \n"
                              "    film_category fc ON f.film_id = fc.film_id\n"
                              "JOIN \n"
                              "    category c ON fc.category_id = c.category_id\n"
                              "WHERE \n"
                              "    c.name = %s AND f.release_year = %s\n"
                              "LIMIT 10;\n")
