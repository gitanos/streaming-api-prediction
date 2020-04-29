from os import environ
import MySQLdb
from time import sleep


class SqlCursorContext():
    def __init__(self, db_connection: MySQLdb.Connection):
        self.connection = db_connection
        self._cursor = self.connection.cursor()  # type: MySQLdb.cursors.Cursor

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._cursor.close()

    def fetch_enumerator(self, query: str, params=None):
        self._cursor.execute(query, params)

    def rollback(self):
        self.connection.rollback()

    def commit(self):
        self.connection.commit()

    def fetch_all(self, query: str, params=None):
        """Gets rows of the database query
        """
        self._cursor.execute(query, params)
        return self._cursor.fetchall()

    def execute(self, query:str, params=None):
        """Execute a query and return the number of affected rows.
        """
        self._cursor.execute(query, params)
        return self._cursor.rowcount


class Database():
    """ Class to instantiate a database connection and define a cursor context to avoid loss of connectivity
        Calls SqlCursorContext to execute queries
    """

    def __init__(self, max_retries=10):
        self.MAX_RETRIES = max_retries
        self._connection = None  # type: MySQLdb.Connection
        self.establish_connection()

    def establish_connection(self):
        for i in range(self.MAX_RETRIES):
            try:
                self._connection = MySQLdb.connect(host='db', user=environ['MYSQL_USER'],
                                                   passwd=environ['MYSQL_PASSWORD'], db=environ['MYSQL_DATABASE'])
                break
            except MySQLdb._exceptions.OperationalError:
                retry_interval = 2 ** i
                print(f'Connection failed, retrying in: {retry_interval} seconds...')
                sleep(retry_interval)
        else:
            raise SystemError

    def set_autocommit(self, flag: bool):
        self._connection.autocommit = flag

    def contextual_cursor(self) -> SqlCursorContext:
        return SqlCursorContext(self._connection)
