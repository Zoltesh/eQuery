"""
An object to manage db connection and run queries
"""
import logging
import os

import keyring
import pyodbc


class Queryer:
    """
    A class to execute queries
    """
    def __init__(self):
        # Credentials for connecting to the db
        self.db_server = keyring.get_password("database", "ip_address")
        self.db_database = keyring.get_password("database", "database_name")
        self.db_username = keyring.get_password("database", "database_user")
        self.db_password = keyring.get_password("database", "database_pass")

        # Make sure to use the same DRIVER on your machine
        connection_string = (f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                             f"SERVER={self.db_server};"
                             f"DATABASE={self.db_database};"
                             f"UID={self.db_username};"
                             f"PWD={self.db_password};"
                             f"TrustServerCertificate=yes;")

        # Set up logging
        self.logger_name = os.path.basename(__file__).split(".")[0]
        self.logger = logging.getLogger(self.logger_name)
        self.logger.setLevel(logging.INFO)

        # Try connecting to the database
        try:
            self.conn = pyodbc.connect(connection_string)
        except pyodbc.OperationalError as poe:
            self.logger.error("Could not connect to the database. Check ODBC Driver and server"
                              " details. Error: %s", poe)

    def close_connection(self):
        """
        Close connection to the database
        """
        if self.conn:
            try:
                self.conn.close()
            except Exception as e:
                self.logger.error("Failed to close db connection with exception: %s", e)

    def execute_query(self, query):
        """
        Execute a user provided query and return the result
        :param query: User provided query
        :return: The result of the query
        """
        # Try creating the cursor
        try:
            cursor = self.conn.cursor()
        except AttributeError as ae:
            self.logger.error("Could not create cursor. Error: %s", str(ae))
            raise ae

        # Try executing the query
        try:
            cursor.execute(query)
            result = str(cursor.fetchall())
            self.logger.info("Successfully executed sql query: %s", query)
            return result
        except Exception as e:
            self.logger.error("Failed to execute query with exception: %s \n Query: %s", str(e),
                              query)
            raise e
