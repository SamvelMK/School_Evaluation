import pandas as pd
from config import connection_string, region_names, eight_grade_tests, eight_grade_attitude, nine_grade_tests, nine_grade_attitude, ten_grade_tests, ten_grade_attitude, eleven_grade_tests, eleven_grade_attitude, formtive_questions, formative_domain
from user import UserData
from test import TestData
from process_evaluation import ProcessEvaluationData

class Task:

    def __init__(self):
        pd.options.mode.chained_assignment = None

    def user(self):

        user_data = UserData(connection_string, region_names, trial = True)
        
        # User Data 
        user_data.user_info()
        user_data.user_aggregate_grade()
        user_data.user_aggregate_grade_region()

        user_data.write_to_csv('user', trial = True, **{'user' : user_data.user_table})
        TestData.write_to_xls('user', 'user_aggregate', trial = True,
                                        **{'user_region_agg' : user_data.user_aggr_grade,
                                            'user_region_agg_grade' : user_data.user_aggr_grade_region})
        user_data.write_info('user', user_data.user_info(), trial= True)
        
    # Test data eight grade
    def eight_grade(self):

        eight_grade = TestData(connection_string)
        eight_grade.query(8, region_names, trial = True)
        eight_grade.test_extract(eight_grade_tests, eight_grade_attitude)
        eight_grade.clean()

        # Knowledge Items
        eight_grade.knwl_aggregate_correct_region()
        eight_grade.knwl_aggregate_correct_reg_sex()
        eight_grade.knwl_aggregate_thematic()
        eight_grade.knwl_aggregate_thematic_reg()
        eight_grade.knwl_aggregate_thematic_sex()
        eight_grade.knwl_aggregate_thematic_reg_sex()

        # Attitude Items
        eight_grade.attd_mean_items_theme()
        eight_grade.attd_mean_items_theme_sex()
        eight_grade.attd_mean_items_theme_reg()
        eight_grade.attd_mean_items_theme_reg_sex()

        eight_grade_tests_dict = {'eight_grade_pre' : eight_grade.pre,
                                  'eight_grade_post' : eight_grade.post,
                                  'eight_grade_dropouts' : eight_grade.dropouts}

        eight_grade_aggr_dict = {'aggr_region' : eight_grade.test_aggr_region,
                                 'aggr_region_sex' : eight_grade.test_aggr_region_sex,
                                 'aggr_themaic' : eight_grade.test_aggr_tematic,
                                 'aggr_thematic_reg' : eight_grade.test_aggr_theme_reg,
                                 'aggr_thematic_reg_sex' : eight_grade.test_aggr_theme_reg_sex,
                                 'aggr_attd_theme' : eight_grade.attd_mean_theme,
                                 'aggr_attd_theme_reg' : eight_grade.attd_mean_theme_reg,
                                 'aggr_attd_theme_sex' : eight_grade.attd_mean_theme_sex,
                                 'aggr_attd_theme_reg_sex' : eight_grade.attd_mean_theme_reg_sex}

        eight_grade.write_to_csv('eight_grade', trial = True, **eight_grade_tests_dict)
        eight_grade.write_to_xls('eight_grade', 'eight_aggregate', trial = True, **eight_grade_aggr_dict)
        eight_grade.write_info('eight_grade', eight_grade.test_info(), trial=True)

    # Test data nine grade
    def nine_grade(self):

        nine_grade = TestData(connection_string)
        nine_grade.query(9, region_names, trial = True)
        nine_grade.test_extract(nine_grade_tests, nine_grade_attitude)
        nine_grade.clean()

        # Knowledge items
        nine_grade.knwl_aggregate_correct_region()
        nine_grade.knwl_aggregate_correct_reg_sex()
        nine_grade.knwl_aggregate_thematic()
        nine_grade.knwl_aggregate_thematic_reg()
        nine_grade.knwl_aggregate_thematic_sex()
        nine_grade.knwl_aggregate_thematic_reg_sex()

        # Attitude items
        nine_grade.attd_mean_items_theme()
        nine_grade.attd_mean_items_theme_sex()
        nine_grade.attd_mean_items_theme_reg()
        nine_grade.attd_mean_items_theme_reg_sex()

        nine_grade_tests_dict = {'nine_grade_pre' : nine_grade.pre,
                                 'nine_grade_post' : nine_grade.post,
                                 'nine_grade_dropouts' : nine_grade.dropouts}

        nine_grade_aggr_dict = {'aggr_region' : nine_grade.test_aggr_region,
                                 'aggr_region_sex' : nine_grade.test_aggr_region_sex,
                                 'aggr_themaic' : nine_grade.test_aggr_tematic,
                                 'aggr_thematic_reg' : nine_grade.test_aggr_theme_reg,
                                 'aggr_thematic_reg_sex' : nine_grade.test_aggr_theme_reg_sex,
                                 'aggr_attd_theme' : nine_grade.attd_mean_theme,
                                 'aggr_attd_theme_reg' : nine_grade.attd_mean_theme_reg,
                                 'aggr_attd_theme_sex' : nine_grade.attd_mean_theme_sex,
                                 'aggr_attd_theme_reg_sex' : nine_grade.attd_mean_theme_reg_sex}

        nine_grade.write_to_csv('nine_grade', trial = True, **nine_grade_tests_dict)
        nine_grade.write_to_xls('nine_grade', 'nine_aggregate', trial = True, **nine_grade_aggr_dict)
        nine_grade.write_info('nine_grade', nine_grade.test_info(), trial=True)

    # Test data ten grade
    def ten_grade(self):
    
        ten_grade = TestData(connection_string)
        ten_grade.query(10, region_names, trial = True)
        ten_grade.test_extract(ten_grade_tests, ten_grade_attitude)
        ten_grade.clean()

        # Knowledge items
        ten_grade.knwl_aggregate_correct_region()
        ten_grade.knwl_aggregate_correct_reg_sex()
        ten_grade.knwl_aggregate_thematic()
        ten_grade.knwl_aggregate_thematic_reg()
        ten_grade.knwl_aggregate_thematic_sex()
        ten_grade.knwl_aggregate_thematic_reg_sex()

        # Attitude items
        ten_grade.attd_mean_items_theme()
        ten_grade.attd_mean_items_theme_sex()
        ten_grade.attd_mean_items_theme_reg()
        ten_grade.attd_mean_items_theme_reg_sex()

        ten_grade_tests_dict = {'ten_grade_pre' : ten_grade.pre,
                                'ten_grade_post' : ten_grade.post,
                                'ten_grade_dropouts' : ten_grade.dropouts}

        ten_grade_aggr_dict = {'aggr_region' : ten_grade.test_aggr_region,
                               'aggr_region_sex' : ten_grade.test_aggr_region_sex,
                               'aggr_themaic' : ten_grade.test_aggr_tematic,
                               'aggr_thematic_reg' : ten_grade.test_aggr_theme_reg,
                               'aggr_thematic_reg_sex' : ten_grade.test_aggr_theme_reg_sex,
                               'aggr_attd_theme' : ten_grade.attd_mean_theme,
                               'aggr_attd_theme_reg' : ten_grade.attd_mean_theme_reg,
                               'aggr_attd_theme_sex' : ten_grade.attd_mean_theme_sex,
                               'aggr_attd_theme_reg_sex' : ten_grade.attd_mean_theme_reg_sex}
        
        ten_grade.write_to_csv('ten_grade', trial = True, **ten_grade_tests_dict)
        ten_grade.write_to_xls('ten_grade', 'ten_aggregate', trial = True, **ten_grade_aggr_dict)
        ten_grade.write_info('ten_grade', ten_grade.test_info(), trial=True)

    # Test data eleven grade
    def eleven_grade(self):

        eleven_grade = TestData(connection_string)
        eleven_grade.query(11, region_names, trial = True)
        eleven_grade.test_extract(eleven_grade_tests, eleven_grade_attitude)
        eleven_grade.clean()

        # Knowledge items
        eleven_grade.knwl_aggregate_correct_region()
        eleven_grade.knwl_aggregate_correct_reg_sex()
        eleven_grade.knwl_aggregate_thematic()
        eleven_grade.knwl_aggregate_thematic_reg()
        eleven_grade.knwl_aggregate_thematic_sex()
        eleven_grade.knwl_aggregate_thematic_reg_sex()

        # Attitude items
        eleven_grade.attd_mean_items_theme()
        eleven_grade.attd_mean_items_theme_sex()
        eleven_grade.attd_mean_items_theme_reg()
        eleven_grade.attd_mean_items_theme_reg_sex()

        eleven_grade_tests_dict = {'eleven_grade_pre' : eleven_grade.pre,
                                   'eleven_grade_post' : eleven_grade.post,
                                   'eleven_grade_dropouts' : eleven_grade.dropouts}

        eleven_grade_aggr_dict = {'aggr_region' : eleven_grade.test_aggr_region,
                                  'aggr_region_sex' : eleven_grade.test_aggr_region_sex,
                                  'aggr_themaic' : eleven_grade.test_aggr_tematic,
                                  'aggr_thematic_reg' : eleven_grade.test_aggr_theme_reg,
                                  'aggr_thematic_reg_sex' : eleven_grade.test_aggr_theme_reg_sex,
                                  'aggr_attd_theme' : eleven_grade.attd_mean_theme,
                                  'aggr_attd_theme_reg' : eleven_grade.attd_mean_theme_reg,
                                  'aggr_attd_theme_sex' : eleven_grade.attd_mean_theme_sex,
                                  'aggr_attd_theme_reg_sex' : eleven_grade.attd_mean_theme_reg_sex}

        eleven_grade.write_to_csv('eleven_grade', trial = True, **eleven_grade_tests_dict)
        eleven_grade.write_to_xls('eleven_grade', 'eleven_aggregate', trial = True, **eleven_grade_aggr_dict)
        eleven_grade.write_info('eleven_grade', eleven_grade.test_info(), trial=True)

    # Process evaluation global
    def process_evaluation_global(self):

        transitions = ProcessEvaluationData(connection_string)
        transitions.transitions_global(trial = True)
        transitions.write_to_xls('user', 'transitions', trial = True, **{'transitions_reg' :  transitions.transition_glb_reg,
                                                                          'transitions_reg_sex' : transitions.transition_glb_reg_sex,
          
                                                                          'transitions_grade' :  transitions.transition_glb_grade,
                                                                          'transitions_grade_region' : transitions.transition_glb_grade_region,
                                                                          'transitions_grade_region_sex' : transitions.transition_glb_grade_region_sex,

                                                                          'transitions_time_reg' : transitions.transition_time_reg,
                                                                          'transitions_time_reg_sex' : transitions.transition_time_reg_sex,
                                                                          
                                                                          'transitions_time_grade' : transitions.transition_time_grade,
                                                                          'transitions_time_grade_reg' : transitions.transition_time_grade_region,
                                                                          'transitions_time_grade_reg_sex' : transitions.transition_time_grade_region_sex,

                                                                          'test_time_reg' : transitions.test_time_reg,
                                                                          'test_time_reg_sex' : transitions.test_time_reg_sex,
          
                                                                          'test_time_grade' : transitions.test_time_grade,
                                                                          'test_time_grade_region' : transitions.test_time_grade_region,
                                                                          'test_time_grade_region_sex' : transitions.test_time_grade_region_sex})

    # Process evaluation eight grade
    def frm_eight_grade(self):

        formative_eight = ProcessEvaluationData(connection_string)
        formative_eight.query(8, region_names, trial = True)
        formative_eight.extract(formtive_questions['evaluation_items'], formtive_questions['comments_recommendations'])
        formative_eight.clean(formative_domain)

        formative_eight.aggregate_topic()
        formative_eight.aggregate_topic_sex()
        formative_eight.aggregate_topic_region()
        formative_eight.aggregate_topic_region_sex()

        formative_eight_aggr_dict = {'formative_aggregate_topic' : formative_eight.aggr_topic,
                                     'formative_aggr_topic_sex' : formative_eight.aggr_topic_sex,
                                     'formative_aggr_topic_reg' : formative_eight.aggr_topic_reg,
                                     'formative_aggr_topic_reg_sex' : formative_eight.aggr_topic_reg_sex}

        formative_eight.write_to_csv('eight_grade', trial = True, **{'Comments' : formative_eight.formative_comment_data})
        formative_eight.write_to_xls('eight_grade', 'eight_aggregate', trial = True, **formative_eight_aggr_dict)
    
    # Process evaluation nine grade
    def frm_nine_grade(self):

        formative_nine = ProcessEvaluationData(connection_string)
        formative_nine.query(9, region_names, trial = True)
        formative_nine.extract(formtive_questions['evaluation_items'], formtive_questions['comments_recommendations'])
        formative_nine.clean(formative_domain)

        formative_nine.aggregate_topic()
        formative_nine.aggregate_topic_sex()
        formative_nine.aggregate_topic_region()
        formative_nine.aggregate_topic_region_sex()

        formative_nine_aggr_dict = {'formative_aggregate_topic' : formative_nine.aggr_topic,
                                    'formative_aggr_topic_sex' : formative_nine.aggr_topic_sex,
                                    'formative_aggr_topic_reg' : formative_nine.aggr_topic_reg,
                                    'formative_aggr_topic_reg_sex' : formative_nine.aggr_topic_reg_sex}

        formative_nine.write_to_csv('nine_grade', trial = True, **{'Comments' : formative_nine.formative_comment_data})
        formative_nine.write_to_xls('nine_grade', 'nine_aggregate', trial = True,  **formative_nine_aggr_dict)

    # Process evaluation ten grade
    def frm_ten_grade(self):
        formative_ten = ProcessEvaluationData(connection_string)
        formative_ten.query(10, region_names, trial = True)
        formative_ten.extract(formtive_questions['evaluation_items'], formtive_questions['comments_recommendations'])
        formative_ten.clean(formative_domain)

        formative_ten.aggregate_topic()
        formative_ten.aggregate_topic_sex()
        formative_ten.aggregate_topic_region()
        formative_ten.aggregate_topic_region_sex()

        formative_ten_aggr_dict = {'formative_aggregate_topic' : formative_ten.aggr_topic,
                                    'formative_aggr_topic_sex' : formative_ten.aggr_topic_sex,
                                    'formative_aggr_topic_reg' : formative_ten.aggr_topic_reg,
                                    'formative_aggr_topic_reg_sex' : formative_ten.aggr_topic_reg_sex}
        
        formative_ten.write_to_csv('ten_grade', trial = True, **{'Comments' : formative_ten.formative_comment_data})
        formative_ten.write_to_xls('ten_grade', 'ten_aggregate', trial = True, **formative_ten_aggr_dict)

    # Process evaluation eleven grade
    def frm_eleven_grade(self):
        
        formative_eleven = ProcessEvaluationData(connection_string)
        formative_eleven.query(11, region_names, trial = True)
        formative_eleven.extract(formtive_questions['evaluation_items'], formtive_questions['comments_recommendations'])
        formative_eleven.clean(formative_domain)

        formative_eleven.aggregate_topic()
        formative_eleven.aggregate_topic_sex()
        formative_eleven.aggregate_topic_region()
        formative_eleven.aggregate_topic_region_sex()

        formative_eleven_aggr_dict = {'formative_aggregate_topic' : formative_eleven.aggr_topic,
                                      'formative_aggr_topic_sex' : formative_eleven.aggr_topic_sex,
                                      'formative_aggr_topic_reg' : formative_eleven.aggr_topic_reg,
                                      'formative_aggr_topic_reg_sex' : formative_eleven.aggr_topic_reg_sex}
        
        formative_eleven.write_to_csv('eleven_grade', trial = True, **{'Comments' : formative_eleven.formative_comment_data})
        formative_eleven.write_to_xls('eleven_grade', 'eleven_aggregate', trial = True, **formative_eleven_aggr_dict)

