import pandas as pd
import numpy as np

class DataHandler:
    """Class to handle construction of data frames from mysql."""

    def __init__(self, data):
        print("Created data handler.")
        self.data = data
    
    def create_dataframe(self, query):
        self.data.query(query)
        
        # df = pd.DataFrame(self.cursor.fetchall())
        # df.columns = self.cursor.column_names
        # return df
    
