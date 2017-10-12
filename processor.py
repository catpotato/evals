from query import *
import pandas as pd
import json
import copy

'''
to use this bad boy:

~~~

if you send a query like this, it will look through all the data

    > Processor(Query((2016.5,2011.0), False, False, False))

if you wanted to find the easiest course in all of the data, you write:

    > print(processor.get_processed_data()['course']['difficulty']['max'])
    > {'course': u'484', 'professor': u'Van Gulick', 'mean_effectiveness': 4.6500000000000004, 'dept': u'ME', 'grades': [21.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'mean_grade': 3.9595000000000002, 'effectiveness': [0.685, 0.28, 0.035, 0.0, 0.0]}

the easiest professor is similar:

    > print(processor.get_processed_data()['professor']['difficulty']['max'])
    > {'course': u'271', 'professor': u'Cohea', 'mean_effectiveness': 4.8900000000000006, 'dept': u'THTR', 'grades': [8.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'mean_grade': 3.9670000000000001, 'effectiveness': [0.89, 0.11, 0.0, 0.0, 0.0]}

you can even do the easiest department:

    > print(processor.get_processed_data()['professor']['difficulty']['max'])
    > {'course': u'210', 'professor': u'Luo', 'mean_effectiveness': 4.2949999999999999, 'dept': u'FLL', 'grades': [11.0, 11.0, 3.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'mean_grade': 3.7905000000000002, 'effectiveness': [0.49, 0.39, 0.065, 0.045, 0.0]}

~~~

you can change the time period like this (.5 means second semmester, .0 means first)

    > Processor(Query((2016.5,2013.5), False, False, False))

limit it to a professor like this

    > Processor(Query((2016.5,2013.5), False, False, 'Gil'))

limit it to a department like this:

    > Processor(Query((2016.5,2013.5), 'ART', False, 'Gil'))

and even a class if you want, but you will only get a single result

    > Processor(Query((2016.5,2013.5), 'ART', 206, 'Gil'))

also, the query object just needs to spit out a pandas dataframe, so we can change that if we want


'''


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

    def slice_me(self,x):
        return x[:-2]

    def percentages_to_people(self, x, responses):
        print(x)
        print(responses)


    def pre_process(self):

        # hi this is a confusing spaghetti code mess, you can attempt to dechiper it if you'd like but it will probably make no sense

        # makes new columns
        self.data['mean_grade'] = self.data['grades'].apply(lambda x : self.grade_avg(x))
        self.data['mean_effectiveness'] = self.data['effectiveness'].apply(lambda x : self.effectiveness_avg(x))
        #self.data['CRN'] = self.data['dept'] + self.data['course'] + self.data['section'].apply(lambda x: self.slice_me(x))

        # makes fun data for the ones we left out
        for filter_type, active in self.info.iteritems():

            # if the space in the query was left blank
            if bool(active) == False or bool(active) == True:

                max_dict = {"mean_grade" : 0, 'mean_effectiveness' : 0}
                min_dict = {"mean_grade" : 4, 'mean_effectiveness' : 5}

                stats = {'difficulty': {'max' : max_dict, 'min' : min_dict}, 'effectiveness': {'max' : max_dict, 'min' : min_dict}}

                for unique_type in self.data[filter_type].drop_duplicates():

                    # putting raw data in
                    unique_type_info = self.data.loc[self.data[filter_type] == unique_type]

                    # just so we get some id on the boy
                    info = copy.deepcopy(self.info)
                    info[filter_type] = unique_type
                    for key in info:
                        info[key] = unique_type_info[key].iloc[0]

                    # insert grade data for each professor
                    info['grades'] = [0,0,0,0,0,0,0,0,0,0,0,0]
                    for grades, responses in zip(unique_type_info['grades'], unique_type_info['responses']):
                        for (i, grade) in enumerate(grades):
                            info['grades'][i] += round(grade*float(responses))

                    # insert effectiveness data for each professor
                    info['effectiveness'] = [0,0,0,0,0]
                    divido = 0
                    for effectiveness in unique_type_info['effectiveness']:
                        divido += 1
                        for (i, rating) in enumerate(effectiveness):
                            info['effectiveness'][i] += rating

                    for (i, rating) in enumerate(info['effectiveness']):
                        info['effectiveness'][i] /= float(divido)


                    # putting averages for each group
                    info['mean_effectiveness'] = unique_type_info['mean_effectiveness'].mean()
                    info['mean_grade'] = unique_type_info['mean_grade'].mean()


                    # max difficulty
                    if info['mean_grade'] > stats['difficulty']['max']['mean_grade']:
                        stats['difficulty']['max']  = info

                    # min difficulty (its not going to be the min if it just was the max)
                    if info['mean_grade'] < stats['difficulty']['min']['mean_grade']:
                        stats['difficulty']['min'] = info

                    # max effectiveness
                    if info['mean_effectiveness'] > stats['effectiveness']['max']['mean_effectiveness']:
                        stats['effectiveness']['max'] = info

                    # min effectiveness (its not going to be the min if it just was the max)
                    if info['mean_effectiveness'] < stats['effectiveness']['min']['mean_effectiveness']:
                        stats['effectiveness']['min'] = info

                self.processed_data[filter_type] = stats


    def __init__(self, query):
        self.query = query
        self.info = {"dept": query.dept, "course": query.course, "professor": query.prof}
        self.data = query.get_query()
        self.processed_data = {}

        self.pre_process()

    def get_processed_data(self):
        return self.processed_data

if __name__ == '__main__':
    processor = Processor(Query((2016.5,2012.0), False, False, False))
    print(processor.get_processed_data()['professor']['difficulty']['min'])
