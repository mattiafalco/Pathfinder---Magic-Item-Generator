"""
This program creates a random generator for magic items
"""

import os
import pandas as pd

class generator(object):
    """
    generator for magic items
    """
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

# test code
gen = generator('clean_data')

print(gen.list_dir)