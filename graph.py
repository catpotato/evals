import json
from evaluation import *
from operator import add
all_dates = [2016.5,2016.0,2015.5,2015.0,2014.5,2014.0,2013.5,2013.0,2012.5,2012.0,]
import numpy as np
import matplotlib.pyplot as plt

engine = create_engine('sqlite:///data.db', echo=True)
Base.metadata.create_all(engine)

class Query:
    def __init__(self, period, dept, prof, course):
        self.period = period
        # in the format of [(20XX, semmester), (20XX, semmester)]
        self.dept = dept
        self.prof = prof
        self.course = course
        self.graph_made = False
        self.graph_path = "/"

    '''
    takes in query parameters and returns a list of a bunch of info

    [
        (responses, [grades], [effectiveness])
        .....
    ]
    '''

    def get_query(self):

        Session = sessionmaker(bind=engine)
        session = Session()

        # set up database
        q = session.query(Evaluation.responses, Evaluation.grades, Evaluation.effectiveness)

        # dept
        if(bool(self.dept) == True):
            print(self.dept)
            q = q.filter(Evaluation.dept == str(self.dept))

        # prof
        if(bool(self.prof) == True):
            print(self.prof)
            q = q.filter(Evaluation.prof == self.prof)

        # course
        if(bool(self.course) == True):
            print(self.course)
            q = q.filter(Evaluation.course == self.course)


        # period
        # make a list of all of the years of the request
        date_range = [self.period[0]]
        while date_range[-1] != self.period[1]:
            date_range.append(date_range[-1] -.5)

        # make a list of years that you don't want
        forbidden_dates = all_dates
        for allowed_date in date_range:
            forbidden_dates.remove(allowed_date)

        # remove all of forbidden_years from query
        for forbidden_date in forbidden_dates:
            q = q.filter(Evaluation.date != forbidden_date)

        return q

    def query_to_list(self, query):
        return query.all()

    def get_all_grades(self):

        # takes all the data and adds it together
        all_grades = [0,0,0,0,0,0,0,0,0,0,0,0]

        for responses, raw_grades in self.query_to_list(self.get_query()):
            for i, grade in enumerate(json.loads(raw_grades)):
                all_grades[i] += round(float(responses)*grade)

        return all_grades

    def get_all_ratings(self):

        all_ratings = [0,0,0,0,0]

        query_list = self.query_to_list(self.get_query)

        for _, _, ratings in query_list:
            for i, rating in enumerate(json.loads(ratings)):
                all_ratings[i] += ratings

        # normalize percentages so that 100% is 1
        for i, rating in enumerate(all_ratings):
            all_ratings[i] = rating/float(len(query_list))

        return all_ratings

    def get_easiest(self):
        pass

    def get_hardest(self):
        pass

    def get_best(self):
        pass

    def get_worst(self):
        pass



    def make_graph(self):
        if self.graph_made != True:

            # make graph
            raw = ('A','A-','B+','B','B-','C+','C','C-','D+','D','D-','FAILURE')
            grade_values = raw[::-1]
            y_pos = np.arange(len(grade_values))
            grades = self.get_all()
            grades.reverse()
            print(grades)

            y_pos = np.arange(len(grade_values))

            plt.bar(y_pos, grades, align='center', alpha=0.5)
            plt.xticks(y_pos, grade_values)
            plt.ylabel('students')
            plt.title('sheehan\'s creative outlet')

            plt.show()



            graph_path = "/"
            self.graph_made = True

    '''def get_graph_path(self):
        self.make_graph()
        return graph_path'''

if __name__ == '__main__':

    graph = Query((2016.5,2012.0),"PHYS", False, 133)
    graph.make_graph()
