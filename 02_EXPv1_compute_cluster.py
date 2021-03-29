import numpy as np
import pandas as pd
import os
from config import BASEPATH, clusters, compute_cluster

N_MIN_CLUSTER = 3
NORMALIZE = True

#%%
datadir = os.path.join(BASEPATH, 'channels')
outdir = os.path.join(BASEPATH, 'clusters_norm')

#%%
metadata_all = []

for condition in ['TOG','SEP']:    
    for sound in ['FEM_CRY', 'FEM_LAUGH', 'INF_CRY_HI', 'INF_CRY_LO', 'INF_LAUGH', 'STATIC']:
        dyads = os.listdir(os.path.join(datadir, condition, sound))
        
        for dyad in dyads:
            
            for member in ['M', 'F']:
                
                for (cluster_name, cluster_channels) in clusters.items():
                    cluster_channels = np.array(cluster_channels)
                    
                    for repetition in [1,2,3]:
    
                        data_cluster = []
                        id_channels = []
                        for ch in cluster_channels:
                            try:
                                data_ch = pd.read_csv(os.path.join(datadir, condition, sound,
                                                                   dyad, member, f'CH{ch+1}', 
                                                                   f'{repetition}.csv')).values.ravel()
                            
                                std_channel = np.std(data_ch)
                                if std_channel != 0:
                                    data_cluster.append(data_ch)
                                    id_channels.append(ch+1)
                                    
                            except:
                                print(os.path.join(condition, sound, dyad, member, 
                                                   f'CH{ch+1}', f'{repetition}.csv'), 'NOT FOUND')
                        
                        if len(data_cluster)>=N_MIN_CLUSTER:
                            os.makedirs(os.path.join(outdir, condition, sound, dyad, member, cluster_name), exist_ok=True)
                            
                            data_cluster = np.array(data_cluster)
                            signal_cluster = compute_cluster(data_cluster, NORMALIZE)
                            
                            signal_cluster_pd = pd.DataFrame(signal_cluster, columns = ['data'])
                            signal_cluster_pd.to_csv(os.path.join(outdir, condition, sound, dyad, member,
                                                                  cluster_name, f'{repetition}.csv'))
                            
                            metadata_sub = {'condition': condition,
                                            'sound': sound,
                                            'dyad': dyad,
                                            'member': member,
                                            'cluster': cluster_name,
                                            'repetition': repetition,
                                            'N': len(data_cluster),
                                            'channels': '~'.join(np.array(id_channels).astype(str))}
                            metadata_all.append(metadata_sub)

#%%
metadata_all = pd.DataFrame(metadata_all)
metadata_all.to_csv(os.path.join(outdir, 'metadata_clusters.csv'))