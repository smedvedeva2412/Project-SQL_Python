from prettytable import PrettyTable

from local_settings import dbconfig
from mysql_manager import MySQLConnection
from query_templates import (
    search_by_keyword_query, search_by_genre_query, search_by_genre_and_years_query, search_movies_by_year_query,
    get_popular_keywords_query, get_popular_genres_query, get_categories_query,
    save_search_keyword_query
)


def get_categories(db):
    categories = db.simple_select(get_categories_query)
    return [category[0] for category in categories]


def search_movies_by_genre(db, genre):
    result = db.simple_select(search_by_genre_query, (genre,))
    return result


def search_movies_by_year(db, year):
    result = db.simple_select(search_movies_by_year_query, (year,))
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
        print("К сожалению, мы не нашли запросов по указанным ключевым словам.")


def display_popular_genres(db):
    result = db.simple_select(get_popular_genres_query)
    if result:
        print("Ловите популярные запросы по жанрам и годам:")
        for idx, search in enumerate(result, start=1):
            print(f"{idx}. {search[0]} - {search[1]} раз(а)")
    else:
        print("К сожалению, мы не нашли запросов по указанным жанрам и годам.")


def is_valid_year(year):
    try:
        year = int(year)
        return 1980 <= year <= 2023
    except ValueError:
        return False


def main():
    with MySQLConnection(dbconfig) as db:
        db.setup_database()

        while True:
            print("\n1. Поиск фильмов по ключевому слову")
            print("2. ТОП фильмов по популярности по жанру")
            print("3. ТОП фильмов по популярности по году")
            print("4. Показать популярные запросы")
            print("5. Выборка фильмов по выбранным годам и жанру")
            print("0. Выход")

            choice = input("\nВыберите действие (0-5): ")

            if choice == '1':
                # повторный ввод ключевого слова, если фильмы не найдены
                while True:
                    keyword = input("Введите ключевое слово для поиска: ")
                    result = search_movies_by_keyword(db, keyword)
                    if result:
                        # Создаем таблицу с заголовками "Название" и "Описание"
                        table = PrettyTable()
                        table.field_names = ["Название фильма", "Описание"]

                        for row in result:
                            title = row[0]
                            description = row[1]
                            table.add_row([title, description])

                        table.align = "l"
                        print(table)
                        break
                    else:
                        print("К сожалению, фильмы не найдены.")
                        retry_choice = input("Хотите попробовать снова? (да/нет): ").strip().lower()
                        if retry_choice != 'да':
                            break

            elif choice == '2':
                # 1. Получение списка жанров
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

                # 2. Вывод ТОП 10 фильмов по жанру
                result = search_movies_by_genre(db, selected_category)
                if result:
                    print(f"\nТОП 10 популярных фильмов по жанру '{selected_category}':")

                    table = PrettyTable()
                    table.field_names = ["Название фильма", "Год выхода"]

                    table.align["Название фильма"] = "l"
                    table.align["Год выхода"] = "l"

                    # Добавляем строки в таблицу
                    for row in result:
                        title = row[0]
                        year = row[3]
                        table.add_row([title, year])

                    print(table)
                else:
                    print("К сожалению, фильмы не найдены.")

            elif choice == '3':
                # ТОП популярных фильмов по году
                while True:
                    year = input("Введите год (например, 2000): ")
                    try:
                        int(year)
                        break
                    except ValueError:
                        print("Ошибка: пожалуйста, введите корректный год.")

                result = search_movies_by_year(db, year)
                if result:
                    print(f"\nТОП 10 популярных фильмов за {year}:")
                    table = PrettyTable()
                    table.field_names = ["Название фильма", "Рейтинг популярности"]

                    table.align["Название фильма"] = "l"
                    table.align["Рейтинг популярности"] = "l"

                    for row in result:
                        title = row[0]
                        rental_rate = row[2]
                        table.add_row([title, rental_rate])
                    print(table)
                else:
                    print(f"К сожалению, фильмы за {year} не найдены.")

            elif choice == '4':
                result_keywords = db.simple_select(get_popular_keywords_query)
                if result_keywords:
                    print("Популярные ключевые слова:")

                    keyword_table = PrettyTable()
                    keyword_table.field_names = ["№", "Ключевое слово", "Количество запросов"]
                    keyword_table.align = "l"

                    for idx, row in enumerate(result_keywords, start=1):
                        keyword = row[0]
                        count = row[1]
                        keyword_table.add_row([idx, keyword, count])
                    print(keyword_table)

                else:
                    print("К сожалению, запросов по ключевым словам не найдено.")
                result_genres = db.simple_select(get_popular_genres_query)
                if result_genres:
                    print("Популярные жанры и годы по запросам:")

                    genre_table = PrettyTable()
                    genre_table.field_names = ["№", "Жанр", "Год", "Количество запросов"]
                    genre_table.align = "l"

                    for idx, row in enumerate(result_genres, start=1):
                        genre = row[0]
                        year = row[1]
                        count = row[2]
                        genre_table.add_row([idx, genre, year, count])
                    print(genre_table)
                else:
                    print("К сожалению, запросов по жанрам не найдено.")

            elif choice == '5':
                while True:
                    year_input = input(
                        "Введите один год или несколько с 1980 по 2023 гг. через запятую (например: 2000, 2005, 2010): ")
                    years = year_input.split(',')
                    if all(is_valid_year(year.strip()) for year in years):
                        selected_years = [int(year.strip()) for year in years]
                        break
                    else:
                        print("Ошибка: пожалуйста, введите корректные годы в диапазоне от 1980 до 2023.")

                # Поиск ТОП популярных фильмов (по жанру и выбранным годам)
                while True:
                    categories = get_categories(db)
                    print("\nВыберите жанр из списка:")
                    for idx, category in enumerate(categories, start=1):
                        print(f"{idx}. {category}")

                    try:
                        category_choice = int(input("Укажите выбранный жанр (номер): ")) - 1
                        if category_choice < 0 or category_choice >= len(categories):
                            raise ValueError("Неверный номер жанра.")
                        selected_category = categories[category_choice]
                        break
                    except ValueError as e:
                        print(f"Ошибка: {e}. Пожалуйста, введите корректный номер жанра.")

                result = search_movies_by_genre_and_years(db, selected_category, selected_years)
                if result:
                    print(f"\nФильмы по жанру '{selected_category}' и выбранным годам:")

                    table = PrettyTable()
                    table.field_names = ["№", "Название фильма", "Год выхода"]
                    table.align["Название фильма"] = "l"
                    table.align["Год выхода"] = "l"

                    for idx, row in enumerate(result, start=1):
                        title = row[0]  # Название фильма
                        year = row[2]  # Год выпуска
                        table.add_row([idx, title, year])
                    print(table)
                else:
                    print("К сожалению, фильмы не найдены.")

            elif choice == '0':
                print("Выход из программы.")
                break

            else:
                print("Выберете цифру, соответствующую вашему запросу, и попробуйте снова.")


if __name__ == "__main__":
    main()
