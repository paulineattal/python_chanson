#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
#pou rla manipulation des dictionnaires
from gensim import corpora
from gensim.matutils import corpus2csc
import numpy as np
#pour la creation des graphes
import networkx as nx
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from imageio import imread


class Graph :
    def __init__(self, mots, titre, auteur):
        self.mots = mots
        self.titre = titre
        self.auteur = auteur
        
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre de la chanson : {self.titre}\nAuteur de la chanson : {self.auteur}\nParoles de la chanson : {self.mots}"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"
    
    #fonction qui construit un nuage de mots a l'aide de la librairie WordCloud
    def word_cloud(self, limit, sm_french) :
        
        fontcolor = '#000000' #couleur de la police
        bgcolor = '#ffffff' # couleur de fond
            
        wordcloud = WordCloud(
            max_words=limit,
            stopwords= sm_french, # liste de mots-outils
            mask=imread('img/mask.png'),
            contour_width=3,
            background_color=bgcolor
        ).generate(self.mots.lower()) 
        
        #sauvegarde dasn un pyplot
        fig = plt.figure()
        # taille de la figure
        fig.set_figwidth(5)
        fig.set_figheight(5)
        #titre de la figure
        title = "chasnson : " + self.titre + " par " + self.auteur
        
        #changer couleurs du texte
        def couleur(*args, **kwargs):
            return "rgb(0, 100, {})".format(random.randint(100, 255))
        
        plt.imshow(wordcloud.recolor(color_func=couleur))
        plt.title(title, color=fontcolor, size=10, y=1.01)
        plt.axis('off')
        #plt.show()
        return plt


    
class Clique(Graph) :
    def __init__(self, mots, titre, auteur, sous_mots):
        super().__init__(mots=mots, titre=titre, auteur=auteur)
        self.sous_mots = sous_mots #cette nouvelle variable sera calcule a la'ide de la methode LDA 
        
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        return f"Titre de la chanson : {self.titre}ntAuteur de la chanson : {self.auteur}\nParoles de la chanson : {self.mots}\nMots importants de la chanson : {self.sous_mots}"

    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        return f"{self.titre}, par {self.auteur}"

    # Fonction qui renvoie la variable sous_mots
    def get_sous_mots(self):
        return self.sous_mots
    
    #fonction qui contruit un graphe de mot a l'aide la librairie networkx
    def display_clique(self) :
        toks = [[tok for tok in self.mots.split() if tok in self.sous_mots]]
        
        dic = corpora.Dictionary(toks) # dictionnaire de tous les mots restant dans le token
        dfm = [dic.doc2bow(tok) for tok in toks]    
        term_matrice = corpus2csc(dfm)
        # Transposée de la matrice pour établir les cooccurrences
        term_matrice = np.dot(term_matrice, term_matrice.T)
        
        #sauvegarde dasn un pyplot
        fig = plt.figure()
        # taille de la figure
        fig.set_figwidth(5)
        fig.set_figheight(5)
        
        G = nx.from_scipy_sparse_matrix(term_matrice)
        G.add_nodes = dic
        pos=nx.spring_layout(G)  # position des nodes
        dic.cfs.values()
            
        nx.draw_networkx_nodes(G,pos, dic,
                      node_color='r',
                      node_size=500,
                      alpha=0.8)
        
        nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
        nx.draw_networkx_labels(G,pos,dic,font_size=8)
    
        return plt