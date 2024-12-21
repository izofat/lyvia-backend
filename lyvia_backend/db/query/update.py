from lyvia_backend.db.query.base import BaseQuery


class UpdateQueries(BaseQuery):
    def verify_email(self, email: str):
        query = """
            UPDATE email
            SET isVerified = TRUE, verifiedAt = NOW()
            WHERE email = %s
        """
        return self.execute_query(query, email, is_commit=True)
