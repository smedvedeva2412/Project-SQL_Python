from mysql_manager import MySQLConnection
from query_templates import (
    search_by_keyword_query, search_by_genre_query, search_by_genre_and_years_query,
    get_popular_keywords_query, get_popular_genres_query, get_categories_query,
    save_search_keyword_query, save_search_genre_year_query
)
from local_settings import dbconfig


def get_categories(db):
    categories = db.simple_select(get_categories_query)
    return [category[0] for category in categories]


def search_movies_by_genre(db, genre):
    result = db.simple_select(search_by_genre_query, (genre,))
    return result


def search_movies_by_genre_and_years(db, genre, years):
    query = search_by_genre_and_years_query.format(','.join(['%s'] * len(years)))
    result = db.simple_select(query, (genre, *years))
    return result


def search_movies_by_keyword(db, keyword):
    search_keyword = f'%{keyword}%'
    result = db.simple_select(search_by_keyword_query, (search_keyword, search_keyword))
    db.save_search_query(save_search_keyword_query, keyword)
    return result


def display_popular_keywords(db):
    result = db.simple_select(get_popular_keywords_query)
    if result:
        print("Вот популярные ключевые слова:")
        for idx, search in enumerate(result, start=1):
            print(f"{idx}. {search[0]} - {search[1]} раз(а)")
    else:
        print("К сожалению, мы не нашли запросов по ключевым словам.")


def display_popular_genres(db):
    result = db.simple_select(get_popular_genres_query)
    if result:
        print("Лови популярные запросы по жанрам и годам:")
        for idx, search in enumerate(result, start=1):
            print(f"{idx}. {search[0]} - {search[1]} раз(а)")
    else:
        print("К сожалению, мы не нашли запросов по указанным жанрам и годам.")


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
                    print("К сожалению, фильмы не найдены.")

            elif choice == '2':
                # 1. Получение списка категорий (жанров)
                categories = get_categories(db)
                print("\nСписок жанров:")
                for idx, category in enumerate(categories, start=1):
                    print(f"{idx}. {category}")

                while True:
                    try:
                        category_choice = int(input("Выберите жанр (номер): ")) - 1
                        if category_choice < 0 or category_choice >= len(categories):
                            raise ValueError("Неверный номер жанра.")
                        selected_category = categories[category_choice]
                        break
                    except ValueError as e:
                        print(f"Ошибка: {e}. Пожалуйста, введите корректный номер жанра.")

                # 2. Вывод всех фильмов по жанру
                result = search_movies_by_genre(db, selected_category)
                if result:
                    print(f"\nФильмы по жанру '{selected_category}':")
                    for row in result:
                        print(row)
                else:
                    print("К сожалению, фильмы не найдены.")

                # 3. Ввод годов для фильтрации
                while True:
                    year_input = input("Введите один или несколько лет с 1980 по 2023 гг. через запятую (например: 2000, 2005, 2010): ")
                    try:
                        selected_years = [int(year.strip()) for year in year_input.split(',')]
                        break
                    except ValueError:
                        print("Ошибка: пожалуйста, введите корректные годы.")

                # 4. Поиск фильмов по жанру и выбранным годам
                result = search_movies_by_genre_and_years(db, selected_category, selected_years)
                if result:
                    print("\nФильмы по жанру и годам:")
                    for row in result:
                        print(row)
                else:
                    print("К сожалению, фильмы не найдены.")

            elif choice == '3':
                # Показ популярных запросов
                display_popular_keywords(db)
                display_popular_genres(db)

            elif choice == '4':
                print("Выход из программы.")
                break

            else:
                print("Выберете цифру, соответствующую вашему запросу, и попробуйте снова.")


if __name__ == "__main__":
    main()