from bs4 import BeautifulSoup as bs
import urllib.request
import pandas as pd

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
        listMovies.append(a.text)

titre = [{'Titre': x} for x in listMovies]

df = pd.DataFrame(titre)

df.to_csv('nombres.csv', index=False)



