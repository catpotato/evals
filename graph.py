import json
from evaluation import *
from operator import add
allowed_years = [2016.5,2016.0,2015.5,2015.0,2014.5,2014.0,2013.5,2013.0,2012.5,2012.0,]
import numpy as np
import matplotlib.pyplot as plt

engine = create_engine('sqlite:///data.db', echo=True)
Base.metadata.create_all(engine)

class Graph:
    def __init__(self, period, dept, prof, course):
        self.period = period
        # in the format of [(20XX, semmester), (20XX, semmester)]
        self.dept = dept
        self.prof = prof
        self.course = course
        self.graph_made = False
        self.graph_path = "/"

    def get_query(self):

        Session = sessionmaker(bind=engine)
        session = Session()

        # set up database
        q = session.query(Evaluation.responses, Evaluation.grades)

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
        year_range = [self.period[0]]
        while year_range[-1] != self.period[1]:
            year_range.append(year_range[-1] -.5)

        queries = []

        for raw_year in year_range:
            year = int(raw_year)
            semmester = int(40*(raw_year - float(year)) + 10)
            queries.append(q.filter(and_(Evaluation.year == year, Evaluation.semmester == semmester)))


        '''# from that make a list of all of the years you cant use
        forbidden_years = allowed_years
        for year in year_range:
            forbidden_years.remove(year)

        # then narrow your query down by eliminating the years that aren't allowed
        for raw_year in forbidden_years:
            year = int(raw_year)
            # weird math due to how the database is set up (semmester 1 is 10, semmester 2 is 30)
            semmester = int(40*(raw_year - float(year)) + 10)
            q = q.filter(and_(Evaluation.year != year, Evaluation.semmester != semmester))'''

        #q = q.filter(and_(Evaluation.year == 2015, Evaluation.semmester == 30))
        #q = q.filter(and_(Evaluation.year == 2015, Evaluation.semmester == 10))

        final = []
        for query in queries:
            final.extend(query.all())

        return final

    def get_data(self):

        # get grades
        all_grades = [0,0,0,0,0,0,0,0,0,0,0,0]
        # print(self.get_query())
        for responses, raw_grades in self.get_query():
            json.loads(raw_grades)
            #print(json.loads(raw_grades))

            grades = []
            for i, grade in enumerate(json.loads(raw_grades)):
                all_grades[i] += round(float(responses)*grade)


        return all_grades


    def make_graph(self):
        if self.graph_made != True:

            # make graph
            raw = ('A','A-','B+','B','B-','C+','C','C-','D+','D','D-','FAILURE')
            grade_values = raw[::-1]
            y_pos = np.arange(len(grade_values))
            grades = self.get_data()
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

    def get_graph_path(self):
        self.make_graph()
        return graph_path

if __name__ == '__main__':


    Session = sessionmaker(bind=engine)

    graph = Graph((2016.5,2012.0),"PHYS", False, 133)
    graph.make_graph()
