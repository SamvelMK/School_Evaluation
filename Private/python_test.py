# Methods

import mysql.connector
import pandas as pd
import numpy as np
from private import config, query_user_background, query_pretest_results, query_questions
from functions import query, long_wide, sql_close


class extract_data:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    def query(self, query_input):
        self.cursor.execute(query_input)
        df = pd.DataFrame(self.cursor.fetchall())
        df.columns = self.cursor.column_names
        return df
    
p = extract_data()

print(p.query(query_user_background))