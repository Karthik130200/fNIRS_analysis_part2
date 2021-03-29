import pandas as pd
import os
import matplotlib.pyplot as plt
import pingouin as pg
import numpy as np
from statsmodels.stats.power import TTestIndPower
from config import BASEPATH

def compute_power(effect_sizes, n_samples, alpha=0.05):
    # perform power analysis
    analysis = TTestIndPower()
    
    powers = []
    for n in n_samples:
        powers.append(analysis.solve_power(d, power=None, 
                                       nobs1=n, ratio=1.0, 
                                       alpha=alpha))
    return(powers)

n_samples = np.arange(5,1000)

effect_sizes = [0.15, 0.2, 0.25, 0.3, 0.35]
for d in effect_sizes:
    powers = compute_power(d, n_samples)
    plt.plot(n_samples, powers)
        
plt.legend(effect_sizes)
plt.xscale('log')
plt.xticks([5, 10, 20, 50, 100, 200, 500, 1000],
           [5, 10, 20, 50, 100, 200, 500, 1000])
plt.grid()
plt.xlabel('Number of dyads')
plt.ylabel('Power')
