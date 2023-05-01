from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import re
import requests

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
        idMovie = re.search(r'(tt\d+)', str(a)).group(1)
        titre = a.text

        # Appel de l'api OMDB
        url = 'http://www.omdbapi.com/?i=' + idMovie + '&apikey=b4d62f57'
        response = requests.get(url)
        donnee = response.json()
        film = {'id': idMovie, 'Titre': titre, 'Date': donnee['Year'], 'Pays': donnee['Country'],
                'Director': donnee['Director'], 'acteurs': donnee['Actors'], 'note': donnee['imdbRating']}
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

df['Pays'] = df['Pays'].apply(lambda x: x.split(',')[0].strip())
counts = df.groupby('Pays')['Titre'].count().nlargest(5)
counts.plot(kind='bar', color='yellow', edgecolor='red', width=0.9)

plt.xlabel('Pays')
plt.ylabel('Quantité')
plt.title('Nombre de meilleurs films par Pays')
plt.savefig('pays.png')
plt.show()

# Enregistrer les données dans un fichier CSV
df.to_csv('nombres.csv', index=False)
