from mysql_manager import MySQLConnection
from query_templates import search_by_keyword_query, search_by_genre_year_query
from local_settings import dbconfig


def search_by_keyword(db):
    keyword = input("Введите ключевое слово для поиска фильмов: ")
    keyword = f"%{keyword}%"
    result = db.simple_select(search_by_keyword_query, (keyword, keyword))

    if result:
        print("Найденные фильмы:")
        for row in result:
            print(f"Название: {row[0]}, Описание: {row[1]}")
    else:
        print("Фильмы по указанному ключевому слову не найдены.")

    db.save_search_query(f"Keyword search: {keyword}")





def main_menu():
    print("Добро пожаловать в программу поиска фильмов!")
    print("1. Поиск фильмов по ключевому слову")
    print("2. Поиск фильмов по жанру и году")
    print("3. Показать самые популярные запросы")
    print("0. Выход")

    choice = input("Выберите опцию: ")
    return choice
