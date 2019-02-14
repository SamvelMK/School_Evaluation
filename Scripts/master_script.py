import sys
sys.path.insert(0, "C:/Users/mkhit/Desktop/UNFPA_2019/Private/")

from private import query_user_background, query_pretest_results, query_questions, config
from functions import etl
from datahandler import DataHandler

# Exrtact Data

if __name__ == '__main__':
    # etl = etl(config)

    # df_user = etl.query(query_user_background)
    # df_pre_test = etl.query(query_pretest_results)
    # df_questions = etl.query(query_questions)

    # # Transform Data
    # data = etl.long_wide(df_pre_test, df_questions).col_rename()

    # Load Data

    # print(data)

    handler = DataHandler(etl(config))
    