import pandas as pd
import os
import matplotlib.pyplot as plt
import pingouin as pg
import numpy as np

from config import BASEPATH

WIDTH = 0.3

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
fig, axes = plt.subplots(1, 1, figsize = (12,3),sharey=True, sharex=True)

axes.set_ylabel("Cohen's d", va='center', ha='center')

plt.sca(axes)

clusters = {'FrontalLeft': [3,5,6,10],
            'FrontalRight': [12,13,15,18],
            'MedialLeft': [0,1,2,4,7],
            'MedialRight': [9,14,16,17,19]}

for i_channel, CHANNEL in enumerate([3,5,6,10, '',
                                     12,13,15,18, '',
                                     0,1,2,4,7, '',
                                     9,14,16,17,19]):
    if CHANNEL != '':
        CH = CHANNEL+1
        #load all stimuli
        data_all_sounds = []
        for SOUND in ['FEM_CRY', 'FEM_LAUGH', 'INF_CRY_HI', 'INF_CRY_LO', 'INF_LAUGH']:
    
            data_sound = pd.read_csv(f'{BASEPATH}/synch_2_norm/channels/cc_2/{SOUND}.csv', index_col = 0)
    
            data_cluster = data_sound.query('channel == @CH')
            
            #some pandas magic
            data_cluster_average = data_cluster.groupby(['dyad', 'type']).mean()
            data_cluster = data_cluster_average.reset_index()
            data_all_sounds.append(data_cluster)
        
        data_all_sounds = pd.concat(data_all_sounds, axis = 0)
                
        d, p = get_d_p(data_all_sounds)
        
        if p<0.05:
            plt.bar(i_channel, d, width=WIDTH, color = '#2196F3')
        else:
            plt.bar(i_channel, d, width=WIDTH, color = 'white', edgecolor = '#2196F3')

plt.hlines(0, -1, 21, 'k', linewidth=0.5)
axes.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
axes.spines['top'].set_visible(False)
axes.spines['right'].set_visible(False)
axes.spines['bottom'].set_visible(False)
axes.spines['left'].set_visible(True)
plt.xticks(np.arange(0, 21), [4,6,7,11, '', 13,14,16,19, '', 1,2,3,5,8, '', 10,15,17,18,20])

axes.tick_params(axis='x', bottom=False, top=False)

for x_cluster, CLUSTER in zip([1.5, 6.5, 12, 18], 
                              ['Frontal\nLeft', 'Frontal\nRight', 'Medial\nLeft', 'Medial\nRight']):
    plt.text(x_cluster, 1.75, CLUSTER, ha = 'center', va='center')
plt.ylim(-1.5, 2)
plt.xlim(-1, 21)
plt.xlabel('Channels')

#%%
