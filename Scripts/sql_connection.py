import mysql.connector
import pandas as pd
from private import config

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# query_pretest = ("SELECT pts.user_id, pts.test_id, pts.answer, pts.time, pts.date, sch.region, sch.region, sch.community\
#             FROM pre_tests_res as pts\
#             JOIN schools as sch ON pts.id = sch.id")

query_user_info = ("SELECT id, sex, region, city, community, school, grade, current_grade, question_id, answer,  created_at, updated_at\
    FROM user")

query_pretest_results = ("SELECT user_id, test_id, answer, time, status, date\
    FROM pre_tests_res")

query_combined = ("SELECT pts.user_id, pts.test_id, pts.answer, pts.time, pts.status, pts.date, us.sex, us.region, us.city, us.community, us.school, us.grade, us.current_grade, us.question_id, us.answer,  us.created_at, us.updated_at\
                    FROM pre_tests_res pts, user us\
                    WHERE pts.user_id = us.id")

cursor.execute(query_user_info)

# Here I create a data frame with the user info. 
df_user = pd.DataFrame(cursor.fetchall())
df_user.columns = cursor.column_names

cursor.execute(query_pretest_results)
df_pre_test = pd.DataFrame(cursor.fetchall())
df_pre_test.columns = cursor.column_names

cursor.execute(query_combined)

df_combined = pd.DataFrame(cursor.fetchall())
df_combined.columns = cursor.column_names

print(df_user)
print(df_pre_test)
print(df_combined)

cursor.close()
cnx.close()