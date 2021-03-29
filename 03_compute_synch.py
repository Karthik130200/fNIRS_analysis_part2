#%% import
import pandas as pd
import os
from physynch import compute_distance
from config import BASEPATH, get_distance, normalize_signal

import random
random.seed(1234)

#%% set params
CLUSTER_DIR = 'clusters_norm' #
DISTANCE= 'cc' #run on all sinchrony measures: cc, wc, dtw

NORMALIZE = True
SYNCH_TYPE = 'synch_norm'

signals_available = True

DATADIR = os.path.join(BASEPATH, CLUSTER_DIR)
    
#%%
for LAG_SECONDS in [0,1,2,5]:
    OUTDIR = os.path.join(BASEPATH, SYNCH_TYPE, CLUSTER_DIR, f'{DISTANCE}_{LAG_SECONDS}')
    os.makedirs(OUTDIR, exist_ok=True)
    
    distance = get_distance(DISTANCE, LAG_SECONDS)
    
    #for all sounds
    for SOUND in ['FEM_CRY', 'FEM_LAUGH', 'INF_CRY_HI', 'INF_CRY_LO', 'INF_LAUGH']:
        data_all = []
        indx = 0
        
        dyads = os.listdir(os.path.join(DATADIR, 'TOG', f'{SOUND}'))
    
        #for all clusters
        for CLUSTER in ['FrontalLeft', 'FrontalRight', 'MedialLeft', 'MedialRight']:
            
            #for all dyads
            for DYAD in dyads:
            
                #for all repetitions
                for REP in [1,2,3]: 
                
                    try: #not all dyads have all repetitions/sounds (?)
                        #signal_m/f----> TOG
                        signal_m = pd.read_csv(os.path.join(DATADIR, 'TOG', 
                                                            SOUND, DYAD, 'M',
                                                            CLUSTER, f'{REP}.csv'), 
                                               index_col=0).values.ravel()
                        
                        signal_f = pd.read_csv(os.path.join(DATADIR, 'TOG', 
                                                            SOUND, DYAD, 'F', 
                                                            CLUSTER, f'{REP}.csv'), 
                                               index_col=0).values.ravel()
                        
                        #signal_m/f_surr----> SEP
                        signal_m_surr = pd.read_csv(os.path.join(DATADIR, 'SEP', 
                                                                 SOUND, DYAD, 'M', 
                                                                 CLUSTER, f'{REP}.csv'), 
                                                    index_col=0).values.ravel()
                        
                        signal_f_surr = pd.read_csv(os.path.join(DATADIR, 'SEP',
                                                                 SOUND, DYAD, 'F', 
                                                                 CLUSTER, f'{REP}.csv'), 
                                                    index_col=0).values.ravel()
                        
                        #if this line of code is executed,
                        #then all the required signals have been loaded
                        signals_available = True
                        
                        if NORMALIZE:
                            signal_m = normalize_signal(signal_m.copy())
                            signal_f = normalize_signal(signal_f.copy())
                            signal_m_surr = normalize_signal(signal_m_surr.copy())
                            signal_f_surr = normalize_signal(signal_f_surr.copy())
		                
                    except:
                        print(f'{DYAD} - no repetition {REP}')
		                
                    if signals_available:

                        dist = compute_distance(signal_m, signal_f, 
                                                distance, detrend=False)
                        
                        data_all.append(pd.DataFrame({'sound': SOUND, 
                                                      'dyad': DYAD, 
                                                      'cluster': CLUSTER,
                                                      'repetition': REP, 
                                                      'type': 'TOG', 
                                                      'distance': dist}, 
                                                     index=[indx]))
                        indx+=1
    		                
                        dist_surr = compute_distance(signal_m_surr, signal_f_surr, 
                                                     distance, detrend=False)
                        
                        data_all.append(pd.DataFrame({'sound': SOUND, 
                                                      'dyad': DYAD,
                                                      'cluster': CLUSTER,
                                                      'repetition': REP, 
                                                      'type': 'SEP', 
                                                      'distance': dist_surr}, 
                                                     index=[indx]))
                        indx+=1
		        
    		        #end for all repetitions
    		        
            #end for all dyads
    		    
        #end for all clusterst
        data_all = pd.concat(data_all, axis = 0)
        data_all.to_csv(os.path.join(OUTDIR, f'{SOUND}.csv'))
    	#end for all sounds
        
#%%
"""
Trial run: I got this when I used print(data_all) in line 91 instead of data_all.to_csv(os.path.join(OUTDIR, f'{SOUND}.csv'))

            Below data are generated based on the conditions (LAG: 0,1; 
                                                              COND: TOG & SEP
                                                              CLUSTER: FrontalLeft;
                                                              REPETITION: 1,2,3)
                                                                  
       sound   dyad      cluster  repetition type  distance
0    FEM_CRY  SSC39  FrontalLeft           1  TOG  0.157792
1    FEM_CRY  SSC39  FrontalLeft           1  SEP  0.096944
2    FEM_CRY  SSC39  FrontalLeft           2  TOG  0.104818
3    FEM_CRY  SSC39  FrontalLeft           2  SEP -0.144953
4    FEM_CRY  SSC39  FrontalLeft           3  TOG -0.122349
..       ...    ...          ...         ...  ...       ...
283  FEM_CRY  SSC38  FrontalLeft           1  SEP -0.825472
284  FEM_CRY  SSC38  FrontalLeft           2  TOG  0.070692
285  FEM_CRY  SSC38  FrontalLeft           2  SEP  0.276350
286  FEM_CRY  SSC38  FrontalLeft           3  TOG  0.209915
287  FEM_CRY  SSC38  FrontalLeft           3  SEP  0.247046

[288 rows x 6 columns]


       sound   dyad      cluster  repetition type  distance
0    FEM_CRY  SSC39  FrontalLeft           1  TOG  0.159543
1    FEM_CRY  SSC39  FrontalLeft           1  SEP  0.172425
2    FEM_CRY  SSC39  FrontalLeft           2  TOG  0.133906
3    FEM_CRY  SSC39  FrontalLeft           2  SEP  0.032059
4    FEM_CRY  SSC39  FrontalLeft           3  TOG -0.023822
..       ...    ...          ...         ...  ...       ...
283  FEM_CRY  SSC38  FrontalLeft           1  SEP -0.705501
284  FEM_CRY  SSC38  FrontalLeft           2  TOG  0.184151
285  FEM_CRY  SSC38  FrontalLeft           2  SEP  0.354104
286  FEM_CRY  SSC38  FrontalLeft           3  TOG  0.414341
287  FEM_CRY  SSC38  FrontalLeft           3  SEP  0.448206

[288 rows x 6 columns]
"""
