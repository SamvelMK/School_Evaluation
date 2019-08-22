# Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Float, Boolean, Column, and_, ForeignKey

# Calling the SQL alchemy Base class. 
Base = declarative_base()

# Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Float, Boolean, Column, and_, ForeignKey

# Calling the SQL alchemy Base class. 
Base = declarative_base()

class Region(Base):        
    __tablename__ = 'region'
    id = Column(Integer, primary_key = True)

class Community(Base):        
    __tablename__ = 'community'
    id = Column(Integer, primary_key = True)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    grade = Column(Integer)
    sex = Column(Integer)
    region = Column(Integer, ForeignKey(Region.id))
    city = Column(Integer)
    community = Column(Integer, ForeignKey(Community.id))
    school = Column(Integer)
    current_grade = Column(Integer)
    created_at = Column(Integer)
    updated_at = Column(Integer)

class TestsQuestions(Base):
    __tablename__ = 'tests_question'
    id = Column(Integer, primary_key = True)
    right_answers = Column(String)

class Tests(Base):
    __tablename__ = 'pre_tests_res'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey(User.id))
    test_id = Column(Integer, ForeignKey(TestsQuestions.id))
    answer = Column(String)
    time = Column(Integer)
    count = Column(Integer)
    status = Column(Integer)
    date = Column(Integer)
    
class FormativeQuestions(Base):
    __tablename__ = 'help_test'
    id = Column(Integer, primary_key = True)

class Formative(Base):
    __tablename__ = 'help_answers'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey(User.id))
    grade = Column(Integer)
    test_id = Column(Integer, ForeignKey(FormativeQuestions.id))
    answer = Column(Integer)
    comment = Column(String)