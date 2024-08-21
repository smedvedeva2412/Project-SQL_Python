from mysql_manager import MySQLConnection
from query_templates import search_by_keyword_query, search_by_genre_year_query, get_popular_queries
from local_settings import dbconfig


def search_movies_by_keyword(db, keyword):
    search_keyword = f'%{keyword}%'
    result = db.simple_select(search_by_keyword_query, (search_keyword, search_keyword))
    db.save_search_query(keyword)
    return result


def search_movies_by_genre_year(db, genre, year):
    result = db.simple_select(search_by_genre_year_query, (genre, year))
    db.save_search_query(f"Genre: {genre}, Year: {year}")
    return result


def display_popular_searches(db):
    result = db.simple_select(get_popular_queries)
    return result


def main():
    with MySQLConnection(dbconfig) as db:
        db.setup_database()

        while True:
            print("\n1. Поиск фильмов по ключевому слову")
            print("2. Поиск фильмов по жанру и году")
            print("3. Показать популярные запросы")
            print("4. Выход")

            choice = input("\nВыберите действие (1-4): ")

            if choice == '1':
                keyword = input("Введите ключевое слово для поиска: ")
                result = search_movies_by_keyword(db, keyword)
                if result:
                    for row in result:
                        print(row)
                else:
                    print("Фильмы не найдены.")

            elif choice == '2':
                genre = input("Введите жанр: ")
                year = input("Введите год: ")
                try:
                    year = int(year)  # Год должен быть числом
                    result = search_movies_by_genre_year(db, genre, year)
                    if result:
                        for row in result:
                            print(row)
                    else:
                        print("Фильмы не найдены.")
                except ValueError:
                    print("Год должен быть числом!")

            elif choice == '3':
                popular_searches = display_popular_searches(db)
                if popular_searches:
                    print("Популярные запросы:")
                    for idx, search in enumerate(popular_searches, start=1):
                        print(f"{idx}. {search[0]} - {search[1]} раз(а)")
                else:
                    print("Нет популярных запросов.")

            elif choice == '4':
                print("Выход из программы.")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()