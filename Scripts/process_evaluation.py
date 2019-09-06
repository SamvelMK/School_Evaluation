# Imports 
from sqlalchemy import String, Integer, Float, Boolean, Column, and_, ForeignKey
from connection import Connection
from datetime import datetime, time, date
import time
from pytz import timezone
import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from openpyxl import load_workbook
import openpyxl

# Import modules
from connection import Connection
from user import UserData
from test import TestData
from tables import User, Tests, TestsQuestions, Formative, FormativeQuestions

class ProcessEvaluationData(TestData):

    """ 
    A class to handle process evaluation data. To initialize the class you need to specify the SQL connection String.
    """


    def __init__(self, connection_string):        
        
        # First we create a session with the DB.
        self.session = Connection.connection(connection_string)

        self.data = pd.DataFrame()
        
        # These are empty dataframes for transition proportions.
        self.transitions_glb = pd.DataFrame()
        self.transitions_eight_grade = pd.DataFrame()
        self.transitions_nine_grade = pd.DataFrame()
        self.transitions_ten_grade = pd.DataFrame()
        self.transitions_eleven_grade = pd.DataFrame()
        
    # General methods for process evaluation
    
    def read_files(self, **kwargs):

        """ 
        This function goes through the specified directories and reades files into a temporary dictionary called
        temp_data. The data is read as dataframe and stored with a key as the name of the file (e.g., user_2019). 
        After reading in all the files the function changes the directory to the global one (the where it started from). 
        """

        self.temp_data = {}

        for i in kwargs:
            grade = i
            year = kwargs[grade]
            current_dir = os.getcwd()
            if grade != 'user':
                os.chdir(current_dir + '/Data/{}_grade/{}_grade_{}'.format(grade, grade, year))
            else:
                os.chdir(current_dir + '/Data/{}/{}_{}'.format(grade, grade, year))

            for f in listdir(os.path.abspath(os.getcwd())):
                
                if (f.split('.')[1] == 'csv') and (f.split('.')[0] != 'Comments'): # This part makes sure that xlsx files are excluded.
                    self.temp_data[str(f.split('.')[0])] = pd.read_csv(str(os.path.abspath(f)),
                                                                       encoding = 'utf-8', engine='c')
            os.chdir(current_dir)
                
    def transitions_global(self, trial = None):
        """
        The method is designed for calculating transition statistics. The function has two modes: Trial = True/False.
        When the trial is True then the it takes searches for directories with the trial date (2019). Otherwise the function 
        takes the past year (current year - 1).    
        """

        def tranistions_grouped(group_by):
            """ 
            The group_by argument needs to be specified to show on which variable/s the aggrigation shall be implemented on. 
            """

            if trial:
                year = 2019
            else:
                now = datetime.now()
                year = now.year - 1
            
            self.year = year
            self.global_step_one = {} # Step 1: Registration
            self.global_step_two = {} # Step 2: Pre-test
            self.global_step_three = {} # Step 3: Post-test
            
            self.read_files(**{'user' : self.year, 
                                'eight' : self.year,
                                'nine' : self.year,
                                'ten' : self.year,
                                'eleven' : self.year})

            """ 
            After reading in the files the method creates dictionaries for each step (3 dictionaries in total).
            """

            for i in self.temp_data.keys():
                
                if 'post' in i: # assembles the post-test data
                    self.global_step_three[i]= pd.DataFrame(self.temp_data[i].drop_duplicates(['user_id'])\
                                                .groupby([i for i in group_by])['user_id'].count())
                    self.global_step_two[i] = pd.DataFrame(self.temp_data[i].drop_duplicates(['user_id'])\
                                                .groupby([i for i in group_by])['user_id'].count())
                    
                elif 'dropouts' in i: # adds droupouts data to step two.
                    self.global_step_two[i] = pd.DataFrame(self.temp_data[i].drop_duplicates(['user_id'])\
                                                .groupby([i for i in group_by])['user_id'].count())

                elif 'user' in i: # add user data to step one. 
                    self.global_step_one[i] = pd.DataFrame(self.temp_data[i]\
                                                            .groupby([i for i in group_by])['user_id'].count())
                
            df1 = pd.concat(self.global_step_three.values(), axis = 1)
            df1 = pd.DataFrame(df1.sum(axis=1, skipna=True))
            df1.rename(columns={ 0 : 'Step_Three'}, inplace = True)

            df2 = pd.concat(self.global_step_two.values(), axis = 1, sort=True)
            df2 = pd.DataFrame(df2.sum(axis=1, skipna=True))
            df2.rename(columns={ 0 : 'Step_Two'}, inplace = True)

            df3 = pd.concat(self.global_step_one.values(), axis = 1)
            df3 = pd.DataFrame(df3.sum(axis=1, skipna=True))
            df3.rename(columns={ 0 : 'Step_One'}, inplace = True)

            transitions = pd.concat([df3, df2, df1], axis = 1, sort=True)
            transitions = transitions.T.assign(Total = lambda x: x.sum(1)).T

            pc_change = transitions.pct_change(axis = 'columns').round(2) # Calculates percentage change between the steps and rounds to the second digit.
            pc_change.rename(columns = {'Step_One' : 'Step_One',
                                        'Step_Two' : 'Step_Two',
                                        'Step_Three' : 'Step_Three',
                                        'Step_One' : 'Step_One_change',
                                        'Step_Two' :  'Step_Two_change',
                                        'Step_Three' : 'Step_Three_change'}, inplace = True)
            
            transitions_pc = pd.concat([transitions, pc_change], axis = 1) 
            transitions_pc.drop('Step_One_change', axis = 1, inplace = True)
            return transitions_pc

        def transition_time(group_by):
            
            pre_date = {}
            for i in self.temp_data.keys():
                if 'pre' in i:
                    pre_date.update({ i : self.temp_data[i][['user_id', 'user_grade', 'user_created_at', 'region_name', 'user_sex', 'pre_tests_res_date']]\
                                            .drop_duplicates(subset = 'pre_tests_res_date', keep="last") })
            
            post_date = {}
            for i in self.temp_data.keys():
                if 'post' in i:
                    post_date.update({i : self.temp_data[i][['user_id', 'user_grade', 'user_created_at', 'region_name', 'user_sex', 'pre_tests_res_date']]\
                                            .drop_duplicates(subset = 'pre_tests_res_date', keep="last")})
            
            d1 = pd.concat(pre_date, ignore_index=True)
            d2 = pd.concat(post_date, ignore_index=True)
    
            transitions_time = d1.merge(d2, on = ['user_id', 'region_name', 'user_grade', 'user_sex', 'user_created_at'])
            transitions_time.rename(columns = {'pre_tests_res_date_x' : 'pre', 
                                                'pre_tests_res_date_y' : 'post'}, inplace = True)
            
            transitions_time['pre'] = transitions_time['pre'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d  %H:%M:%S"))
            transitions_time['post'] = transitions_time['post'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d  %H:%M:%S"))
            transitions_time['user_created_at'] = transitions_time['user_created_at'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d  %H:%M:%S"))
            
            transitions_time['tdelta_registered_pre'] = transitions_time['pre'] - transitions_time['user_created_at']
            transitions_time['tdelta_pre_post'] = transitions_time['post'] - transitions_time['pre']
            transitions_time['tdelta_registered_post'] = transitions_time['post'] - transitions_time['user_created_at']

            df1 = pd.DataFrame(transitions_time.groupby([i for i in group_by])['tdelta_registered_pre'].quantile(0.75).astype(str))
            df2 = pd.DataFrame(transitions_time.groupby([i for i in group_by])['tdelta_pre_post'].quantile(0.75).astype(str))
            df3 = pd.DataFrame(transitions_time.groupby([i for i in group_by])['tdelta_registered_post'].quantile(0.75).astype(str))
            
            combined_transitions_time = df1.join([df2, df3])

            return combined_transitions_time

        def test_time(group_by):

            pre_date = {}
            for i in self.temp_data.keys():
                if 'pre' in i:
                    pre_date.update({ i : self.temp_data[i][['user_id', 'user_grade', 'region_name', 'user_sex', 'pre_tests_res_time']]\
                                                        .drop_duplicates(subset = 'user_id', keep="last") })
                        
            post_date = {}
            for i in self.temp_data.keys():
                if 'post' in i:
                    post_date.update({i : self.temp_data[i][['user_id', 'user_grade', 'region_name', 'user_sex', 'pre_tests_res_time']]\
                                                        .drop_duplicates(subset = 'user_id', keep="last")})
            
            d1 = pd.concat(pre_date, ignore_index=True)
            d2 = pd.concat(post_date, ignore_index=True)

            transitions_test_time = d1.merge(d2, on = ['user_id', 'region_name', 'user_grade', 'user_sex'])
            transitions_test_time.rename(columns = {'pre_tests_res_time_x' : 'pre_test_time_minutes', 
                                                            'pre_tests_res_time_y' : 'post_test_time_minutes'}, inplace = True)
            

            def percentile(n): # an inner function to calculate percentiles
                def percentile_(x):
                    return np.percentile(x, n)
                percentile_.__name__ = 'percentile_%s' % n
                return percentile_  

            transitions_test_time = transitions_test_time.groupby([i for i in group_by])['pre_test_time_minutes' , 'post_test_time_minutes']\
                                                    .aggregate(['min', np.median, percentile(75), np.mean, max])\
                                                    .apply(lambda x: pd.to_timedelta(x, unit='s')).astype(str)
            
            return transitions_test_time

        self.transition_glb_reg = tranistions_grouped(['region_name'])
        self.transition_glb_reg_sex = tranistions_grouped(['region_name', 'user_sex'])

        self.transition_glb_grade = tranistions_grouped(['user_grade'])
        self.transition_glb_grade_region = tranistions_grouped(['user_grade', 'region_name'])
        self.transition_glb_grade_region_sex = tranistions_grouped(['user_grade', 'region_name', 'user_sex'])

        self.transition_time_reg = transition_time(['region_name'])
        self.transition_time_reg_sex = transition_time(['region_name', 'user_sex'])

        self.transition_time_grade = transition_time(['user_grade'])
        self.transition_time_grade_region = transition_time(['user_grade', 'region_name'])
        self.transition_time_grade_region_sex = transition_time(['user_grade', 'region_name', 'user_sex'])

        self.test_time_reg = test_time(['region_name'])
        self.test_time_reg_sex = test_time(['region_name', 'user_sex'])

        self.test_time_grade = test_time(['user_grade'])
        self.test_time_grade_region = test_time(['user_grade', 'region_name'])
        self.test_time_grade_region_sex = test_time(['user_grade', 'region_name', 'user_sex'])
    
    # Specific methods for process evaluation
    
    def query(self, grade, region_names, trial = None):
        
        """ 
            If the trial argument is set to be True then the databased is queried with the dates of the trial of the e-learning module. 
            Otherwise, the start date of the "date" filter is set on the current date (i.e., the date of the query) and the end date is set
            to -1 years. 
        """
        
        # Because the created_at column in the User table is in UNIX epoch format we need to convert the UTC
        # time format to UNIX epoch time format before sending the query.

        if trial:
            start_date =  time.mktime(pd.Timestamp("2019-06-06 11:00:00").timetuple())
            end_date = time.mktime(pd.Timestamp("2019-07-31 00:00:00").timetuple())
        else:
            start_date = pd.Timestamp(datetime.now().timetuple())
            end_date = time.mktime(pd.Timestamp(datetime.now() + pd.DateOffset(years=-1)).timetuple())

        self.data = pd.read_sql(self.session.query(User, Formative, FormativeQuestions).with_labels()\
                         .filter(and_(User.created_at.between(start_date, end_date), User.grade == str(grade)))\
                                .join(Formative, Formative.user_id == User.id)\
                                .join(FormativeQuestions, FormativeQuestions.id == Formative.test_id)\
                                .statement, self.session.bind)
        
        # Changing the time from UNIX epoch to US/Central: The "Created_at" and "Updated_at" objects are stored as UNIX time
        # stamp and in UTC timezone. However, other date objects (e.g., in pre_tests_res table) in other tables are 
        # stored as datetime objects and in US Central time zone (based on the location of the IP). 
        # Therefore, 1) we need to change the UNIX int obj to py datetime object; 
        # then 2) change the UTC time zone to US/Central.
        
        # utc = timezone('UTC')
        # central = timezone('US/Central')
        
        self.data['user_created_at'] = self.data['user_created_at'].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
                                                               
        self.data['user_updated_at'] = self.data['user_updated_at'].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
                                                               
        
        self.data['region_name'] = self.data['user_region'].apply(lambda x: region_names[x])
    
    
    def extract(self, items, comments):
        
        self.formative_item_data = self.data[self.data['help_answers_test_id'].isin(items)]
        self.formative_comment_data = self.data[self.data['help_answers_test_id'].isin(comments)]
        
    def clean(self, topics_dict):

        def drop_douplicates(test):

            """ This function drops the duplicates from the dataframe and returns a dataframe"""

            test = test.loc[:,~test.columns.duplicated()]
                
            # The procedure below eliminates double enteries per user. The first set of answers.
            temp_test = []
            for i in self.formative_item_data['user_id'].unique():
                temp = test.loc[test['user_id'] == i]
                temp = temp.drop_duplicates(subset = 'help_answers_test_id', keep="last") # Keep last assuming that the last entry will contain the fullest data.
                temp_test.append(temp)
                
            test = pd.concat(temp_test)

            return test
        
        def attach_item_labels(test, items):
            l = []
            for y in test['help_answers_test_id']:
                for i in items:
                    if y in items[i]:
                        l.append(i)
            test['topic'] = l
            
            return test
        
        temp = drop_douplicates(self.formative_item_data)
        temp_formative_item_data = attach_item_labels(temp, topics_dict)
        self.formative_item_data = temp_formative_item_data
        
        temp_data_comments = drop_douplicates(self.formative_comment_data)
        self.formative_comment_data = temp_data_comments

    # Methods for formative evaluation items: Statistics
    
    def item_prc(self, test, *args):
        
        test['answer_category'] = test['help_answers_answer'].replace([1, 2, 3], 
                                                         ['totally agree', 'partially_agree', 'disagree'])
        
        test = pd.DataFrame(test.groupby([i for i in args] + ['answer_category'])['help_answers_answer'].count()*100/\
                     test.groupby([i for i in args])['help_answers_answer'].count())
        
        return test
    
    def aggregate_topic(self):
        
        self.aggr_topic = self.item_prc(self.formative_item_data, 'topic')
    
    def aggregate_topic_sex(self):
        
        self.aggr_topic_sex = self.item_prc(self.formative_item_data, 'topic', 'user_sex')
    
    def aggregate_topic_region(self):
        
        self.aggr_topic_reg = self.item_prc(self.formative_item_data, 'region_name', 'topic')
    
    def aggregate_topic_region_sex(self):
        
        self.aggr_topic_reg_sex = self.item_prc(self.formative_item_data, 'region_name', 'topic', 'user_sex')
    
    
        