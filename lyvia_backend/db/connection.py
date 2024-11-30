import mysql.connector

from settings import MySqlConfig


class DbConnection:
    _instance = None
    _pool = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config=MySqlConfig):
        if DbConnection._initialized:
            return

        if DbConnection._pool is None:
            DbConnection._pool = mysql.connector.pooling.MySQLConnectionPool(
                host=config.HOST,
                port=config.PORT,
                user=config.USER,
                password=config.PASSWORD,
                database=config.DATABASE,
                pool_name=config.POOL_NAME,
                pool_size=config.POOL_SIZE,
                charset="utf8mb4",
                collation="utf8mb4_unicode_ci",
            )
        self.conn = None
        DbConnection._initialized = True

    def __enter__(self):
        self.conn = DbConnection._pool.get_connection()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            if self.conn.is_connected():
                self.conn.close()
            self.conn = None
