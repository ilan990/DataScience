import pandas as pd

# Charger le fichier CSV dans un dataframe
df = pd.read_csv('annonces.csv')

# Trouver les doublons basés sur la colonne DESCRIPTION
duplicates = df[df.duplicated(subset=['DESCRIPTION'], keep=False)]

# Supprimer les doublons basés sur la colonne DESCRIPTION
df.drop_duplicates(subset=['DESCRIPTION'], keep='first', inplace=True)

# Sauvegarder le dataframe dans un nouveau fichier CSV
df.to_csv('annonces_clean.csv', index=False)
