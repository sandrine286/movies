import pandas as pd
import numpy as np
from sklearn import decomposition
from sklearn import preprocessing
from sklearn.manifold import Isomap
from sklearn.neighbors import NearestNeighbors


class Reco(np.ndarray):
    def __new__(self, df):
        echantillon = df.drop(['Unnamed: 0', 'movie_title', 'genres',
                               'language', 'country', 'Couleur', 'imdb_score', 'movie_imdb_link'], axis=1)
        # préparation des données pour la modelisation
        X = echantillon.values
        # Centrage et Réduction
        std_scale = preprocessing.StandardScaler().fit(X)
        X_scaled = std_scale.transform(X)

        # Creation du modele isomap
        embedding = Isomap(n_components=15)
        res = embedding.fit_transform(X_scaled)
        new = res.view(self)
        return new

    def rechercheVoisin(self, nbVoisins, indFilm, df):
        neigh = NearestNeighbors(n_neighbors=nbVoisins)
        neigh.fit(self)
        print("\ntoto index de X : ", indFilm)
        # on construit un dataframe qui contiendra les films les plus proches du premier choix
        res = pd.DataFrame(columns=['movie_title', 'title_year', 'genres',
                                    'language', 'country', 'movie_imdb_link', 'imdb_score'])

        for i in range(nbVoisins):
            ind = neigh.kneighbors(self[indFilm])[1][0][i]
            print("\n toto index : ", ind)
            if (ind != indFilm):
                res = res.append(df[['movie_title', 'title_year', 'genres', 'language',
                                     'country', 'Couleur', 'movie_imdb_link', 'imdb_score']].iloc[ind])
        print(res.sort_values(['imdb_score'], ascending=False).head(10))
        return(res.sort_values(['imdb_score'], ascending=False).head(5))