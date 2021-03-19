import numpy as np
from physynch import CrossCorrDistance, MIDistance, DTWDistance, WaveletCoherence
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns

#%%
clusters = {'FrontalLeft': [3,5,6,10],
            'FrontalRight': [12,13,15,18],
            'MedialLeft': [0,1,2,4,7],
            'MedialRight': [9,14,16,17,19]}

def plot_synchronies(data_cluster):
    #% all rep together
    data_diff = data_cluster.query('type == "diff"')
    data_same = data_cluster.query('type == "same"')
    
    results_mwu = pg.mwu(data_same['distance'].values, data_diff['distance'].values, 'greater')
    p_val= results_mwu['p-val'][0]
    
    d = pg.compute_effsize(data_same['distance'], data_diff['distance'], eftype='cohen')
    
    plt.hist(data_diff['distance'].values, density=True, color = 'r', alpha=0.25)
    plt.hist(data_same['distance'].values, density=True, color = 'g', alpha=0.25)
    
    plt.grid()
    
    ca = plt.gca()
    x_min, x_max = ca.get_xlim()
    x = x_min + 0.5*(x_max - x_min)
    
    y_min, y_max = ca.get_ylim()
    y = y_min + 0.85*(y_max - y_min)
    
    if p_val < 0.05:
        plt.text(x, y, 'p = {:.3f}, d = {:.3f}'.format(p_val, d), ha='center', fontweight='bold')
    else:
        plt.text(x, y, 'p = {:.3f}, d = {:.3f}'.format(p_val, d), ha='center')
    
def normalize_signal(x):
    return( (x-np.mean(x))/np.std(x))
    
def compute_cluster(x, normalize=False):
    if normalize:
        x = np.apply_along_axis(normalize_signal, 1, x)
    x_mean = np.mean(x, axis = 0)
    return(x_mean)

def get_distance(distance, LAG):
    
    LAG_SAMPLES = int(LAG*FSAMP)
    if distance == 'cc':
        dist = CrossCorrDistance(lag = LAG_SAMPLES,
                                 normalize = True)
    elif distance == 'dtw':
        if LAG == 0:
            LAG_SAMPLES = 1
        dist = DTWDistance(wsize = LAG_SAMPLES,
                           method = 'Euclidean',
                           step = 'asymmetric', 
                           wtype = 'sakoechiba', 
                           openend = True,
                           openbegin = True, 
                           normalize = True)

    elif distance == 'mi':
        dist = MIDistance(K=4,
                          lag = LAG_SAMPLES,
                          jarlocation = '/home/karthikeyan/Desktop/fNIRS_project/infodynamics-jar-1.4/infodynamics/infodynamics/measures/continuous/kraskov')
    
    elif distance == 'wc':
        dist = WaveletCoherence(dt = 1/FSAMP,
                                lag = LAG_SAMPLES,
                                normalize=True)

    return(dist)

BASEPATH = '/home/karthikeyan/data'
     
FSAMP = 7.81
DEMEAN = True
RESCALE = True
NORMALIZE = True


