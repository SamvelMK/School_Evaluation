import mysql.connector

class extractor:

    """ Class to create a connection with SQL database and run queries""" 
    def __init__(self, config):
        self.open_connection(config) 

    def open_connection(self, config):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def query(self, query_input):
        self.cursor.execute(query_input)        
        return self.cursor.fetchall()

    def get_column_names(self):
        return self.cursor.column_names

    def __del__(self):
        self.cursor.close()
        self.cnx.close()