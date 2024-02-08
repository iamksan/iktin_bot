import psycopg2


class DatBase:
    def __init__(self):
        self.connection = psycopg2.connect(database='iktin',
                                           user='postgres',
                                           password='Miniminiralka1',
                                           host='localhost',
                                           port='5432')
        self.cursor = self.connection.cursor()

        query_users = '''SELECT EXISTS (SELECT relname FROM pg_class WHERE relname = 'users');'''
        self.cursor.execute(query_users)
        rows_claim = self.cursor.fetchone()
        if rows_claim[0] == False:
            create_table_query = '''CREATE TABLE users(
                                user_id bigint NOT NULL PRIMARY KEY,
                                username TEXT NOT NULL,
                                role varchar(5) DEFAULT user); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()
        query_claim = '''SELECT EXISTS (SELECT relname FROM pg_class WHERE relname = 'claim');'''
        self.cursor.execute(query_claim)
        rows_claim = self.cursor.fetchone()
        if rows_claim[0] == False:
            create_table_query = '''CREATE TABLE claim(
                                user_id bigint NOT NULL PRIMARY KEY,
                                username TEXT NOT NULL,
                                email text,
                                description text,
                                amount bigint,
                                photo text,
                                close_or_open varchar(3)); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()

    def add_user(self, data):
        with self.connection:
            self.data = data
            query = "INSERT INTO users (user_id, username, role) values (%s, %s, %s)"            
            self.cursor.executemany(query, [data])
            self.connection.commit()

    def get_user_role(self, user_id):
        self.cursor.execute(f"SELECT role FROM users WHERE user_id = {user_id}")
        user_role = self.cursor.fetchone()
        return user_role

    def get_user_id(self, user_id):
        self.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {user_id}")
        user_identifier = self.cursor.fetchall()
        return user_identifier

    def get_user_data(self):
        self.cursor.execute("SELECT * FROM users")
        users_data = self.cursor.fetchall()
        return users_data

    def add_claim(self, data):
        with self.connection:
            self.data = data
            query = "INSERT INTO claim (user_id, username, email, description, amount, photo, open_or_close) values (%s, %s, %s, %s, %s, %s, %s)"            
            self.cursor.executemany(query, [data])
            self.connection.commit()


db = DatBase()