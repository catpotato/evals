from sqlalchemy import and_, Column, create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Evaluation(Base):

    __tablename__ = 'evaluations'

    id = Column(Integer, primary_key = True)
    unique_crn = Column(String, unique=True)
    year = Column(Integer)
    semmester = Column(Integer)
    course = Column(String)
    section = Column(String)
    dept = Column(String)
    professor = Column(String)
    responses = Column(Integer)
    grades = Column(String)
    effectiveness = Column(String)

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

    def uniqueify(self):
        self.unique_crn = self.dept + str(self.course) + self.section + str(self.year) + str(self.semmester) + self.professor
