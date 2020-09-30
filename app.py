# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from reco import Reco
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)


@app.route("/")
def hello():
    return "Le chemin de 'racine' est : " + request.path


dataFilms = pd.read_csv("Movies-cleaned.csv", sep=";")
echantillon_isomap = Reco(dataFilms)


@app.route('/movies/', methods=['GET', 'POST'])
def movies():
    if request.method == 'POST':
        film = request.form['titre']
        if len(film) == 0:
            return render_template('index.html', msg="Données obligatoire")
        choix = dataFilms[dataFilms['movie_title'].str.contains(
            film, case=False, regex=False)]

        if len(choix) > 0:
            choix = choix.sort_values(
                by='movie_title', ascending=False).head(1)
            indFilm = choix.index
            print("titi indice film : ", indFilm)
            res = echantillon_isomap.rechercheVoisin(
                10, indFilm, dataFilms)
            film = choix["movie_title"].iloc[0]
            return render_template('resultat.html',  titre=film, tables=[res.to_html(classes='data')], titles=res.columns.values)
        else:
            return render_template('index.html', msg="Film inconnu")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)