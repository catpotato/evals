from query import *
import pandas as pd
import json
import copy

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

        # hi this is a confusing spaghetti code mess, you can attempt to dechiper it if you'd like but it will probably make no sense

        # makes new columns
        self.data['mean_grade'] = self.data['grades'].apply(lambda x : self.grade_avg(x))
        self.data['mean_effectiveness'] = self.data['effectiveness'].apply(lambda x : self.effectiveness_avg(x))
        self.data['CRN'] = self.data['dept'] + str(self.data['course'])

        # makes fun data for the ones we left out
        for key, values in self.info.iteritems():
            if bool(values) == False:
                all_keys = self.data[key].drop_duplicates()
                key_data = {}
                self.processed_data[key] = {}

                # pre stuff

                max_difficulty = [self.info, 0]
                min_difficulty = [self.info, 4.0]
                max_effectiveness = [self.info, 0]
                min_effectiveness = [self.info, 4.0]

                self.processed_data[key]['difficulty'] = {}
                self.processed_data[key]['effectiveness'] = {}

                for unique_key in all_keys:

                    key_data[unique_key] = {}

                    # putting raw data in
                    key_data[unique_key]['raw'] = self.data.loc[self.data[key] == unique_key]

                    # putting averages for each group
                    key_data[unique_key]['mean_effectiveness'] = key_data[unique_key]['raw']['mean_effectiveness'].mean()
                    key_data[unique_key]['mean_grade'] = key_data[unique_key]['raw']['mean_grade'].mean()

                    # just so we get some id on the boy
                    temp_info = copy.deepcopy(self.info)
                    temp_info[key] = unique_key

                    # max difficulty
                    if key_data[unique_key]['mean_grade'] > max_difficulty[1]:
                        max_difficulty = [temp_info, key_data[unique_key]['mean_grade']]

                    # min difficulty (its not going to be the min if it just was the max)
                    if key_data[unique_key]['mean_grade'] < min_difficulty[1]:
                        min_difficulty = [temp_info, key_data[unique_key]['mean_grade']]

                    # max effectiveness
                    if key_data[unique_key]['mean_effectiveness'] > max_effectiveness[1]:
                        max_effectiveness = [temp_info, key_data[unique_key]['mean_effectiveness']]

                    # min effectiveness (its not going to be the min if it just was the max)
                    if key_data[unique_key]['mean_effectiveness'] < min_effectiveness[1]:
                        min_effectiveness = [temp_info, key_data[unique_key]['mean_effectiveness']]



                self.processed_data[key]['data'] = key_data

                self.processed_data[key]['difficulty']['max'] = max_difficulty
                self.processed_data[key]['difficulty']['min'] = min_difficulty

                self.processed_data[key]['effectiveness']['max'] = max_effectiveness
                self.processed_data[key]['effectiveness']['max'] = min_effectiveness


    def __init__(self, query):
        self.query = query
        self.info = {"dept": query.dept, "course": query.course, "professor": query.prof}
        self.data = pd.DataFrame(query.get_query())
        self.processed_data = {}

        self.pre_process()

    def get_processed_data(self):
        return self.processed_data

if __name__ == '__main__':
    processor = Processor(Query((2016.5,2012.0),False, False, False))
    print(processor.get_processed_data()['professor']['difficulty']['max'])
