from lyvia_backend.db.query.base import BaseQuery


class TableQueries(BaseQuery):
    def create_user_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS user(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(25) NOT NULL,
                password VARCHAR(300) NOT NULL,
                name VARCHAR(100) NOT NULL,
                lastName VARCHAR(100) NOT NULL,
                email VARCHAR(254) NOT NULL,
                emailVerified BOOL NOT NULL DEFAULT FALSE,
                createdAt DATETIME DEFAULT NOW(),
                updatedAt DATETIME DEFAULT NOW()
            )
        """
        return self.execute_query(query)

    def create_token_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS token(
                id INT AUTO_INCREMENT PRIMARY KEY,
                userId INT NOT NULL,
                jwtToken VARCHAR(2000) NOT NULL,
                jwtExpireDate DATETIME NOT NULL,
                createdAt DATETIME DEFAULT NOW(),
                FOREIGN KEY (userId) REFERENCES user(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
            )
        """
        return self.execute_query(query)
