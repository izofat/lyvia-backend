from lyvia_backend.db.connection import DbConnection
from lyvia_backend.db.query.insert import InsertQueries
from lyvia_backend.db.query.select import SelectQueries
from lyvia_backend.db.query.table import TableQueries
from lyvia_backend.db.query.update import UpdateQueries


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
        self._tables.create_email_table()
        self._tables.create_user_table()
        self._tables.create_token_table()

        self._insert = InsertQueries(self.connection)
        self._select = SelectQueries(self.connection)
        self._update = UpdateQueries(self.connection)

        Query._initialized = True

    @property
    def insert(self):
        return self._insert

    @property
    def select(self):
        return self._select

    @property
    def update(self):
        return self._update
