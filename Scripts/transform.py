import pandas as pd
import numpy as np

class DataTransform:
    """Class to handle construction of data frames from mysql and data transformation."""

    def __init__(self, extract):
        self.extract = extract
        self.dfs = {}
    
    def create_dataframe(self, name, query):
        df = pd.DataFrame(self.extract.query(query))
        df.columns = self.extract.get_column_names()
        self.dfs[name] = df

    def transform(self, name):
        first_subset = self.dfs[name].iloc[:, np.r_[:1, 7:9]]
        second_subset = self.dfs[name].iloc[:, :7].drop_duplicates()
        first_subset = self.dfs[name].pivot(index = "id", columns = "test_id", values = "answer")
        self.dfs["merged"] = pd.merge(second_subset, first_subset,  on = "id")
        self.dfs["subset"] = first_subset

    def col_rename(self, name):
        dict_name = {}
        for key, value in zip(self.dfs[name]["id"], self.dfs[name]["question"]):
            dict_name.update({key : value})

        for i in list(self.dfs["subset"].columns.values):
            for y in dict_name.keys():
                if i == y:
                    self.dfs["merged"] = self.dfs["merged"].rename(columns = {i : dict_name[y]})

    def get_transformed(self, what_to_transform, what_to_rename):
        self.transform(what_to_transform)
        self.col_rename(what_to_rename)
        return self.dfs["merged"]