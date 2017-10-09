from query import *
import pandas as pd

class

class Processor:

    def __init__(self, query):
        self.query = query
        self.info = {"dept": query.dept, "course": query.course, "prof": query.prof}
        self.data = pandas.DataFrame(query.get_query())


    def get_easiest(self):

        for key, values in self.info.iteritems():
            if bool(values) == False:
                self.fill_in_easiest(key)


        # case all are False
            # get easiest dept
            # get easiest course
            # get easier prof

        # case dept is defined
            # get easiest course
            # get easiest prof
        # case course is defined
            # get easiest prof
            # get easiest dept (N/A)
        # case professor is defined
            # get easiest dept (N/A)
            # get easiest course


        # case course and dept and defined
            # get easiest professor
        # case professor and dept are defined
            # get easiest course
        # case course and professor are defined
            # get easiest deparment

    def fill_in_easiest(self, key):

        if key == "dept":
            # fill in easiest dept

        elif key == "course":
            # fill in easiest course

        elif key == "prof":
            # fill in easiest prof



    def get_hardest():

    def get_best():

    def get_worst():
