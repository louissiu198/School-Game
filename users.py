from uuid import uuid4
from sqlite3 import connect, Row

class Users:
    def __init__(self, file_path: str = "./database/users.db") -> None:
        self.conn = connect(file_path)
        self.conn.row_factory = Row
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username text, password text, token text)")
    
    def update_table(self, data: dict = {}) -> None:
        self.cursor.execute("INSERT INTO users VALUES ('{}','{}','{}')".format(data["username"], data["password"], data["token"]))
        self.conn.commit()

    def create_session(self) -> str:
        while True:
            authorization_token = str(uuid4()).replace("-", "")
            if not self.check_db_item("token", authorization_token):
                return authorization_token

    def create_user(self, username: str = "testing", password: str = "12345678") -> bool:
        data = {
            "token": self.create_session(),
            "username": username, 
            "password": password, 
        }
        self.update_table(data)
        return data["token"]

    def check_db_item(self, item_name: str = "token", data_name: str = "...") -> bool:
        self.cursor.execute(f"SELECT COUNT(*) FROM users WHERE {item_name} = '{data_name}'")
        count = self.cursor.fetchone()[0]  
        return count > 0

    def fetch_account_info(self, username: str = "testing") -> dict:
        user_info: tuple = self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user_info != None:
            return dict(user_info)

    def fetch_account_token(self, token: str = "testing") -> dict:
        user_info: tuple = self.cursor.execute("SELECT * FROM users WHERE token = ?", (token,)).fetchone()
        if user_info != None:
            return dict(user_info)
    


