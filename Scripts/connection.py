# Imports
from sqlalchemy import create_engine, Sequence
from sqlalchemy.orm import sessionmaker

from tables import User, Region, Community, Tests, Formative, FormativeQuestions
from config import connection_string

class Connection(object):
    
    """ This class creates a connection with the DB. the connection method requires the connection
        string. The connection string includes the necessary configurations of the DB. Because connection it's a static method
        it does not require instantiation. """
    
    @staticmethod
    def connection(connection_string):
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        return session
