from mysql_manager import MySQLConnection
from query_templates import (
    search_by_keyword_query, search_by_genre_year_query, get_popular_keywords_query,
    get_popular_genres_query, get_categories_query,
    save_search_keyword_query, save_search_genre_year_query
)
from local_settings import dbconfig


def get_categories(db):
    categories = db.simple_select(get_categories_query)
    return [category[0] for category in categories]


def get_years_for_category(db, category_name):
    years = db.simple_select(get_years_for_category_query, (category_name,))
    return [year[0] for year in years]


def search_movies_by_genre_year(db, genre, year):
    result = db.simple_select(search_by_genre_year_query, (genre, year))
    db.save_search_query(save_search_genre_year_query, genre, year)
    return result


def search_movies_by_keyword(db, keyword):
    search_keyword = f'%{keyword}%'
    result = db.simple_select(search_by_keyword_query, (search_keyword, search_keyword))
    db.save_search_query(save_search_keyword_query, keyword)
    return result


def display_popular_keywords(db):
    result = db.simple_select(get_popular_keywords_query)
    if result:
        print("Популярные ключевые слова:")
        for idx, search in enumerate(result, start=1):
            print(f"{idx}. {search[0]} - {search[1]} раз(а)")
    else:
        print("Нет запросов по ключевым словам.")


def display_popular_genres(db):
    result = db.simple_select(get_popular_genres_query)
    if result:
        print("Популярные запросы по жанрам и годам:")
        for idx, search in enumerate(result, start=1):
            print(f"{idx}. {search[0]} - {search[1]} раз(а)")
    else:
        print("Нет запросов по жанрам и годам.")


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
                # 1. Получение списка категорий
                categories = get_categories(db)
                print("\nСписок категорий:")
                for idx, category in enumerate(categories, start=1):
                    print(f"{idx}. {category}")

                while True:
                    try:
                        category_choice = int(input("Выберите категорию (номер): ")) - 1
                        if category_choice < 0 or category_choice >= len(categories):
                            raise ValueError("Неверный номер категории.")
                        selected_category = categories[category_choice]
                        break
                    except ValueError as e:
                        print(f"Ошибка: {e}. Пожалуйста, введите корректный номер категории.")
                # 2. Выбор года
                while True:
                    year_input = input("Введите любой год с 1980 до 2023: ")
                    if year_input.isdigit():
                        selected_year = int(year_input)
                        break
                    else:
                        print("Ошибка: пожалуйста, введите корректный год в виде числа.")

                # 3. Поиск фильмов по выбранной категории и году
                result = search_movies_by_genre_year(db, selected_category, selected_year)
                if result:
                    for row in result:
                        print(row)
                else:
                    print("Фильмы не найдены.")

            elif choice == '3':
                # Показ популярных запросов
                popular_keywords: None = display_popular_keywords(db)
                if popular_keywords:
                    for idx, keyword in enumerate(popular_keywords, start=1):
                        print(f"{idx}. {keyword[0]} - {keyword[1]} раз(а)")

                        print("Нет популярных ключевых слов.")

                popular_genres = display_popular_genres(db)
                if popular_genres:
                    for idx, genre in enumerate(popular_genres, start=1):
                        print(f"{idx}. {genre[0]} - {genre[1]} раз(а)")

                        print("Нет популярных жанров.")

            elif choice == '4':
                print("Выход из программы.")
                break

            else:
                print("Выберете цифру, соответствующую вашему запросу, и попробуйте снова.")


if __name__ == "__main__":
    main()