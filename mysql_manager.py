import mysql.connector
from local_settings import dbconfig
from query_templates import *


class MixinMySQLQuery:
    def simple_select(self, query, value):
        if self.is_exist_table(get_tables_name_query, value):

            try:
                self.cursor.execute(query.format(value))
                rows = self.cursor.fetchall()
                return rows

            except Exception as e:
                print(f"{e.__class__.__name__}: {e}")

    def is_exist_table(self, get_tables_name_query, table_name) -> bool:
        try:
            query = get_tables_name_query.format(table_name)
            self.cursor.execute(query)
            result = list(self.cursor)
            if not result:
                print(f"Тhe table <{table_name}> does not exist!")
                return False
            return True

        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")


class MySQLConnection(MixinMySQLQuery):
    def __init__(self, dbconfig):
        self.dbconfig = dbconfig
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = mysql.connector.connect(**dbconfig)
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.cursor:
            self.connection.close()


if __name__ == '__main__':
    with MySQLConnection(dbconfig) as db:

        # 1. Проверка создания подключения
        db.cursor.execute('SELECT * FROM Users;')
        rows = db.cursor.fetchall()
        assert rows[0] == (1, 'John Doe', 30), "Error!"
        assert rows[0] != (11, 'John Doe', 30), "Error!"

        # 2. Проверка метода .simple_select()
        rows = db.simple_select(s_query, 'Users')
        assert rows[0] == (1, 'John Doe', 30), "Error!"
        assert rows[0] != (11, 'John Doe', 30), "Error!"

        # 3. Проверка метода .is_exist_table()
        # 3.1 если имя таблицы существует
        is_exist = db.is_exist_table(get_tables_name_query, 'Users')
        assert is_exist == True, "Error!"

        # 3.2 если имя таблицы НЕ существует
        is_exist = db.is_exist_table(get_tables_name_query, 'Users1')
        assert is_exist == False, "Error!"

        print("Тесты успешно прошли!")