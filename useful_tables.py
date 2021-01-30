"""
estracting useful tables
"""

import scraping_golarion
from scraping_golarion import Scraper

base_url = 'https://golarion.altervista.org'
id_zebra = 'wiki_table_zebra'

# find principal table
scr = Scraper(base_url + '/wiki/Oggetti_Magici')
scr.parse()
df_list = scr.get_table(id_zebra)

# correct table
table1 = df_list[0]
table1['Minore'] = table1['Minore'].str.replace('â', '-')
table1['Medio'] = table1['Medio'].str.replace('â', '-')
table1['Maggiore'] = table1['Maggiore'].str.replace('â', '-')

table1['Minore'] = table1['Minore'].str.replace('â', '-')
table1['Medio'] = table1['Medio'].str.replace('â', '-')
table1['Maggiore'] = table1['Maggiore'].str.replace('â', '-')

table1['Oggetto'].iloc[0] = 'Armature'

# find body table
scr = Scraper(base_url + '/wiki/Oggetti_Meravigliosi')
scr.parse()
df_list = scr.get_table(id_zebra)

table2 = scr.get_table(id_zebra)[0]

# find pergamene table
scr = Scraper(base_url + '/wiki/Pergamene')
scr.parse()
df_list = scr.get_table(id_zebra)

table3 = scr.get_table(id_zebra)[1]
table3 = table3[['Minore Inferiore', 'Minore Superiore', 'Medio Inferiore', 'Medio Superiore',
                 'Maggiore Inferiore', 'Maggiore Superiore', 'Livello Incantesimo']]
table3['Livello Incantesimo'] = table3['Livello Incantesimo'].str.replace('Â°', '')
table3['Livello Incantesimo'] = table3['Livello Incantesimo'].apply(int)

# find table pozioni
scr = Scraper(base_url + '/wiki/Pozioni')
scr.parse()
df_list = scr.get_table(id_zebra)

table4 = scr.get_table(id_zebra)[2]
table4 = table4[['Minore Inferiore', 'Minore Superiore', 'Medio Inferiore', 'Medio Superiore',
                 'Maggiore Inferiore', 'Maggiore Superiore', 'Livello Incantesimo']]
table4['Livello Incantesimo'] = table4['Livello Incantesimo'].str.replace('Â°', '')
table4['Livello Incantesimo'] = table4['Livello Incantesimo'].apply(int)
for column in table4.columns.values[:-2]:
    table4[column] = table4[column].str.replace('â', '-')

# find table bacchette
scr = Scraper(base_url + '/wiki/Bacchette')
scr.parse()
df_list = scr.get_table(id_zebra)

table5 = scr.get_table(id_zebra)[0]
table5 = table5[['Minore Inferiore', 'Minore Superiore', 'Medio Inferiore', 'Medio Superiore',
                 'Maggiore Inferiore', 'Maggiore Superiore', 'Livello incantesimo']]
table5['Livello incantesimo'] = table5['Livello incantesimo'].str.replace('Â°', '')
table5['Livello incantesimo'] = table5['Livello incantesimo'].apply(int)
for column in table4.columns.values[:-2]:
    table5[column] = table5[column].str.replace('â', '-')


print(table5)

# save
table1.to_csv('clean_data/Tabella_principale.csv', sep=',', index=False)
table2.to_csv('clean_data/Tabella_corpo.csv', sep=',', index=False)
table3.to_csv('clean_data/Tabella_Pergamene.csv', sep=',', index=False)
table4.to_csv('clean_data/Tabella_Pozioni.csv', sep=',', index=False)
table5.to_csv('clean_data/Tabella_Bacchette.csv', sep=',', index=False)