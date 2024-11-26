from lyvia_backend.db.connection import DbConnection
from lyvia_backend.db.query.table import TableQueries


class Query:
    def __init__(self):
        self.connection = DbConnection()
        self._tables = TableQueries(self.connection)

        self._tables.create_user_table()
        self._tables.create_token_table()
