import pandas as pd
import os
import matplotlib.pyplot as plt
import pingouin as pg
import numpy as np
np.random.seed(1234)
from config import BASEPATH

palette = ['#2196F3', '#4CAF50', '#FF5722', '#9C27B0']

SIZE = 64
CLUSTER_NAMES = ['Frontal\nLeft', 'Frontal\nRight', 'Medial\nLeft', 'Medial\nRight']

data = pd.read_csv(f'{BASEPATH}/synch_boot.csv', index_col=0)

#%% ALL SOUNDS TOGETHER
fig, axes = plt.subplots(1, 4, figsize = (12,3), sharey=True, sharex=True)

NORM = 'synch_2_norm/clusters_norm_together_v2'

MARKERS = ['o', 's', 'D', 'v']

for i_distance, DISTANCE in enumerate(['cc']):
    data_distance = data.query("measure == @DISTANCE")
    curr_ax = axes[i_distance]
    plt.sca(curr_ax)
    
    for i_lag, LAG in enumerate([0,1,2,5]):    
        data_lag = data_distance.query("lag == @LAG")
        
        for i_cluster, CLUSTER in enumerate(['FrontalLeft', 'MedialLeft', 'MedialRight', 'FrontalRight']):
            data_cluster = data_lag.query("cluster == @CLUSTER")
            
            d = data_cluster['d'].values[0]
            p = data_cluster['p'].values[0]
            
            if p<0.05:
                plt.scatter([LAG], [d], s=SIZE, color = palette[i_distance], edgecolor='w', marker=MARKERS[i_cluster], alpha=1)
            else:
                plt.scatter([LAG], [d], s=SIZE, color = 'w', edgecolors = palette[i_distance], marker=MARKERS[i_cluster], alpha=1)
            
            
            
        # plt.ylim(-.5, 0.6)
        # plt.text(i_cluster+0.3, np.max(distances)+0.1, CLUSTER_NAME, ha='center', va='center', fontsize=9)
        plt.xlim(-2, 7)
        plt.hlines(0, -2, 7, 'k', linewidth=0.5)
        curr_ax.spines['top'].set_visible(False)
        curr_ax.spines['right'].set_visible(False)
        curr_ax.spines['bottom'].set_visible(False)
        curr_ax.spines['left'].set_visible(True)
        curr_ax.get_xaxis().set_ticks([0,1,2,5])
        curr_ax.tick_params(axis='x', bottom=False, top=False)
        curr_ax.grid(True, 'major', 'both', ls='--', lw=.5, c='k', alpha=.3)
        curr_ax.set_xlabel('Lag')
#%
for i_dist, DISTANCE in enumerate(['Cross Correlation', 'Mutual Information', 'Wavelet Coherence', 'Dynamic Time Warping']):
    curr_ax = axes[i_dist]
    curr_ax.set_title(DISTANCE)
            
axes[0].set_ylabel("Cohen's d")
plt.tight_layout()

#%%

