# Imports
from datetime import datetime, time, date
import time
from pytz import timezone
import pandas as pd
import os
from os import listdir
from os.path import isfile, join
from openpyxl import load_workbook
import openpyxl

from connection import Connection
from tables import User 


class UserData(Connection):

    """ 
    Class to handle user data.
    To initialize the class, you need to pass on the SQLdb connection string, region names dictionary
    and specify whether the it is a trial or not.
    The region names dictionary includes the region names that will be reassigned to the dataframes (because the 
    region names in the original db is in Armenian alphabet).
    The trial argument specifies whether the preprocessing is for the trial period. If true then the dates of the
    trial will be used for data query, otherwise the current date -1 will be selected.  
    """

    def __init__(self, connection_string, region_names, trial = None):

                
        # First we create a session with the DB.
        self.session = Connection.connection(connection_string)
        self.region_names = region_names
        
        # Because the created_at column in the User table is in UNIX epoch format we need to convert the UTC
        # time format to UNIX epoch time format before sending the query.

        if trial:
            start_date =  time.mktime(pd.Timestamp("2019-06-06 11:00:00").timetuple())
            end_date = time.mktime(pd.Timestamp("2019-07-31 00:00:00").timetuple())
        else:
            start_date = pd.Timestamp(datetime.now().timetuple())
            end_date = time.mktime(pd.Timestamp(datetime.now() + pd.DateOffset(years=-1)).timetuple())

        # Send Query.
        self.user_table = pd.read_sql(self.session.query(User).with_labels()\
                             .filter((User.created_at.between(start_date, end_date)))\
                                          .statement, self.session.bind)
        
        # Changing the time from UCT to US/Central: The "Created_at" and "Updated_at" objects are stored as UNIX time
        # stamp and in UTC timezone. However, other date objects (e.g., in pre_tests_res table) in other tables are 
        # stored as datetime objects and in US Central time zone (based on the location of the IP). 
        # Therefore, 1) we need to change the UNIX int obj to py datetime object; 
        # then 2) change the UTC time zone to US/Central.
        
        # utc = timezone('UTC')
        # central = timezone('US/Central')
        
        self.user_table['user_created_at'] = self.user_table['user_created_at'].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
                                                                           
        self.user_table['user_updated_at'] = self.user_table['user_updated_at'].apply(lambda x: datetime.fromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"))
                                                                           
        self.user_table['region_name'] = self.user_table['user_region'].apply(lambda x: self.region_names[x])

    def user_info(self):

        """ 
        User information method prepares a string with user information. E.g. number of regions the users come from. 
        """
        
        # Note: The number of registered users (unless otherwise specified) reflects the total number of registered users regardless of their
        # status of completion of the course.
        
        region = len(self.user_table['user_region'].unique())
        region_names = self.user_table[['region_name', 'user_id']].groupby(["region_name"]).count()
        region_names.reset_index(level=0, inplace=True)
        region_names = region_names['region_name']
        communities = len(self.user_table['user_community'].unique())
        school = len(self.user_table['user_school'].unique())
        user_registered = len(self.user_table['user_id'].unique())
        eight_grade = len(self.user_table[self.user_table['user_grade'] == 8])
        nine_grade = len(self.user_table[self.user_table['user_grade'] == 9])
        ten_grade = len(self.user_table[self.user_table['user_grade'] == 10])
        eleven_grade = len(self.user_table[self.user_table['user_grade'] == 11])
        sex = (sum(self.user_table['user_sex']) * 100 / len(self.user_table['user_sex']))
        curent_date = date.today().strftime("%B %d, %Y")

        self.info = """
        
        ************************************************************************************************
        ****                                USER INFO                                               ****
        ************************************************************************************************
        **** Data acquisition date: {}                                                 ****
        ****        Total number of participating regions: {}                                        ****
        ****        Total number of participating communities: {}                                   ****
        ****        Total number of participating schools: {}                                      ****
        ****        Total number of registered users: {}                                           ****
        ****        Gender distribution among the registered participants: {}% Male              ****
        ****        Registered users at grade eight: {}                                            ****
        ****        Registered users at grade nine: {}                                             ****
        ****        Registered users at grade ten: {}                                               ****
        ****        Registered users at grade eleven: {}                                           ****
        ************************************************************************************************
        ************************************************************************************************
        **** NOTE: The number of registered users (unless otherwise specified) reflect the total    **** 
        **** number of registered users regardless of their status of completion of the course.     ****                                             
        ************************************************************************************************


        """.format(curent_date, region, communities, school,  
                   user_registered, round(sex, 2), eight_grade, nine_grade, 
                   ten_grade, eleven_grade)
        
        return self.info

    def user_aggr(self, group_by):

        """ 
        This function creates aggregates (counts) of a passed dataframe.
        The group_by argument specifies the variables the df should be aggregated on.
        """

        students = self.user_table[['user_id'] + group_by].groupby([i for i in group_by]).nunique().T
        schools = self.user_table[['user_school'] + group_by].groupby([i for i in group_by]).nunique().T
        communities = self.user_table[['user_community'] + group_by].groupby([i for i in group_by]).nunique().T
        cities = self.user_table[['user_city'] + group_by].groupby([i for i in group_by]).nunique().T

        user_sex = self.user_table[['user_sex', 'user_id'] + group_by]
        user_sex = pd.DataFrame(round(user_sex.groupby([i for i in group_by])['user_sex'].sum()*100/user_sex.groupby([i for i in group_by])['user_sex'].count(), 2)).T

        user_results = pd.concat([schools, communities, cities, students, user_sex]).T

        user_results = user_results[['user_school', 'user_community', 'user_city', 'user_id', 'user_sex']]
        user_results.rename(columns = {'user_id' : 'Number of Students', 
                                        'user_school' : 'Number of Schools',
                                        'user_community' : 'Number of Communities',
                                        'user_city' : 'Number of Cities',
                                        'user_sex' : 'Proportion of Males'}, inplace = True)

        return user_results
      
    def user_aggregate_grade(self):
        self.user_aggr_grade = self.user_aggr(['user_grade'])

    def user_aggregate_grade_region(self):
        self.user_aggr_grade_region = self.user_aggr(['user_grade', 'region_name'])
    
    @staticmethod
    def write_to_csv(directory, trial = None, **kwargs):
        
        """ 
        The write_to_csv method writes out the specified dataframe to a csv file.
        Requires specification of the name of the directory. That's the directory that 
        shall be created inside the Data directory. Trial argument specifies whether the trial dates shall be used. If
        true than the trial dates are selected; otherwise the current date -1 is selected. The kwargs is a dictionary that takes
        the dataframe_name as a key and dataframe as the value. 
        """
        
        current_dir = os.getcwd()

        if trial:
            now = datetime.now()
            year = now.year
        else:
            year = now.year - 1
        
        if not os.path.exists('Data'):
            os.mkdir('Data')
        os.chdir('Data')
        
        if not os.path.exists('{}'.format(directory)):
            os.mkdir('{}'.format(directory))
        os.chdir('{}'.format(directory)) 
        
        if not os.path.exists('{}_{}'.format(directory, year)):
            os.mkdir('{}_{}'.format(directory, year))
        os.chdir('{}_{}'.format(directory, year))    
        
        for i in kwargs:
            if not os.path.isfile('{}_{}.csv'.format(i, year)):
                kwargs[i].to_csv('{}_{}.csv'.format(i, year), index=False, header=True, encoding='utf_8_sig') # the utf_8_sig was necessary because of armenian letters.
        
        os.chdir(current_dir)
    
    @staticmethod    
    def write_info(directory, message, trial = None):

        """ 
        Write_info method writes out the info.txt file. This method requires the name of the directory where the info file is
        going to be written in. The trial argument is used for selecting the dates. If true then the dates of the trial will be
        selected; otherwise the current date -1 will be selected.
        """

        current_dir = os.getcwd()

        if trial:
            now = datetime.now()
            year = now.year
        else:
            year = now.year - 1

        if not os.path.exists('Data'):
            os.mkdir('Data')
        os.chdir('Data')
        
        if not os.path.exists('{}'.format(directory)):
            os.mkdir('{}'.format(directory))
        os.chdir('{}'.format(directory)) 
        
        if not os.path.exists('{}_{}'.format(directory, year)):
            os.mkdir('{}_{}'.format(directory, year))
        os.chdir('{}_{}'.format(directory, year))

        f = open(os.path.abspath(os.path.abspath(str(os.getcwd()) + "/info.txt" )) ,"a")
        f.write(message)

        os.chdir(current_dir)
    
    