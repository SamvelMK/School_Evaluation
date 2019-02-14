import mysql.connector
import pandas as pd
import numpy as np

 
# Functions and Methods

class etl:

        # This class includes three methods that allow connecting to SQL database, implement queries and data tranformation.
        # The query method requires one argument which is a string of SQL queries. The method implements
        # the query method returns the quried tables as pandas dataframe.
        # Long_wide method selects the specified columns in the dataframe and transforms it from long to wide format by assigning column
        # names as the columns it takes and the values as the columns of the values. The col_rename function then changes the column names
        # based on the question names based on tests_id column in the database and then merges the table with the rest of the data in the initial
        # dataframe. The df.long_wide() method should be followed by .col_rename() method. 

    def __init__(self, config):
        self.open_connection(config) 

    def open_connection(self, config):
        print("Opened connection to the database.")
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def query(self, query_input):
        # self.cursor.execute(query_input)
        # df = pd.DataFrame(self.cursor.fetchall())
        # df.columns = self.cursor.column_names
        # return df
        self.cursor.execute(query_input)
        return self.cursor


    def long_wide(self, df_test_res, df_questions):
        self.df_questions = df_questions

        temp = df_test_res.iloc[:, np.r_[:1, 7:9]]
        self.temp2 = df_test_res.drop_duplicates().iloc[:, :7]
        self.temp = temp.pivot(index = "id", columns = "test_id", values = "answer")
        return self

    def col_rename(self):
        dict_name = {}
        for key, value in zip(self.df_questions["id"], self.df_questions["question"]):
            dict_name.update({key : value})

        for i in list(self.temp.columns.values):
            for y in dict_name.keys():
                if i == y:
                    self.temp = self.temp.rename(columns = {i : dict_name[y]})
                else:
                    pass

        self.temp = pd.merge(self.temp2, self.temp,  on = "id" ).drop_duplicates()
        return self.temp

    def __del__(self):
        self.cursor.close()
        self.cnx.close()