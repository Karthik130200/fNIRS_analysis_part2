import pandas as pd
import os
import matplotlib.pyplot as plt
import pingouin as pg
import numpy as np
np.random.seed(1234)
from config import BASEPATH

palette = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0']

WIDTH = 0.15
CLUSTER_NAMES = ['Frontal\nLeft', 'Frontal\nRight', 'Medial\nLeft', 'Medial\nRight']

def bootstrap(x, N=100, k=0.25, func=np.mean):
    n_samp = int(len(x)*k)
    
    out_dist = []
    for i in range(N):
        x_boost = np.random.choice(x, n_samp)
        out_dist.append(func(x_boost))
    
    return(out_dist)

def get_d_p(data_cluster):
    
    data_diff = data_cluster.query('type == "SEP"')
    data_same = data_cluster.query('type == "TOG"')
    
    same_boot = bootstrap(data_same['distance'].values)
    diff_boot = bootstrap(data_diff['distance'].values)
    
    results_mwu = pg.mwu(same_boot, diff_boot, 'greater')
    p_val= results_mwu['p-val'][0]
    
    d = pg.compute_effsize(same_boot, diff_boot, eftype='cohen')
    
    return(d, p_val)

#%% ALL SOUNDS TOGETHER
fig, axes = plt.subplots(1, 4, figsize = (12,3), sharey=True, sharex=True)

NORM = 'synch_2_norm/clusters_norm_together_v2'

results = []
iii=0
for i_lag, LAG in enumerate([0,1,2,5]):
    curr_ax = axes[i_lag]
    plt.sca(curr_ax)
        
    for i_cluster, CLUSTER in enumerate(['FrontalLeft', 'FrontalRight', 'MedialLeft', 'MedialRight']):
        
        distances = []
        for i_distance, DISTANCE in enumerate(['cc']):
            x = i_cluster+i_distance*WIDTH
            
            d_ = []
            p_ = []
        

            #load all stimuli
            data_all_sounds = []
            for SOUND in ['FEM_CRY', 'FEM_LAUGH', 'INF_CRY_HI', 'INF_CRY_LO', 'INF_LAUGH']:
    
                data_sound = pd.read_csv(f'{BASEPATH}/{NORM}/{DISTANCE}_{LAG}/{SOUND}.csv', index_col = 0)
    
                data_cluster = data_sound.query('cluster == @CLUSTER')
                
                #some pandas magic
                data_cluster_average = data_cluster.groupby(['dyad', 'type']).mean()
                data_cluster = data_cluster_average.reset_index()
                data_all_sounds.append(data_cluster)
            
            data_all_sounds = pd.concat(data_all_sounds, axis = 0)
            
            d, p = get_d_p(data_all_sounds)
            
            if p<0.05:
                plt.bar(x, d, width=0.9*WIDTH, color = palette[i_distance])
            else:
                plt.bar(x, d, width=0.9*WIDTH, color = 'white', edgecolor = palette[i_distance])
            
            distances.append(d)
            results.append(pd.DataFrame({'measure':DISTANCE, 'lag': LAG, 'cluster': CLUSTER, 'd':d, 'p':p}, index = [iii]))
            iii+=1
            
        # plt.ylim(-.5, 0.6)
        # plt.text(i_cluster+0.3, np.max(distances)+0.1, CLUSTER_NAME, ha='center', va='center', fontsize=9)
        plt.xlim(-0.2, 3.8)
        plt.hlines(0, -0.2, 3.5, 'k', linewidth=0.5)
        curr_ax.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
        curr_ax.spines['top'].set_visible(False)
        curr_ax.spines['right'].set_visible(False)
        curr_ax.spines['bottom'].set_visible(False)
        curr_ax.spines['left'].set_visible(True)
        curr_ax.get_xaxis().set_ticks([])
        curr_ax.tick_params(axis='x', bottom=False, top=False)

for i_lag, LAG in enumerate([0,1,2,5]):
    curr_ax = axes[i_lag]
    curr_ax.set_title(f'LAG = {LAG}')

curr_ax.get_xaxis().set_ticks([0.3, 1.3, 2.3, 3.3])
curr_ax.get_xaxis().set_ticklabels(CLUSTER_NAMES)
axes[0].set_ylabel("Cohen's d")
plt.tight_layout()

#%%
results = pd.concat(results, axis=0)
results.to_csv('synch_boot.csv')  #problem with the directory. So the csv file is saved in the scripts folder 



"""
   measure  lag       cluster         d             p
0       cc    0   FrontalLeft  0.406119  4.084926e-03
1       cc    0  FrontalRight  0.032447  4.586466e-01
2       cc    0    MedialLeft -0.075076  7.166691e-01
3       cc    0   MedialRight  0.243192  1.775317e-02
4       cc    1   FrontalLeft  0.365830  3.854965e-03
5       cc    1  FrontalRight -0.008003  4.985378e-01
6       cc    1    MedialLeft  0.054794  4.134484e-01
7       cc    1   MedialRight  0.311436  2.523654e-02
8       cc    2   FrontalLeft  0.414688  3.404407e-03
9       cc    2  FrontalRight -0.120395  7.656098e-01
10      cc    2    MedialLeft  0.496564  6.373665e-04
11      cc    2   MedialRight  0.831899  1.509043e-08
12      cc    5   FrontalLeft -0.245869  9.542137e-01
13      cc    5  FrontalRight -0.449111  9.993061e-01
14      cc    5    MedialLeft  1.037017  2.982400e-11
15      cc    5   MedialRight  1.523885  9.284476e-19
"""