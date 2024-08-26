import mysql.connector
from local_settings import dbconfig
from query_templates import *


class MixinMySQLQuery:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def simple_select(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")

    def save_search_query(self, query, *params):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            #print(f"Saved query with params: {params}")
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")

    def is_exist_table(self, table_name):
        try:
            self.cursor.execute(get_tables_name_query, (table_name,))
            result = self.cursor.fetchone()
            return result is not None
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            return False


class MySQLConnection(MixinMySQLQuery):
    def __init__(self, dbconfig):
        super().__init__()
        self.dbconfig = dbconfig

    def __enter__(self):
        self.connection = mysql.connector.connect(**dbconfig)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def setup_database(self):
        if not self.is_exist_table('search_keywords_sv'):
            try:
                self.cursor.execute(create_search_keywords_table)
                self.connection.commit()
                print("Таблица 'search_keywords_sv' успешно создана.")
            except Exception as e:
                print(f"Ошибка при создании таблицы: {e}")
        #else:
        #    print("Таблица 'search_keywords_sv' уже существует.")


if __name__ == '__main__':
    with MySQLConnection(dbconfig) as db:
        # Проверка создания подключения
        db.cursor.execute('SELECT film_id, title, release_year FROM film LIMIT 1;')
        rows = db.cursor.fetchall()
        film_id, title, release_year = rows[0]
        release_year = int(release_year)

        # Вывод фактических данных для проверки
        print(f"Полученные данные: {rows[0]}")

        assert (film_id, title, release_year) == (
            1, 'ACADEMY DINOSAUR', 2013), "Error: The first film data does not match!"
        assert (film_id, title, release_year) != (2, 'ACADEMY DINOSAUR', 2013), "Error: Test data mismatch!"

        # Проверка метода .simple_select()
        keyword = '%ACADEMY%'
        rows = db.simple_select(search_by_keyword_query, (keyword, keyword))
        assert rows[0] == ('ACADEMY DINOSAUR',
                           'A Epic Drama of a Feminist And a Mad Scientist who must Battle a Teacher in The Canadian Rockies'), "Error: Film data does not match!"
        assert rows[0] != ('Some Other Film', 'Some Other Description'), "Error: Test data mismatch!"

        # Проверка метода .is_exist_table()
        is_exist = db.is_exist_table('search_keywords_sv')
        assert is_exist == True, "Error: Table 'search_keywords_sv' does not exist! Please create it."

        is_exist = db.is_exist_table('non_existing_table')
        assert is_exist == False, "Error: Table 'non_existing_table' should not exist!"

        print("Tests were passed successfully!")