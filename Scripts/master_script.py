import sys
sys.path.insert(0, "C:/Users/mkhit/Desktop/UNFPA_2019/Private/")

from private import query_user_background, query_pretest_results, query_questions, config
from extract import extractor
from transform import DataTransform

# Extract, Transform, Load (ETL)

if __name__ == '__main__':
    
    etl = DataTransform(extractor(config))
    
    # handler.create_dataframe(query_user_background)
    etl.create_dataframe("results", query_pretest_results)
    etl.create_dataframe("questions", query_questions)
    
    result = etl.get_transformed("results", "questions")
    
