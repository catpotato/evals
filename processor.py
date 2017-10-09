from query import *
import pandas as pd
import json

class Processor:


    def grade_avg(self, grades):

        mean = 0

        grade_values = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0]
        for grade_value, grade in zip(grade_values, grades):
            mean += grade_value*grade

        return mean

    def effectiveness_avg(self, effs):

        mean = 0

        eff_values = [5.0, 4.0, 3.0, 2.0, 1.0]
        for eff_value, eff in zip(eff_values, effs):
            mean += eff_value*eff_value

        return mean

    def pre_process(self):

        # makes new columns
        self.data['mean_grade'] = self.data['grades'].apply(lambda x : self.grade_avg(x))
        self.data['mean_effectiveness'] = self.data['effectiveness'].apply(lambda x : self.effectiveness_avg(x))
        self.data['CRN'] = self.data['dept'] + str(self.data['course'])

        # makes fun data for the ones we left out
        for key, values in self.info.iteritems():
            if bool(values) == False:
                all_keys = self.data[key].drop_duplicates()
                key_data = {}

                for unique_key in all_keys:

                    # putting raw data in
                    key_data[unique_key]['raw'] = self.data.loc[self.data[key] == unique_key]

                    # putting averages for each group
                    key_data[unique_key]['mean_effectiveness'] = key_data[unique_key]['raw']['mean_effectiveness'].mean()
                    key_data[unique_key]['mean_grade'] = key_data[unique_key]['raw']['mean_grade'].mean()

                self.processed_data[key] = key_data
                self.processed_data['max_easy'] 



        # prepare the fun data with






    def __init__(self, query):
        self.query = query
        self.info = {"dept": query.dept, "course": query.course, "professor": query.prof}
        self.data = pd.DataFrame(query.get_query())
        self.processed_data = {}

        self.pre_process()



    def get_min(self, column):

        min_key = "mean_" + column
        output = self.info

        for key, values in self.info.iteritems():
            if bool(values) == False:
                # fill in easiest for those who are missing
                output[key] = self.data.iloc[[self.data[min_key].idxmax()]][key]

        return output

    def get_max(self, column):

        max_key = "mean_" + column
        output = self.info

        for key, values in self.info.iteritems():
            if bool(values) == False:
                # fill in easiest for those who are missing
                self.fill_in_max(key)
                output[key] = self.data.iloc[[self.data[max_key].idxmax()]][key]

        return output

    def fill_in_max(self, key):




        '''if key == "dept":
            # add up all of the things from the same dept, and compare them
            pass

        if key == "course":
            # add up all of the courses that are the same and spit back the max
            all_courses = self.data.CRN.drop_duplicates()
            course_data = {

            }

            for course in all_courses:
                course_data[course] = self.data.loc[self.data['course'] == course]

            self.processed_data["course"] = course_data

        if key == "professor":

            # add up all of the porfessors that are the same and spit out the max
            all_profs = self.data.professor.drop_duplicates()
            prof_data = {

            }

            for prof in all_profs:
                prof_data[prof] = self.data.loc[self.data['professor'] == prof]

            self.processed_data["professor"] = prof_data'''



        '''
        data structure

        prof_data

        department_data

        course_data

        easiest_prof
        hardest_prof

        best_prof
        worst_prof




        '''



    def get_easiest(self):
        return self.get_max("grade")

    def get_hardest(self):
        return self.get_min("grade")

    def get_best(self):
        return self.get_max("effectiveness")

    def get_worst(self):
        return self.get_min("effectiveness")

if __name__ == '__main__':
    processor = Processor(Query((2016.5,2012.0),"PHYS", 133, False))
    print(processor.get_easiest()['professor'])
