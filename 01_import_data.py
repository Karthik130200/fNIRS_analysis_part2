import pandas as pd
import numpy as np
import os
from config import BASEPATH

#%%
datafile = os.path.join(BASEPATH, 'original', 'SSC_TS.csv')
data = pd.read_csv(datafile)

dyads = ['SSC13', 'SSC16', 'SSC35', 'SSC37', 'SSC24', 'SSC38', 'SSC23', 
         'SSC34', 'SSC19', 'SSC25', 'SSC31', 'SSC33', 'SSC29', 'SSC15', 
         'SSC28', 'SSC39', 'SSC26', 'SSC12', 'SSC32', 'SSC21', 'SSC36', 
         'SSC27', 'SSC18', 'SSC20']

#% get sounds
sounds = data['sound'].unique()

#%%
for COND in ['SEP', 'TOG']:
    #%%
    for SOUND in sounds:
        #%%
        for DYAD in dyads:
            #%%
            for PARENT in ['M', 'F']:
                data_parent = data.query(f'cond == @COND & sound == @SOUND & ID == "{DYAD}{PARENT}"')
                idx_change = np.where(np.diff(data_parent['ts'])>1)[0]
                
                if len(idx_change) == 2: #strange data
                    i_st = 0
                    i_sp = idx_change[0]+1
                    data_1 = data_parent.iloc[i_st:i_sp]
                    data_1.drop(['ID', 'cond', 'sound'], axis=1, inplace=True)
                
                    i_st = i_sp
                    i_sp = idx_change[1]+1
                    data_2 = data_parent.iloc[i_st:i_sp]
                    data_2.drop(['ID', 'cond', 'sound'], axis=1, inplace=True)
                    
                    i_st = i_sp
                    data_3 = data_parent.iloc[i_st:]
                    data_3.drop(['ID', 'cond', 'sound'], axis=1, inplace=True)
                    
                    for CH in np.arange(1,21):            
                        data_1_ch = data_1[f'CH{CH}']
                        data_2_ch = data_2[f'CH{CH}']
                        data_3_ch = data_3[f'CH{CH}']
                        
                        if ~(data_1_ch.isna().any() | data_2_ch.isna().any() | data_3_ch.isna().any()):
                            
                            OUTDIR = os.path.join(BASEPATH, 'channels', COND, SOUND, DYAD, PARENT, f'CH{CH}')
                            os.makedirs(OUTDIR, exist_ok=True)
                            data_1_ch.to_csv(os.path.join(OUTDIR, '1.csv'), index=False, header=[f'CH{CH}'])
                            data_2_ch.to_csv(os.path.join(OUTDIR, '2.csv'), index=False, header=[f'CH{CH}'])
                            data_3_ch.to_csv(os.path.join(OUTDIR, '3.csv'), index=False, header=[f'CH{CH}'])
                        else:
                            print('nans', COND, SOUND, DYAD, PARENT, CH)
                        
                else:
                    print('bad ts', COND, SOUND, DYAD, PARENT, data_parent.shape)