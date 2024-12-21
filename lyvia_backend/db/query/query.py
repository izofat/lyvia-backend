from datetime import datetime

from lyvia_backend.db.connection import DbConnection
from lyvia_backend.db.query.insert import InsertQueries
from lyvia_backend.db.query.select import SelectQueries
from lyvia_backend.db.query.table import TableQueries


class Query:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if Query._initialized:
            return

        self.connection = DbConnection()
        self._tables = TableQueries(self.connection)
        self._insert = InsertQueries(self.connection)
        self._select = SelectQueries(self.connection)

        self._tables.create_email_table()
        self._tables.create_user_table()
        self._tables.create_token_table()

        Query._initialized = True

    def register_account(
        self, username: str, password: str, name: str, lastName: str, email: str
    ):
        return self._insert.register_account(username, password, name, lastName, email)

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        return self._insert.insert_token(user_id, jwt_token, jwt_expire_date)

    def get_user(self, username: str):
        return self._select.get_user(username)

    def get_token(self, user_id: int):
        return self._select.get_token(user_id)
