import psycopg2


class DatBase:
    def __init__(self):
        self.connection = psycopg2.connect(database='iktin',
                                           user='postgres',
                                           password='Miniminiralka1',
                                           host='localhost',
                                           port='5432')
        self.cursor = self.connection.cursor()

        query_users = '''SELECT EXISTS (
            SELECT relname FROM pg_class WHERE relname = 'admins');'''
        self.cursor.execute(query_users)
        rows_claim = self.cursor.fetchone()
        if rows_claim[0] == False:
            create_table_query = '''CREATE TABLE admins(
                                admin_id BIGINT PRIMARY KEY,
                                adminname TEXT
                                ); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()

        query_users = '''SELECT EXISTS (
            SELECT relname FROM pg_class WHERE relname = 'users');'''
        self.cursor.execute(query_users)
        rows_claim = self.cursor.fetchone()
        if rows_claim[0] == False:
            create_table_query = '''CREATE TABLE users(
                                user_id BIGINT PRIMARY KEY,
                                username TEXT,
                                role TEXT DEFAULT user,
                                admin BIGINT
                                ); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()

        query_claim = '''SELECT EXISTS (
            SELECT relname FROM pg_class WHERE relname = 'invoices');'''
        self.cursor.execute(query_claim)
        rows_claim = self.cursor.fetchone()
        if rows_claim[0] == False:
            create_table_query = '''CREATE TABLE invoices(
                                invoice_number BIGINT,
                                user_id BIGINT,
                                username TEXT,
                                description TEXT,
                                weight TEXT,
                                dimensions TEXT,
                                sending_address TEXT,
                                receiving_address TEXT,
                                payment_method TEXT); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()

        query_claim = '''SELECT EXISTS (
            SELECT relname FROM pg_class WHERE relname = 'claims');'''
        self.cursor.execute(query_claim)
        rows_claim = self.cursor.fetchone()
        if rows_claim[0] == False:
            create_table_query = '''CREATE TABLE claims(
                                user_id BIGINT,
                                username TEXT,
                                invoice_number BIGINT,
                                email TEXT,
                                description TEXT,
                                amount TEXT,
                                photo_db TEXT,
                                admin_id BIGINT,
                                status TEXT); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()

        query_claim = '''SELECT EXISTS (
            SELECT relname FROM pg_class WHERE relname = 'calls');'''
        self.cursor.execute(query_claim)
        rows_claim = self.cursor.fetchone()
        if rows_claim[0] == False:
            create_table_query = '''CREATE TABLE calls(
                                user_id BIGINT PRIMARY KEY,
                                admin_id BIGINT,
                                status_admin TEXT
                                ); '''
            self.cursor.execute(create_table_query)
            self.connection.commit()

    def get_admis(self):
        self.cursor.execute("SELECT admin_id FROM admins")
        admins = self.cursor.fetchall()
        return admins

    def add_user(self, data):
        with self.connection:
            self.data = data
            query = """INSERT INTO users (user_id, username, role, admin)
            values (%s, %s, %s, %s)"""
            self.cursor.executemany(query, [data])
            self.connection.commit()

    def get_user_role(self, user_id):
        self.cursor.execute(f"""SELECT role
                            FROM users
                            WHERE user_id = {user_id}""")
        user_role = self.cursor.fetchone()
        return user_role

    def get_user_id(self, user_id):
        self.cursor.execute(f"""SELECT user_id
                            FROM users
                            WHERE user_id = {user_id}""")
        user_identifier = self.cursor.fetchall()
        return user_identifier

    def get_user_data(self):
        self.cursor.execute("SELECT * FROM users")
        users_data = self.cursor.fetchall()
        return users_data

    def find_user(self, user_id):
        self.cursor.execute(f"""SELECT EXISTS(SELECT user_id
                            FROM users
                            WHERE user_id = {user_id})""")
        rows_claim = self.cursor.fetchone()
        return rows_claim[0]

    def get_user_admin(self, user_id):
        self.cursor.execute(f"""SELECT admin
                            FROM users
                            WHERE user_id = {user_id}""")
        user_admin = self.cursor.fetchone()
        return user_admin

    def add_claim(self, data):
        with self.connection:
            self.data = data
            query = """INSERT INTO claims (
                user_id,
                username,
                invoice_number,
                email,
                description,
                amount,
                photo_db,
                admin_id,
                status) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.executemany(query, [data])
            self.connection.commit()

    def get_all_claim(self):
        self.cursor.execute("SELECT * FROM claims")
        claim_data = self.cursor.fetchall()
        return claim_data

    def get_open_claim(self, admin_id):
        self.cursor.execute(f"""SELECT * FROM claims
                            WHERE status = 'open' AND admin_id = {admin_id}""")
        claim_open_data = self.cursor.fetchall()
        return claim_open_data

    def add_invoice(self, data):
        with self.connection:
            self.data = data
            query = """INSERT INTO invoices (
                invoice_number,
                user_id,
                username,
                description,
                weight,
                dimensions,
                sending_address,
                receiving_address,
                payment_method)
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            self.cursor.executemany(query, [data])
            self.connection.commit()

    def count_invoice(self):
        self.cursor.execute("SELECT * FROM invoices")
        invoices_data = self.cursor.fetchall()
        return len(invoices_data)

    def get_all_invoice(self):
        self.cursor.execute("SELECT * FROM invoices")
        invoices_data = self.cursor.fetchall()
        return invoices_data

    def get_admin(self):
        self.cursor.execute("SELECT * FROM admins")
        admin_data = self.cursor.fetchall()
        return admin_data

    def add_call(self, data):
        with self.connection:
            self.data = data
            query = """INSERT INTO calls (
                user_id,
                admin_id,
                status_admin) values (%s, %s, %s)"""
            self.cursor.executemany(query, [data])
            self.connection.commit()

    def get_calls_admin(self, admin_id):
        self.cursor.execute(f"""SELECT * FROM calls
                            WHERE admin_id = {admin_id}
                            AND status_admin = 'open'""")
        calls_data = self.cursor.fetchall()
        return calls_data

    def del_call(self, user_id):
        with self.connection:
            self.cursor.execute(f"DELETE FROM calls WHERE user_id = {user_id}")
            self.connection.commit()


db = DatBase()
