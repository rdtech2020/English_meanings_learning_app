import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('guess_data.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute('PRAGMA foreign_keys = ON')

    def create_table(self, table_name, fields):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})")
        self.conn.commit()
        print(f"Table {table_name} created successfully!!")

    def create_ques_table(self, table_name, fields):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})")
        self.conn.commit()
        print(f"Table {table_name} created successfully!!")

    def create_contact_table(self, table_name, fields):
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({fields})")
        self.conn.commit()
        print(f"Table {table_name} created successfully!!")

    def insert_user(self, username, password):
        hashed_password = generate_password_hash(password)
        self.cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        self.conn.commit()

    def check_user(self, username, password):
        self.cur.execute("SELECT id, password FROM users WHERE username=?", (username,))
        user = self.cur.fetchone()
        if user and check_password_hash(user[1], password):
            return user[0]
        else:
            return None

    def exist_user(self, username):
        self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
        result = self.cur.fetchone()
        if result:
            return False
        else:
            return True

    def insert_question(self, username, user_id, number, status, word):
        self.cur.execute("SELECT * FROM users WHERE username=?", (username,))
        result = self.cur.fetchone()
        if result:
            self.cur.execute("INSERT INTO questions (user, number, status, word) VALUES (?, ?, ?, ?)", (user_id, number, status, word))
            self.conn.commit()
            return True
        else:
            return False

    def get_ques_num(self, user_id):
        self.cur.execute(f"SELECT max(number) FROM questions WHERE user = {user_id};")
        result = self.cur.fetchone()
        if result[0] is None:
            return 1
        else:
            val = result[0] + 1
            return val

    def get_score(self, user_id):
        right = self.cur.execute(f"SELECT COUNT(*) FROM questions WHERE user={user_id} AND status=1;").fetchone()[0]
        wrong = self.cur.execute(f"SELECT COUNT(*) FROM questions WHERE user={user_id} AND status=0;").fetchone()[0]
        return [right,wrong,right+wrong]

    def insert_contact(self, name, email, company, message):
        self.cur.execute("INSERT INTO contact (name, email, company, message) VALUES (?, ?, ?, ?)", (name, email, company, message))
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

# Create user Table in DB
# db = Database()
# db.create_table('users', 'id INTEGER PRIMARY KEY,username TEXT, password TEXT')
# Create question Table in DB
# db.create_ques_table('questions', 'id INTEGER PRIMARY KEY, user INTEGER, number INTEGER, status BOOL, word TEXT')
# create contact table
# db.create_contact_table('contact', 'id INTEGER PRIMARY KEY, name TEXT, email TEXT, company TEXT, message TEXT')
# db.close()
