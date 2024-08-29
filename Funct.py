
def get_categories(db, get_categories_query):
    categories = db.simple_select(get_categories_query)
    return [category[0] for category in categories]


def search_movies_by_genre(db, genre, search_by_genre_query):
    result = db.simple_select(search_by_genre_query, (genre,))
    return result


def search_movies_by_year(db, year, search_movies_by_year_query):
    result = db.simple_select(search_movies_by_year_query, (year,))
    return result


def search_movies_by_genre_and_years(db, genre, years, search_by_genre_and_years_query):
    query = search_by_genre_and_years_query.format(','.join(['%s'] * len(years)))
    result = db.simple_select(query, (genre, *years))
    return result


def search_movies_by_keyword(db, keyword, search_by_keyword_query, save_search_keyword_query):
    search_keyword = f'%{keyword}%'
    result = db.simple_select(search_by_keyword_query, (search_keyword, search_keyword))
    db.save_search_query(save_search_keyword_query, keyword)
    return result


def display_popular_keywords(db, get_popular_keywords_query):
    result = db.simple_select(get_popular_keywords_query)
    if result:
        print("Вот популярные ключевые слова:")
        for idx, search in enumerate(result, start=1):
            print(f"{idx}. {search[0]} - {search[1]} раз(а)")
    else:
        print("К сожалению, мы не нашли запросов по указанным ключевым словам.")


def display_popular_genres(db, get_popular_genres_query):
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
