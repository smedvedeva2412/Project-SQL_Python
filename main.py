from mysql_manager import MySQLConnection
from query_templates import (search_by_keyword_query, search_by_genre_year_query, get_popular_queries,
                             get_years_for_category_query, get_categories_query)
from local_settings import dbconfig


def get_categories(db):
    categories = db.simple_select(get_categories_query)
    return [category[0] for category in categories]


def get_years_for_category(db, category_name):
    years = db.simple_select(get_years_for_category_query, (category_name,))
    return [year[0] for year in years]


def search_movies_by_genre_year(db, genre, year):
    result = db.simple_select(search_by_genre_year_query, (genre, year))
    db.save_search_query(f"Genre: {genre}, Year: {year}")
    return result


def search_movies_by_keyword(db, keyword):
    search_keyword = f'%{keyword}%'
    result = db.simple_select(search_by_keyword_query, (search_keyword, search_keyword))
    db.save_search_query(keyword)
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
                # 1. Получение списка категорий
                categories = get_categories(db)
                print("\nСписок категорий:")
                for idx, category in enumerate(categories, start=1):
                    print(f"{idx}. {category}")

                category_choice = int(input("Выберите категорию (номер): ")) - 1
                selected_category = categories[category_choice]

                # 2. Получение доступных годов для выбранной категории
                years = get_years_for_category(db, selected_category)
                print(f"Доступные годы для категории '{selected_category}':")
                for idx, year in enumerate(years, start=1):
                    print(f"{idx}. {year}")

                year_choice = int(input("Выберите год (номер): ")) - 1
                selected_year = years[year_choice]

                # 3. Поиск фильмов по выбранной категории и году
                result = search_movies_by_genre_year(db, selected_category, selected_year)
                if result:
                    for row in result:
                        print(row)
                else:
                    print("Фильмы не найдены.")

            elif choice == '3':
                popular_searches = display_popular_searches(db)
                if popular_searches:
                    print("Популярные запросы:")
                    for idx, search in enumerate(popular_searches, start=1):
                        print(f"{idx}. {search[0]} - {search[1]} раз(а)")
                else:
                    print("Нет запросов.")

            elif choice == '4':
                print("Выход из программы.")
                break

            else:
                print("Фильмов с этим ключевым словом нет. Попробуйте снова.")


if __name__ == "__main__":
    main()
