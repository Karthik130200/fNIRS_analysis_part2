#%% import
import pandas as pd
import os
import numpy as np
from physynch import compute_distance
from config import BASEPATH, get_distance, normalize_signal

import random
random.seed(1234)

#%% set params
DISTANCE= 'cc'

NORMALIZE = True

LAG_SECONDS = 2

#%%
OUTDIR = f'{BASEPATH}/synch_2_norm/channels/cc_2' #Computer for each lag
DATADIR = f'{BASEPATH}/channels'

os.makedirs(OUTDIR, exist_ok=True)

distance = get_distance(DISTANCE, LAG_SECONDS)

#%%
#for all sounds
for SOUND in ['FEM_CRY', 'FEM_LAUGH', 'INF_CRY_HI', 'INF_CRY_LO', 'INF_LAUGH']:
    for CONDITIONS in ['TOG','SEP']:
        dyads = os.listdir(f'{DATADIR}/{CONDITIONS}/{SOUND}')
        data_all = []
        indx = 0

	    #for all clusters
        for CHANNEL in np.arange(1,21):
            #for all dyads
            for DYAD in dyads:
                #for all repetitions
                for REP in [1,2,3]:
                    try: #not all dyads have all repetitions/sounds (?)
                        signal_m = pd.read_csv(f'{DATADIR}/TOG/{SOUND}/{DYAD}/M/CH{CHANNEL}/{REP}.csv').values.ravel()
                        signal_f = pd.read_csv(f'{DATADIR}/TOG/{SOUND}/{DYAD}/F/CH{CHANNEL}/{REP}.csv').values.ravel()
                        signal_m_surr = pd.read_csv(f'{DATADIR}/SEP/{SOUND}/{DYAD}/M/CH{CHANNEL}/{REP}.csv').values.ravel()
                        signal_f_surr = pd.read_csv(f'{DATADIR}/SEP/{SOUND}/{DYAD}/F/CH{CHANNEL}/{REP}.csv').values.ravel()
                        
                        if NORMALIZE:
                            signal_m = normalize_signal(signal_m.copy())
                            signal_f = normalize_signal(signal_f.copy())
                            signal_m_surr = normalize_signal(signal_m_surr.copy())
                            signal_f_surr = normalize_signal(signal_f_surr.copy())
    		            
                        signals_available = True
    		            
                    except:
                        print(f'{DYAD} - no repetition {REP}')
    		            
                    if signals_available:
    		            
                        dist = compute_distance(signal_m, signal_f, distance, detrend=False)
                        data_all.append(pd.DataFrame({'sound': SOUND, 
                                                      'dyad': DYAD, 
                                                      'channel': CHANNEL,
                                                      'repetition': REP, 
                                                      'type': 'TOG', 
                                                      'distance': dist}, index=[indx]))
                        indx+=1
            		                
                                
                        dist_surr = compute_distance(signal_m_surr, signal_f_surr, distance, detrend=False)
                        data_all.append(pd.DataFrame({'sound': SOUND, 
                                                      'dyad': DYAD,
                                                      'channel': CHANNEL,
                                                      'repetition': REP, 
                                                      'type': 'SEP', 
                                                      'distance': dist_surr}, index=[indx]))
                        indx+=1
    		    
    		    #end for all repetitions
    		    
		#end for all dyads
		
	    #end for all clusters
    data_all = pd.concat(data_all, axis = 0)
    data_all.to_csv(f'{OUTDIR}/{SOUND}.csv')
#end for all sounds
