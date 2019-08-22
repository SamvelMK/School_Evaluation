# Imports
from tasks import Task
from datetime import datetime, time, date
import os

if __name__ == '__main__':

    # A function to write a log file
    def write_log(message):
        current_date = datetime.now()
        f= open(os.path.abspath('Data/logs.txt'),"a")
        f.write(str(current_date) + ': ' + message + '\n')

    task = Task()   
    
    # User Data
    try:
        task.user()
        write_log('User data was processed successfuly!')
    except Exception as err:
        write_log('User data failed to be processed! Error: {}'.format(err))
    
    # Test data
    try:
        task.eight_grade()
        write_log('Egiht grade data was processed successfuly!')
    except Exception as err:
        write_log('Egiht grade data failed to be processed! Error: {}'.format(err))   
    
    try:
        task.nine_grade()
        write_log('Nine grade data was processed successfuly!')
    except Exception as err:
        write_log('Nine grade data failed to be processed! Error: {}'.format(err)) 
    
    try:
        task.ten_grade()
        write_log('Ten grade data was processed successfuly!')
    except Exception as err:
        write_log('Ten grade data failed to be processed! Error: {}'.format(err)) 

    try:
        task.eleven_grade()
        write_log('Eleven grade data was processed successfuly!')
    except Exception as err:
        write_log('Eleven grade data failed to be processed! Error: {}'.format(err)) 

    # Process evaluation
    try:
        task.process_evaluation_global()
        write_log('Process evaluation global data was processed successfuly!')
    except Exception as err:
        write_log('Process evaluation global data failed to be processed! Error: {}'.format(err)) 
    
    try:
        task.frm_eight_grade()
        write_log('Process evaluation eight grade data was processed successfuly!')
    except Exception as err:
        write_log('Process evaluation eight grade datafailed to be processed! Error: {}'.format(err)) 
    
    try:
        task.frm_nine_grade()
        write_log('Process evaluation nine grade data was processed successfuly!')
    except Exception as err:
        write_log('Process evaluation nine grade datafailed to be processed! Error: {}'.format(err)) 
    
    try:
        task.frm_ten_grade()
        write_log('Process evaluation ten grade data was processed successfuly!')
    except Exception as err:
        write_log('Process evaluation ten grade datafailed to be processed! Error: {}'.format(err)) 
    
    try:
        task.frm_eleven_grade()
        write_log(str('Process evaluation eleven grade data was processed successfuly!' + '\n' + '#'*91))
    except Exception as err:
        write_log(str('Process evaluation eleven grade datafailed to be processed! Error: {}'.format(err) + '\n' + '#'*91))
