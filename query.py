import json
from evaluation import *
from operator import add
all_dates = [2016.5,2016.0,2015.5,2015.0,2014.5,2014.0,2013.5,2013.0,2012.5,2012.0,]
import numpy as np
import pandas as pd

engine = create_engine('sqlite:///data.db', echo=True)
Base.metadata.create_all(engine)

class Query:
    def __init__(self, period=None, department=None, course=None, professor=None): # optional parameters
        self.period = period
        # in the format of [20XX.semmester, 20XX.semmester]
        self.department = department
        self.professor = professor
        self.course = course
        self.query_as_list_dict = []
        self.query_as_dataframe = pd.DataFrame()
        self.not_queried = True

    '''
    takes in query parameters and returns a list of a bunch of info

    [
        (responses, [grades], [effectiveness])
        .....
    ]
    '''


    def query(self):
        Session = sessionmaker(bind=engine)
        session = Session()

        # set up database
        q = session.query(Evaluation)

        # dept
        if self.department:
            q = q.filter(Evaluation.dept == str(self.department.upper()))

        # prof
        if self.professor:
            q = q.filter(Evaluation.professor == self.professor)

        # course
        if self.course:
            q = q.filter(Evaluation.course == self.course)

        # period
        # make a list of all of the years of the request
<<<<<<< HEAD
        if self.period:
            date_range = [self.period[0]]
            while date_range and date_range[-1] != self.period[1]:
                date_range.append(date_range[-1] -.5)
=======
        date_range = [self.period[0]]
        while date_range[-1] != self.period[1] and len(date_range) > 0:
            date_range.append(date_range[-1] -.5)
>>>>>>> master

            # make a list of years that you don't want
            forbidden_dates = all_dates
            for allowed_date in date_range:
                forbidden_dates.remove(allowed_date)

            # remove all of forbidden_years from query
            for forbidden_date in forbidden_dates:
                q = q.filter(Evaluation.semmester != forbidden_date*10)

        # convert to dict
        for u in q.all():
            self.query_as_list_dict.append(u.__dict__)

        for query in self.query_as_list_dict:
            query['grades'] = json.loads(query['grades'])
            query['effectiveness'] = json.loads(query['effectiveness'])

        self.query_as_dataframe = pd.DataFrame(self.query_as_list_dict)

        self.not_queried = False

    def get_query(self):
        if(self.not_queried):
            self.query()
        return self.query_as_dataframe
