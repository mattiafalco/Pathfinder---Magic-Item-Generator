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

        returns: tables_df, list of pd.DataFrame
        """
        tables = scr.find_all('table', {'id': id})
        tables_df = [pd.read_html(tab.prettify('utf-8'))[0] for tab in tables]
        # [0] is needed because read_html returns a list

        return tables_df


# Useful functions
def get_links(scraper):
    """ get desired links from a page with a table 'prd_capitoli'.

        return: dictionary of links"""

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


def save_table_csv(df, name):
    """ save a DataFrame to name.csv"""
    df.to_csv('data/' + name, sep=',', index=False)

if __name__ == '__main__':

    base_url = 'https://golarion.altervista.org'
    id_zebra = 'wiki_table_zebra'
    id_filter = 'wiki_table_filter'

    # links
    scr = Scraper(base_url + '/wiki/Oggetti_Magici')
    scr.parse()
    links = get_links(scr)

    keys = ['Database Oggetti Magici e Meravigliosi', 'Armature Magiche',
              'Armi Magiche', 'Bacchette', 'Pergamene', 'Pozioni']

    """Database Oggetti Magici:
        Oggetti Meravigliosi
        Anelli
        Bastoni
        Verghe"""

    scr = Scraper(links[keys[0]])
    scr.parse()
    df_list = scr.get_table(id_filter)
    save_table_csv(df_list[0], 'Database_Oggetti_Magici.csv')

    """Armi Magiche, Armature Magiche, Bacchette, Pergamene, Pozioni"""
    for i in range(1, len(links)):
        scr = Scraper(links[keys[i]])
        scr.parse()
        df_list = scr.get_table(id_zebra)

        # save all tables
        for j in range(0, len(df_list)):
            save_table_csv(df_list[j], keys[i] + '_' + str(j+1) + '.csv')
