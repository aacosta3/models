import sqlite3
import bcrypt

class User:

    def __init__(self, props):
        self.id = props.get('id')
        self.username = props.get('username')
        self.password_hash = props.get('password_hash')
        self.admin = props.get('admin')

    @staticmethod
    def find_by_username(username, db_conn):
        cursor = db_conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username=?", (username,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data)
        return None

    @staticmethod
    def signup(username, password, db_conn):
        errors = []
        success = False
        user = None

        existing_user = User.find_by_username(username, db_conn)
        
        if not username:
            errors.append('Username cannot be blank')
        elif existing_user:
            errors.append('Username already in use')
        
        if len(password) < 4:
            errors.append('Password must be at least four characters')
        
        if not errors:
            success = True
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor = db_conn.cursor()
            cursor.execute("INSERT INTO user (username, password_hash, admin) VALUES (?, ?, ?)", (username, hashed, 0))
            db_conn.commit()
            user = User.find_by_username(username, db_conn)

        return success, user, errors

    @staticmethod
    def login(username, password, db_conn):
        if not username or len(password) < 4:
            return None

        user = User.find_by_username(username, db_conn)
        if not user:
            return None
        
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user
        return None

# Usage example
# db_conn = sqlite3.connect('your_database_file.db')
# user = User.signup('username123', 'password123', db_conn)
# logged_in_user = User.login('username123', 'password123', db_conn)
