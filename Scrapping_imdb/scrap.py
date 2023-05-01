from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
page = urllib.request.urlopen(url, timeout=5)

soup = bs(page, 'html.parser')
tbody = soup.find('tbody', {'class': 'lister-list'})
listMovies = []
titre = []

for tr in tbody.find_all('tr'):
    td = tr.find('td', {'class': 'titleColumn'})
    a = td.find('a')
    if a:
        titre = a.text
        date = td.find('span').text.strip('()')
        film = {'Titre': titre, 'Date': date}
        listMovies.append(film)

df = pd.DataFrame(listMovies)

# Ajouter une colonne pour les années arrondies à la décennie
df['Decennie'] = pd.cut(df['Date'].astype(int), bins=range(1920, 2026, 10), right=False)

# Compter le nombre de films par décennie
counts = df.groupby('Decennie')['Titre'].count()

# Tracer un graphique en barres
counts.plot(kind='bar', color='yellow', edgecolor='red', width=0.9)

plt.xlabel('Décennie')
plt.ylabel('Quantité')
plt.title('Nombre de meilleurs films par dizaine d\'années')
plt.savefig('graphique.png')
plt.show()


# Enregistrer les données dans un fichier CSV
df.to_csv('nombres.csv', index=False)

