from query import *
import pandas as pd
import json
import copy

'''
to use this bad boy:

send a query like this

Query((2016.5,2012.0),False, False, False)

'''

class Performace:


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
            mean += eff_value*eff

        return mean

    def pre_process(self):

        # hi this is a confusing spaghetti code mess, you can attempt to dechiper it if you'd like but it will probably make no sense

        # makes new columns
        self.data['mean_grade'] = self.data['grades'].apply(lambda x : self.grade_avg(x))
        self.data['mean_effectiveness'] = self.data['effectiveness'].apply(lambda x : self.effectiveness_avg(x))
        self.data['CRN'] = self.data['dept'] + self.data['course']
        # print(self.data['CRN'])

        # makes fun data for the ones we left out
        for filter_type, active in self.info.iteritems():

            # if the space in the query was left blank
            if bool(active) == False:

                filtered_data = {}

                stats = {'difficulty': {'max' : [self.info, 0], 'min' : [self.info, 4.0]}, 'effectiveness': {'max' : [self.info, 0], 'min' : [self.info, 4.0]}}

                for unique_type in self.data[filter_type].drop_duplicates():

                    stats[unique_type] = {}

                    # putting raw data in
                    unique_type_info = self.data.loc[self.data[filter_type] == unique_type]

                    # putting averages for each group
                    stats[unique_type]['mean_effectiveness'] = unique_type_info['mean_effectiveness'].mean()
                    stats[unique_type]['mean_grade'] = unique_type_info['mean_grade'].mean()

                    # just so we get some id on the boy
                    temp_info = copy.deepcopy(self.info)
                    temp_info[filter_type] = unique_type

                    # max difficulty
                    if stats[unique_type]['mean_grade'] > stats['difficulty']['max'][1]:
                        stats['difficulty']['max']  = [temp_info, stats[unique_type]['mean_grade']]

                    # min difficulty (its not going to be the min if it just was the max)
                    if stats[unique_type]['mean_grade'] < stats['difficulty']['min'][1]:
                        stats['difficulty']['min'] = [temp_info, stats[unique_type]['mean_grade']]

                    # max effectiveness
                    if stats[unique_type]['mean_effectiveness'] > stats['effectiveness']['max'][1]:
                        stats['effectiveness']['max'] = [temp_info, stats[unique_type]['mean_effectiveness']]

                    # min effectiveness (its not going to be the min if it just was the max)
                    if stats[unique_type]['mean_effectiveness'] < stats['effectiveness']['min'][1]:
                        stats['effectiveness']['min'] = [temp_info, stats[unique_type]['mean_effectiveness']]

                self.processed_data[filter_type] = stats


    def __init__(self, query):
        self.query = query
        self.info = {"dept": query.dept, "course": query.course, "professor": query.prof}
        self.data = pd.DataFrame(query.get_query())
        self.processed_data = {}

        self.pre_process()

    def get_processed_data(self):
        return self.processed_data

if __name__ == '__main__':
    processor = Processor(Query((2016.5,2014.0), "ART", False, False))
    print(processor.get_processed_data())
