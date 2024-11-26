from lyvia_backend.db.connection import DbConnection


class BaseQuery:  # pylint: disable=too-few-public-methods
    def __init__(self, connection: DbConnection):
        self._connection = connection

    def execute_query(self, query: str, *args, is_commit: bool = False):
        with self._connection as conn:
            cursor = conn.cursor(dictionary=True)

            try:
                cursor.execute(query, (*args,))
                if is_commit:
                    conn.commit()
                    return cursor.rowcount

                result = cursor.fetchall()
                return result

            except Exception as e:
                raise e
            finally:
                cursor.close()
