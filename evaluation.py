from sqlalchemy import and_, Column, create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()

'''

COURSE (department + course + including L if a lab (i.e. CS150L))
SEMESTER (year.semester i.e 20150 for 2015-2016 semester 1, 20155 for 2015-2016 semester 2)
PROFESSOR (last name)
DEPT ('CS', 'ES', etc...)
LEVEL (100,200,300,400 etc)
RESPONSES (number of responses)
GRADES (string of grades)
EFFECTIVENESS (string of effectiveness)
UNIQUE_CRN (course + section)

'''

class Evaluation(Base):

    __tablename__ = 'evaluations'

    id = Column(Integer, primary_key = True)
    course = Column(String)
    semmester = Column(Integer)
    professor = Column(String)
    dept = Column(String)
    level = Column(Integer)
    grades = Column(String)
    responses = Column(Integer)
    effectiveness = Column(String)
    #unique_crn = Column(String, unique=True)

    def set_grades(self, _grades):
        self.grades = json.dumps(_grades)

    def set_effectiveness(self, _effectiveness):
        self.effectiveness = json.dumps(_effectiveness)

    def __init__(self):
        self.year = 2017
        self.semmester = 10
        self.course = "101"
        self.section = "01";
        self.dept = "ART"
        self.professor = "Ahl"
        self.responses = 20
        self.grades = self.set_grades([0,0,0,0,0,0,0,0,0,0,0,0])
        self.effectiveness = self.set_effectiveness([0,0,0,0])
