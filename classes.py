class DatabaseConnection:

    """ Class to create a connection with SQL database and run queries""" 
    def __init__(self, config):
        self.open_connection(config) 

    def open_connection(self, config):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def query(self, query_input):
        self.cursor.execute(query_input)        
        return self.cursor.fetchall()

    def get_column_names(self):
        return self.cursor.column_names

    def __del__(self):
        self.cursor.close()
        self.cnx.close()


class Query:
    
    """Class to handle extraction of data from a database."""

    def __init__(self, connection):
        self.connection = connection
        self.dfs = {}
    
    def query_builder(self, columns = None, table = None, date_column = 'date', comparison_operator = '>=',
                            date = '2019-06-06 13:51:33', date_type = 'date_time', filter_by_date = False, 
                            filter_by_grade = False, id_column = None, grade = None, query_type = None, 
                            advanced_query = None):
        if not query_type:                    
            self.column = ', '.join(columns)
            self.query = "SELECT {} FROM {}".format(self.column, table)
            self.sub_query = " WHERE {} in (SELECT id FROM user WHERE grade = {})".format(id_column, grade)
            self.date = date
            self.date_type = date_type
            self.date_column = date_column
            self.comparison_operator = comparison_operator
        else:
            self.advanced_query = advanced_query

        def general_query():
            return self.query

        def filter_date():
            if date_type == 'date_time':
                self.new_query = self.query + " WHERE {} {} '{}'".format(self.date_column, self.comparison_operator, self.date)
                return self.new_query
            else:
                new_request = self.query.split("'")[0]
                new_date = int(pd.Timestamp(self.date).strftime("%s"))
                new_query = self.query + " WHERE {} {} '{}'".format(self.date_column, self.comparison_operator, new_date)
                return new_query
                        
        def filter_grade():
            return self.query + self.sub_query

        if not query_type:
            if filter_by_date == True and filter_by_grade == True:
                new_query = filter_date() + self.sub_query.replace(' WHERE', ' AND', 1)
                return new_query
            elif filter_by_date == True and filter_by_grade == False:
                query = filter_date()
                return  query
            elif filter_by_grade == True and filter_by_date == False:
                query = filter_grade()
                return query
            else:
                new_query = general_query()
                return new_query
        else:
            new_query = self.advanced_query
            return new_query
        
    def create_dataframe(self, query):
        df = pd.DataFrame(self.connection.query(query))
        df.columns = self.connection.get_column_names()
        return df
        
class User(Query):

    """ Class to handle user data """

    def __init__(self, connection):
        self.connection = connection
        self.queries = {}
        self.user_dfs = {}
        
    def user_query(self):
        self.queries['user_eight_grade'] = self.query_builder(columns = user_column, 
                                                             table= 'user', filter_by_date=True, filter_by_grade=True,
                                                             grade = 8, id_column = 'id', date_column = 'created_at', 
                                                             date_type = 'int')
        self.queries['user_nine_grade'] = self.query_builder(columns = user_column, 
                                                             table= 'user', filter_by_date=True, filter_by_grade=True,
                                                             grade = 9, id_column = 'id', date_column = 'created_at', 
                                                             date_type = 'int')
        self.queries['user_ten_grade'] = self.query_builder(columns = user_column, 
                                                             table= 'user', filter_by_date=True, filter_by_grade=True,
                                                             grade = 10, id_column = 'id', date_column = 'created_at', 
                                                             date_type = 'int')
        self.queries['user_eleven_grade'] = self.query_builder(columns = user_column, 
                                                             table= 'user', filter_by_date=True, filter_by_grade=True,
                                                             grade = 11, id_column = 'id', date_column = 'created_at', 
                                                             date_type = 'int')
            
    def user_data_frame(self):
        self.user_query() 
        for grade, query in self.queries.items():
            self.user_dfs[grade] = self.create_dataframe(query)
    
    class tests:
        
        """ Class to handle test data """

        def __init__(self, connection):
            self.connection = connection
            self.dfs = {'eight_grade: {data}, nine_grade: {data}, ten_grade: {data}, eleven_grade: {data}'}
                
                'Data'
                    'pretest'
                        '-> user_id, test_id, answer, time, count, status, date '
                    'posttest'
                        '-> user_id, test_id, answer, time, count, status, date '
        pass
    
    class formative:

         """ Class to handle fromative evaluation data """

         def __init__(self, connection):
            self.connection = connection
            self.dfs = {'eight_grade: {data}, nine_grade: {data}, ten_grade: {data}, eleven_grade: {data}'}

                'Data'
                    'lessons'
                        '-> choose_test_res, drag_test_res, hardest_age_res, pre_test_res'
                    'evaluation data'
                        '-> user_id, grade, test_id, answer, comment'
        pass
    
    class 


    def __init__(self, extract):
        self.extract = extract
        self.dfs = {}
    

    def create_dataframe(self, name, columns,
                         table, date = '2019-06-06 13:51:33',
                         comparison_operator = '>=', date_column = 'date',
                         date_type = 'date_time', grade = None, id_column = None):
        
        ''' create_dataframe method executes an SQL query and creates pandas dataframe which is stored in a dictionary in the 
        global environment. 
        * DESCRIPTION * 
        | The method has takes three positional arguments and three optional arguments for filtering purposes:   | 
        | The "name" argument refers to the name that shall be assigned to the created dataframe. The columns    |
        | arguemt is the columns that shall be queried from a particular table. The table argument refers to the |
        | specific table in the database.                                                                        |
        | The additional argument date is the date by which the query should be filtered. The default of this    |
        | argument is set to be euqal to '2019-06-06 13:51:33' which is the date of the start of the pilot.      |
        | The comparison operator argument refers to the sign by which the filter shall be applied (e.g., >, <)  |
        | The date_column indicates the name of the column that includes the date in a specific table.           |
        | The defualt of the date_column is set to be ecual to 'date' as this is the most prevalent name in this |
        | particular database. The date_type argument refers to the type of data structure of the date column.   |
        | It can be either a date_time object or integer. The grade argument filters the data based on the school|
        | grade. The id_column refers to the id column of the table of reference.                                |
        '''
        
        def general_filter():
            column = ', '.join(columns)
            if not grade:
                query = "SELECT {} FROM {}".format(column, table)
            else:
                sub_query = "WHERE {} in (SELECT id FROM user WHERE grade = {})".format(id_column, grade)
                query = "SELECT {} FROM {} {}".format(column, table, sub_query)
            df = pd.DataFrame(self.extract.query(query))
            df.columns = self.extract.get_column_names()
            self.dfs[name] = df
                  
        def date_filter():
            column = ', '.join(columns)
            if not grade:
                query = "SELECT {} FROM {} WHERE {} {} '{}'".format(column, table, date_column, comparison_operator, date)
                if date_type == 'date_time':
                    dates = pd.Timestamp(date)
                    df = pd.DataFrame(self.extract.query(query))
                    df.columns = self.extract.get_column_names()
                    self.dfs[name] = df
                else:
                    column = ', '.join(columns)
                    query = "SELECT {} FROM {} WHERE {} {} '{}'".format(column, table, date_column, comparison_operator, date)
                    new_request = query.split("'")[0]
                    dates = int(pd.Timestamp(date).strftime("%s"))
                    new_request = new_request + "'" + str(dates) + "'"
                    df = pd.DataFrame(self.extract.query(new_request))
                    df.columns = self.extract.get_column_names()
                    df[date_column] = df[date_column].apply(lambda x: datetime.fromtimestamp(x))
                    self.dfs[name] = df
            else: 
                sub_query = "AND {} in (SELECT id FROM user WHERE grade = {})".format(id_column, grade)
                query = "SELECT {} FROM {} WHERE {} {} '{}'".format(column, table, date_column, comparison_operator, date)
                if date_type == 'date_time':
                    dates = pd.Timestamp(date)
                    df = pd.DataFrame(self.extract.query(query))
                    df.columns = self.extract.get_column_names()
                    self.dfs[name] = df
                else:
                    column = ', '.join(columns)
                    new_request = query.split("'")[0]
                    dates = int(pd.Timestamp(date).strftime("%s"))
                    query = "SELECT {} FROM {} WHERE {} {} '{}' {}".format(column, table, date_column, comparison_operator,
                                                                       dates, sub_query)
                    df = pd.DataFrame(self.extract.query(query))
                    df.columns = self.extract.get_column_names()
                    df[date_column] = df[date_column].apply(lambda x: datetime.fromtimestamp(x))
                    self.dfs[name] = df            
                    
        if not date:
            general_filter()
        else:
            date_filter()
        
        
                
        def question_mapper(self, data, questions_df, column_name = 'questions'):
            """Question mapper method takes the question_id and maps the question onto the dataframe. """
            self.data[column_name] = self.data['question_id']



