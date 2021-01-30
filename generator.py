"""
This program creates a random generator for magic items
"""

import os
import pandas as pd
import random

random.seed(42)

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

    def generate(self, num_dice, dice, manuals='all'):
        """
        generate magic items

        :param num_dice: list of integers
        :param dice: list of integers
        :param manuals: list of str
        :return: dictionary of tuples
        """
        results = {}
        results['Minore'] = self.generate_multiple_items(num_dice[0], dice[0], 'Minore', manuals)
        results['Medio'] = self.generate_multiple_items(num_dice[1], dice[1], 'Medio', manuals)
        results['Maggiore'] = self.generate_multiple_items(num_dice[2], dice[2], 'Maggiore', manuals)

        return results

    def generate_multiple_items(self, num_dice, dice, type, manuals='all'):
        """ generate multiple item from the given dices"""
        dice_results = sum([random.choice(range(1, dice+1)) for _ in range(num_dice)])
        items = [self.generate_from_type(type, manuals) for _ in range(dice_results)]
        return items
        #print(dice_results)
        #print(items)

    def generate_from_type(self, type, manuals='all'):
        """
        generate item of the given type
        """

        check = True

        while check:
            # load df
            data_df, type_item = self.get_type_item(type)

            # get item
            try:
                item = self.get_random_object(data_df, manuals)
                check = False
            except ValueError:
                pass

        # add price for Armi, Armature
        #if type_item == 'Armi' or type_item == 'Armature':
        #    pass

        return type_item, item

    def get_type_item(self, type):
        """ get a random type of item dataFrame"""
        type_series = self.get_random_object(self.princ_table, from_column=type)
        type_item = type_series['Oggetto']
        # print(type_item)

        # get correct file
        file = self.get_file(type_item, type)
        # print(file)

        # load df
        data_df = pd.read_csv('clean_data/' + type_item + '/' + file)

        return data_df, type_item

    def get_random_object(self, df, manuals='all', from_column='d%'):
        """
        :param df: dataFrame with one column named from_column
        :param manuals: list of consented manuals
        :param from_column
        :return: Pandas dataFrame, row of the random item
        """

        # filter by manuals
        if 'Fonte' in df.columns.values:
            if manuals != 'all':
                filt = df['Fonte'].isin(manuals)
                df = df.loc[filt]
                if sum(filt)==0:
                    raise ValueError
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
        # print('Numero estratto:', number)
        # print(intervals)

        # find the correspondent row
        for key, interval in zip(intervals, intervals.values()):
            if number in interval:
                idx = key
                break

        return df.loc[idx]

    def get_file(self, type_item, type):
        """
        :param type_item: string,type of item (Arma, ...)
        :param type: string, (Minore, ...)
        :return: string, correct file for the given item
        """
        legend = {'Anelli':'direct', 'Armature':'direct', 'Armi':'direct',
                  'Bacchette':'indirect', 'Bastoni':'direct', 'Oggetti meravigliosi':'special',
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

        if type_item == 'Pergamene':
            type_item += '_arcane'

        file = type_item + '_' + rarity + '_' + 'lv' + str(level) + '.csv'
        return file

    def special_search(self, type_item, type):

        # Oggetti meravigliosi
        if type_item == 'Oggetti meravigliosi':
            subtype = random.choice(['inferiori', 'superiori'])
            body_df = pd.read_csv('clean_data/Tabella_corpo.csv')
            body = self.get_random_object(body_df)[-1]

            if body != 'Senza Slot':
                file = 'Oggetti_Slot_' + body + '_' + self.convert_type(type) + '_' + subtype + '.csv'
            else:
                body = body.replace(' ', '_')
                file = 'Oggetti_' + body + '_' + self.convert_type(type) + '_' + subtype + '.csv'

            return file

    def add_price(self, df, df_price):
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
# print(gen.get_file('Armi', 'Medio'))
# print(gen.generate_from_type('Maggiore', manuals=['Manuale di Gioco']))
# gen.generate_multiple_items(1, 6, 'Medio', manuals=['Manuale di Gioco'])
res = gen.generate([2,2,1], [6,3,2], manuals=['Manuale di Gioco'])

# print(res['Minore'])
# print(res['Medio'])
# for item in res['Maggiore']:
#    print(item[1]['Oggetto'])