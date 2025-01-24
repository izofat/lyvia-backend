from lyvia_backend.db.query.base import BaseQuery


class SelectQueries(BaseQuery):
    def get_user(self, username: str):
        query = """
            SELECT * FROM user WHERE username = %s 
        """
        return self.execute_query(query, username)

    def get_token(self, user_id: int):
        query = """
            SELECT id, userId, jwtToken, expireDate FROM token 
            WHERE userId = %s
            ORDER BY expireDate DESC
            LIMIT 1
        """
        return self.execute_query(query, user_id)

    def get_is_email_verified(self, email: str):
        query = """
            SELECT isVerified FROM email WHERE email = %s
        """
        return self.execute_query(query, email)
