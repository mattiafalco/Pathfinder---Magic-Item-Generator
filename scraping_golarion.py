# Import relevant libraries
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# create class scraper
class Scraper(object):
    """ Scraper class """

    def __init__(self, url):
        self.base_url = url
        response = requests.get(url)
        if response.status_code == 200:
            self.response = response
            self.soup = None
        else:
            raise ValueError(f"url doesn't respond, status code: {response.status_code}")

    def get_html(self):
        """ return html of the provided url"""
        return self.response.content

    def parse(self, parser='lxml'):
        """ parse the base url with the given parser """
        self.soup = BeautifulSoup(self.get_html(), features=parser)

    def find(self, obj, attr):
        if self.soup is not None:
            return self.soup.find(obj, attr)

    def find_all(self, obj, attr):
        if self.soup is not None:
            return self.soup.find_all(obj, attr)

    def get_table(self, id):
        """ read all table with the provided id

        returns: tables_df, list of lists of pd.DataFrame
        """
        tables = scr.find_all('table', {'id': id})
        tables_df = [pd.read_html(tab.prettify('utf-8'))[0] for tab in tables]
        # [0] is needed because read_html returns a list

        return tables_df


# Useful functions
def get_links(scraper):
    titles = ['Database Oggetti Magici e Meravigliosi', 'Armature Magiche',
                'Armi Magiche', 'Bacchette', 'Pergamene', 'Pozioni']

    # find table with links
    table = scraper.find('table', {'class': 'prd_capitoli'})

    # find all links
    links = [table.find('a', {'title': title}).get('href') for title in titles]

    links = [urljoin(scraper.base_url, link) for link in links]

    # create a dictionary
    links = dict(zip(titles, links))

    # modified links
    mod = ['Bacchette', 'Pergamene', 'Pozioni']
    for key in mod:
        if key == 'Pergamene':
            links[key] = links[key] + '_Arcane'
        else:
            links[key] = links[key] + '_Casuali'

    return links


if __name__ == '__main__':

    print('hello')
    id_zebra = 'wiki_table_zebra'
    id_filter = 'wiki_table_filter'


    base_url = 'https://golarion.altervista.org'
    scr = Scraper(base_url + '/wiki/Armi_Magiche')
    scr.parse()

    df_list = scr.get_table(id_zebra)
    df = df_list[1]
    print(df)
