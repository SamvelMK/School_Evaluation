# Imports 
from sqlalchemy import String, Integer, Float, Boolean, Column, and_, ForeignKey
from connection import Connection
from datetime import datetime, time, date
import time
from pytz import timezone
import pandas as pd
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

import pandas as pd
from config import connection_string, region_names, eight_grade_tests, eight_grade_attitude, nine_grade_tests, nine_grade_attitude, ten_grade_tests, ten_grade_attitude, eleven_grade_tests, eleven_grade_attitude, formtive_questions, formative_domain
from user import UserData
from test import TestData


class ProcessEvaluationData(TestData):

    """ 
        DOC STRING

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

        """ This function goes through the specified directories and reades files into a temporary dictionary called
        temp_data. The data is read as dataframe and stored with a key as the name of the file (e.g., user_2019). 
        After reading in all the files the function changes the directory to the global one (the where it started from). """

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

        def tranistions_grouped(group_by):

            """" The method is designed for calculating transition statistics. The function has two modes: Trial = True/False.
            When the trial is True then the it takes searches for directories with the trial date (2019). Otherwise the function 
            takes the past year (current year - 1). """

            if trial:
                year = 2019
            else:
                now = datetime.now()
                year = now.year - 1
            
            self.year = year
            self.global_step_one = {}
            self.global_step_two = {}
            self.global_step_three = {}
            
            self.read_files(**{'user' : self.year, 
                                'eight' : self.year,
                                'nine' : self.year,
                                'ten' : self.year,
                                'eleven' : self.year})

            """ After reading in the files the method creates dictionaries for each step (3 dictionaries in total). """

            for i in self.temp_data.keys():
                
                if 'post' in i:
                    
                    self.global_step_three[i]= pd.DataFrame(self.temp_data[i].drop_duplicates(['user_id'])\
                                                .groupby([i for i in group_by])['user_id'].count())
                    self.global_step_two[i] = pd.DataFrame(self.temp_data[i].drop_duplicates(['user_id'])\
                                                .groupby([i for i in group_by])['user_id'].count())
                    
                elif 'dropouts' in i:
                    self.global_step_two[i] = pd.DataFrame(self.temp_data[i].drop_duplicates(['user_id'])\
                                                .groupby([i for i in group_by])['user_id'].count())
                elif 'user' in i:
                    self.global_step_one[i] = pd.DataFrame(self.temp_data[i]\
                                                            .groupby([i for i in group_by])['user_id'].count())
                
            df1 = pd.concat(self.global_step_three.values(), axis = 1)
            df1 = pd.DataFrame(df1.sum(axis=1, skipna=True))
            df1.rename(columns={ 0 : 'Step_Three'}, inplace = True)

            df2 = pd.concat(self.global_step_two.values(), axis = 1)
            df2 = pd.DataFrame(df2.sum(axis=1, skipna=True))
            df2.rename(columns={ 0 : 'Step_Two'}, inplace = True)

            df3 = pd.concat(self.global_step_one.values(), axis = 1)
            df3 = pd.DataFrame(df3.sum(axis=1, skipna=True))
            df3.rename(columns={ 0 : 'Step_One'}, inplace = True)

            transitions = pd.concat([df3, df2, df1], axis = 1)
            transitions = transitions.T.assign(Total = lambda x: x.sum(1)).T

            pc_change = transitions.pct_change(axis = 'columns').round(2)
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
                    
        self.transition_glb_grade = tranistions_grouped(['user_grade'])
        self.transition_glb_grade_region = tranistions_grouped(['user_grade', 'region_name'])
        self.transition_glb_grade_region_sex = tranistions_grouped(['user_grade', 'region_name', 'user_sex'])

    def transitions_by_grade(self):
        self.transitions_grade = {}
        
        grade = {'eight' : 8, 
                 'nine' : 9,
                 'ten' : 10,
                 'eleven' : 11}
        
        for i in grade:
            step_one = pd.DataFrame(self.temp_data['user_{}'.format(self.year)][self.temp_data['user_{}'.format(self.year)]['user_grade'] == grade[i]]\
                                .groupby(['region_name', 'user_sex'])['user_id'].count())  
            
            step_two = dict((k, v) for (k, v) in self.global_step_two.items() if i in k)
            step_three = dict((k, v) for (k, v) in self.global_step_three.items() if i in k)        
            print(step_two.keys())
            # df1 = pd.concat(step_three.values(), axis = 1)
            # df1 = pd.DataFrame(df1.sum(axis=1, skipna=True))
            # df1.rename(columns={ 0 : 'Step_Three'}, inplace = True)

            # df2 = pd.concat(step_two.values(), axis = 1)
            # df2 = pd.DataFrame(df2.sum(axis=1, skipna=True))
            # df2.rename(columns={ 0 : 'Step_Two'}, inplace = True)

            # df3 = pd.DataFrame(step_one.sum(axis=1, skipna=True))
            # df3.rename(columns={ 0 : 'Step_One'}, inplace = True)

            # print(df3)


            # transitions = pd.concat([df3, df2, df1], axis = 1)
            # transitions = transitions.T.assign(Total = lambda x: x.sum(1)).T

            # pc_change = transitions.pct_change(axis = 'columns').round(2)
            # pc_change.rename(columns = {'Step_One' : 'Step_One',
            #                             'Step_Two' : 'Step_Two',
            #                             'Step_Three' : 'Step_Three',
            #                             'Step_One' : 'Step_One_change',
            #                             'Step_Two' :  'Step_Two_change',
            #                             'Step_Three' : 'Step_Three_change'}, inplace = True)

            # transitions_pc = pd.concat([transitions, pc_change], axis = 1)
            # transitions_pc.drop('Step_One_change', axis = 1, inplace = True)
            
            # self.transitions_grade[i] = transitions

transitions = ProcessEvaluationData(connection_string)
transitions.transitions_global(trial=True)
transitions.transitions_by_grade()
