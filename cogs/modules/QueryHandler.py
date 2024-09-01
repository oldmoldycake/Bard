import mysql.connector
from mysql.connector import Error

class QueryHandler:
    def __init__(self, db_info):
        self.db_info = db_info

    def SQL(self, database, query, params=None):
        db_info = self.db_info.copy()
        db_info['database'] = database

        try:
            with mysql.connector.connect(**db_info) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params) if params else cursor.execute(query)

                    if query.strip().upper().startswith('SELECT'):
                        return cursor.fetchall()
                    else:
                        connection.commit()
                        return cursor.rowcount
        except Error as e:
            raise e

    def get_all_users(self):
        return self.SQL("bog_bot", "SELECT user_id, username FROM discord_users",)

    def get_username_by_user_id(self, user_id):
        return self.SQL("bog_bot", "SELECT username FROM discord_users WHERE user_id = %s", (user_id,),)

    def get_date_joined_by_user_id(self, user_id):
        return self.SQL("bog_bot", "SELECT date_joined FROM discord_users WHERE user_id = %s", (user_id,),)

    def get_user_id_by_username(self, username):
        return self.SQL("bog_bot", "SELECT user_id FROM discord_users WHERE username = %s", (username,),)

    def add_user(self, user_id, username):
        try:
            self.SQL('bog_bot', "INSERT INTO discord_users (user_id, username) VALUES (%s, %s)", (user_id, username,))
        except Exception as e:
            print(f"An error occurred: {e}")


