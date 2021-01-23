"""
estracting useful tables
"""

import scraping_golarion
from scraping_golarion import Scraper

base_url = 'https://golarion.altervista.org'
id_zebra = 'wiki_table_zebra'

# find table
scr = Scraper(base_url + '/wiki/Oggetti_Magici')
scr.parse()
df_list = scr.get_table(id_zebra)

# correct table
table = df_list[0]
table['Minore'] = table['Minore'].str.replace('â', '-')
table['Medio'] = table['Medio'].str.replace('â', '-')
table['Maggiore'] = table['Maggiore'].str.replace('â', '-')

table['Minore'] = table['Minore'].str.replace('â', '-')
table['Medio'] = table['Medio'].str.replace('â', '-')
table['Maggiore'] = table['Maggiore'].str.replace('â', '-')


print(table)
# save
table.to_csv('clean_data/Tabella_principale.csv', sep=',', index=False)