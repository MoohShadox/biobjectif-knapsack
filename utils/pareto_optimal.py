import numpy as np
import matplotlib.pyplot as plt


def pareto_optimal_naif(cout) -> np.ndarray :
    Choosen = np.ones(cout.shape[0]).astype(bool)
    i = 0
    for c in cout:
        #Ce ET vaut 1 si tout les coûts avant i et aprés i sont plus grand que c auquel cas on choisi le point.
        Choosen[i] = np.logical_and(np.all(np.any(cout[:i]>c, axis=1)),np.all(np.any(cout[i+1:]>c, axis=1))) 
        i = i + 1
    return cout[Choosen, :]

def pareto_optimal_ameliore(couts : np.ndarray) -> np.ndarray:
    Choosen = np.ones(couts.shape[0], dtype = bool) #Vecteur de ce qu'on choisi initialement a True pour tout
    for i, c in enumerate(couts):
        if Choosen[i]: #Si quelque chose a déja été retiré on le test pas.
            Choosen[Choosen] = np.any(couts[Choosen]<c, axis=1)  #Tout les points meilleurs que le point courant restent
            Choosen[i] = True  # Et le point courant reste bien-sur (vu que de base il était efficace)
    return couts[Choosen, :]

def pareto_optimal_MO(couts : np.ndarray):
    or_couts = couts
    n_points = couts.shape[0] #nombre de points
    Choosen = np.arange(n_points) #non plus un vecteur de 1 mais d'indices dans lesquels chercher
    to_check = 0 
    while to_check<len(couts):
        Efficaces = np.any(couts<couts[to_check], axis=1) #Masque des points efficaces jusque la
        Efficaces[to_check] = True #Le courant est efficace
        Choosen = Choosen[Efficaces]  #On garde les efficaces
        couts = couts[Efficaces] #On retire les coûts de ce qui est non dominé
        """
        On met a jour le nouvel indice a checker par le nombre de points efficaces avant l'indice courant + 1
        On comprend que si tout les points sont a garder avant l'indice courant on passe simplement a l'indice suivant.
        """
        to_check = Efficaces[:to_check].sum()+1 
    m = np.zeros(n_points).astype(bool)
    m[Choosen] = True
    return or_couts[m, :]

lex_sort = lambda x:x[np.lexsort(np.rot90(x))]

def pareto_front_sorted(v):
    s_v = lex_sort(v)
    msq = np.ones(s_v.shape[0]).astype(bool)
    min_pos = 0
    for i,x in enumerate(s_v):
        #Si c'est plus grand que le minimum de la deuxième étant donné que c'est forcément plus grand sur la première on supprime
        if x[1] > s_v[min_pos][1]:
            msq[i] = False
        #Mettre a jour le minimum de la deuxième colonne
        if(x[1] < s_v[min_pos][1]):
            min_pos = i
    return s_v[msq, :]

def masque_pareto_optimal_ameliore(couts : np.ndarray) -> np.ndarray:
    Choosen = np.ones(couts.shape[0], dtype = bool) #Vecteur de ce qu'on choisi initialement a True pour tout
    for i, c in enumerate(couts):
        if Choosen[i]: #Si quelque chose a déja été retiré on le test pas.
            Choosen[Choosen] = np.any(couts[Choosen]<c, axis=1)  #Tout les points meilleurs que le point courant restent
            Choosen[i] = True  # Et le point courant reste bien-sur (vu que de base il était efficace)
    return Choosen

def pareto_front_sorted_ameliore(couts):
    couts_o = couts
    ixs = np.argsort((couts).sum(axis=1))
    couts = couts[ixs]
    is_efficient = masque_pareto_optimal_ameliore(couts)
    is_efficient[ixs] = is_efficient.copy()
    return couts_o[is_efficient,:]

def tirer(m,n=10):
    return np.random.normal(loc=m, scale=m/4+1e-10, size=(n,2))