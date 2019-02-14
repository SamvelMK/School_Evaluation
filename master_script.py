from private import query_user_background, query_pretest_results, query_questions
from functions import etl

# Exrtact Data

etl = etl()

df_user = etl.query(query_user_background)
df_pre_test = etl.query(query_pretest_results)
df_questions = etl.query(query_questions)

# Transform Data
data = etl.long_wide(df_pre_test, df_questions).col_rename()

# Load Data

print(data)