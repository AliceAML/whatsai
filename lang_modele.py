import numpy as np

def modelisation(corpus):
    modele = proba_triplets(triplets(' '.join(corpus).split(' ')))
    return modele

def generation_phrases(modele) :
    historique = ["BEGIN","NOW"]
    while (historique[-1] != "END"):
        paire = (historique[-2],historique[-1])
        historique.append(sample_from_discrete_distrib(modele[paire]))
    return historique

def triplets(list):
    '''fonction qui à partir d’une liste de mots renvoie la liste des triplets
    successifs formés par ces mots'''
    triplets = []
    index = 0
    for word in list[:-2]:
        triplets.append((word, list[index+1], list[index+2]))
        index += 1
    return triplets

def proba_triplets(triplets):
    '''fonction qui à partir d’une liste de triplets (a, b, c) estime les probabilités p(c|a, b)'''
    proba = {} # on accédera aux mots suivants une paire a,b via un dictionnaire contenu dans proba["a b"]
    occur_paires = {} # pour compter les occurrences de ab, afin de calculer la fréquence

    for (a,b,c) in triplets :
        paire = (a,b)
        occur_paires[paire] = occur_paires.get(paire,0) + 1 # je décompte une occurrence supp de la paire
        proba[paire] = proba.get(paire, {}) # on crée un dictionnaire si nécessaire
        proba[paire][c] = proba[paire].get(c,0) + 1 
    
    # il faut maintenant transformer les fréquences absolues en fréquences relatives
    for paire, predictions in proba.items() :
        for mot, compte in predictions.items():
            proba[paire][mot] = compte/occur_paires[paire]
    
    return proba

def sample_from_discrete_distrib(distrib):
    words, probas = list(zip(*distrib.items()))
    return np.random.choice(words, p=probas)