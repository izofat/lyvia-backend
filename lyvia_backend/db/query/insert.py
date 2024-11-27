from datetime import datetime

from lyvia_backend.db.query.base import BaseQuery


class InsertQueries(BaseQuery):
    def register_account(
        self, username: str, password: str, name: str, lastName: str, email: str
    ):
        query = """
            INSERT IGNORE INTO user (username, password, name, lastName, email)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.execute_query(
            query, username, password, name, lastName, email, is_commit=True
        )

    def insert_token(self, user_id: int, jwt_token: str, jwt_expire_date: datetime):
        query = """
            INSERT INTO token (userId, jwtToken, expireDate)
            VALUES (%s, %s, %s)
        """
        return self.execute_query(
            query, user_id, jwt_token, jwt_expire_date, is_commit=True
        )
