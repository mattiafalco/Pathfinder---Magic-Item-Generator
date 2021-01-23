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

    def generate(self, num_dice, dice):
        pass

    def generate_multiple_items(self, num_dice, dice, type):
        pass

    def generate_from_type(self, type):
        """
        generate item of the given type
        """
        type_series = self.get_random_object(self.princ_table, from_column=type)
        type_item = type_series['Oggetto']

        print(type_item)
        pass

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

    def get_file(self, type_item, type):
        """
        :param type_item: string,type of item (Arma, ...)
        :param type: string, (Minore, ...)
        :return: string, correct file for the given item
        """
        legend = {'Anelli':'direct', 'Armature':'special', 'Armi':'special',
                  'Bacchette':'indirect', 'Bastoni':'direct', 'Oggetti meravigliosi':'direct',
                  'Pergamene':'indirect', 'Pozioni':'indirect', 'Verghe':'direct'}

        # direct search
        if legend[type_item] == 'direct':
            file = self.direct_search(type_item, type)

        # indirect search
        if legend[type_item] == 'indirect':
            file = self.indirect_search(type_item, type)

        if legend[type_item] == 'special':
            file = self.special_search(type_item, type)

        return file

    def direct_search(self, type_item, type):
        """
        :param type_item: str
        :param type: str
        :return: file with direct method
        """
        subtype = random.choice(['inferiori', 'superiori'])
        file = type_item + '_' + self.convert_type(type) + '_' + subtype + '.csv'
        return file

    def indirect_search(self, type_item, type):
        """
        :param type_item: str
        :param type: str
        :return: file with indirect method
        """
        subtype = random.choice(['Inferiore', 'Superiore'])

        # read table
        ref_table = pd.read_csv('clean_data/Tabella_' + type_item + '.csv')

        # estract level
        column = type + ' ' + subtype
        row = self.get_random_object(ref_table, from_column=column)
        level = row.iloc[-1]

        # rarity
        rarity = random.random()
        rarity = 'comuni' if rarity <= 0.75 else 'non_comuni'

        file = type_item + '_' + rarity + '_' + 'lv' + str(level) + '.csv'
        return file

    def special_search(self, type_item, type):
        pass


    def convert_type(self, type):
        if type == 'Minore':
            return 'minori'
        elif type == 'Medio':
            return 'medi'
        elif type == 'Maggiore':
            return 'maggiori'

# test code
gen = generator('clean_data')

# gen.generate_from_type('Minore')
print(gen.get_file('Verghe', 'Medio'))