import pandas as pd
import os
import matplotlib.pyplot as plt
import pingouin as pg
import numpy as np

from config import BASEPATH

palette = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0']

WIDTH = 0.15
CLUSTER_NAMES = ['Frontal\nLeft', 'Frontal\nRight', 'Medial\nLeft', 'Medial\nRight']

def get_d_p(data_cluster):
    
    data_diff = data_cluster.query('type == "SEP"')
    data_same = data_cluster.query('type == "TOG"')
    
    results_mwu = pg.mwu(data_same['distance'].values, data_diff['distance'].values, 'greater')
    p_val= results_mwu['p-val'][0]
    
    d = pg.compute_effsize(data_same['distance'], data_diff['distance'], eftype='cohen')
    
    return(d, p_val)

#%% ALL SOUNDS TOGETHER
fig, axes = plt.subplots(2, 4, figsize = (12,6), sharey=True, sharex=True)
plt.suptitle("All sounds \n Cohen's d")

NORM_DIR = ['synch_2_norm/clusters_norm_together_v2', 'synch_2/clusters_norm_together_v2']
for i_norm, NORM in enumerate(NORM_DIR):
    CLUST_TYPE = NORM.split('/')[1]
    SYNCH_TYPE = NORM.split('/')[0]

    for i_lag, LAG in enumerate([0,1,2,5]):
        curr_ax = axes[i_norm, i_lag]
        plt.sca(curr_ax)
            
        for i_cluster, CLUSTER in enumerate(['FrontalLeft', 'FrontalRight', 'MedialLeft', 'MedialRight']):
            
            distances = []
            for i_distance, DISTANCE in enumerate(['cc']):
                x = i_cluster+i_distance*WIDTH
 
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
                
            plt.ylim(-.5, 0.6)
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
    curr_ax = axes[0, i_lag]
    curr_ax.set_title(f'LAG = {LAG}')
            

curr_ax.get_xaxis().set_ticks([0.3, 1.3, 2.3, 3.3])
curr_ax.get_xaxis().set_ticklabels(CLUSTER_NAMES)
axes[0, 0].set_ylabel('Normalized signals')
axes[1, 0].set_ylabel('Non-normalized signals')
plt.tight_layout()
