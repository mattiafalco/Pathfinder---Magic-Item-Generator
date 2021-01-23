"""
This program creates a random generator for magic items
"""

import os
import pandas as pd
import random

random.seed(0)

class generator(object):
    """
    generator for magic items
    """

    princ_table = pd.read_csv('clean_data/Tabella_principale.csv')

    def __init__(self, clean_data):
        """
        :param clean_data: path of directory with magic items data
        """
        self.principal_dir = clean_data
        self.list_dir = []
        # list of all sub-directories
        for dir in os.listdir(self.principal_dir):
            if os.path.isdir(clean_data + '/' + dir) and (not dir.startswith('.')):
                self.list_dir.append(dir)
        self.list_dir.sort()

    def generate(self):
        pass

    def generate_from_type(self, type):
        """
        generate item of the given type
        """
        type_series = self.get_random_object(self.princ_table, from_column=type)
        type_item = type_series['Oggetto']

        print(type_item)

    def get_random_object(self, df, manuals='all', from_column='d%'):
        """
        :param df: dataFrame with one column named from_column
        :param manuals: list of consented manuals
        :param from_column
        :return: Pandas dataFrame, row of the random item
        """

        # filter by manuals
        if 'Fonte' in df.columns.values:
            filt = df['Fonte'].isin(manuals)
            df = df.loc[filt]
        # print(df)

        # get all possible choices
        avaible_choice = []
        intervals = {}
        for id, rnge in zip(df.index.values, df[from_column].values):
            rnge = rnge.split('-')
            if len(rnge) == 2 and rnge[0] != '':
                rnge = [int(num) for num in rnge]
                rnge = list(range(rnge[0], rnge[1] + 1))
                avaible_choice += rnge
                intervals[id] = rnge

        # pick a random number
        number = random.choice(avaible_choice)
        print(number)
        # print(intervals)

        # find the correspondent row
        for key, interval in zip(intervals, intervals.values()):
            if number in interval:
                idx = key
                break

        # print(idx)
        return df.loc[idx]

# test code
gen = generator('clean_data')

gen.generate_from_type('Minore')
