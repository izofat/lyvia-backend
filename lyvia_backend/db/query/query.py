from datetime import datetime

from lyvia_backend.db.connection import DbConnection
from lyvia_backend.db.query.insert import InsertQueries
from lyvia_backend.db.query.table import TableQueries


class Query:
    def __init__(self):
        self.connection = DbConnection()
        self._tables = TableQueries(self.connection)
        self._insert = InsertQueries(self.connection)
        self._tables.create_user_table()
        self._tables.create_token_table()

    def register_account(
        self, username: str, password: str, name: str, lastName: str, email: str
    ):
        return self._insert.register_account(username, password, name, lastName, email)

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        return self._insert.insert_token(user_id, jwt_token, jwt_expire_date)
