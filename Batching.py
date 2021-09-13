import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
seed = 0
print()

# read csv
results = pd.read_csv('GoogleSearch.csv')
print('total number of results: %d'%(len(results)))

# exclude len(phrases) > 3 words)
results = results[results['cues'].str.count(' ')<3]
print('number of cues (with results) of length less than 4 words: %d'%(len(results)))

# log (base 10) bin results
results['log'] = np.log10(results['result']+results['compare'])
bin_max = math.ceil(results['log'].max())
hist, bins = np.histogram(results['log'], bins=range(bin_max+1))

# plot histogram
ax = results['log'].plot.hist(log=True, bins=bins, edgecolor='black')
ax.set_xlabel('log (base-10) of number of Google Search results')
ax.set_ylabel('number of cues per bin')
plt.savefig('histogram.png')

# get batch draft
get = 20
batch = None
print()
for b in bins[:-1]:
    _bin = results['cues'][(results['log']>b) & (results['log']<b+1)]
    if len(_bin) < get: 
        _get = len(_bin)
    else:
        _get = get
    print('number in bin 10^%d to 10^%d: %d'%(b, b+1, _get))
    _bin = _bin.sample(n=_get, replace=False, random_state=seed).to_list()
    if batch is None:
        batch = _bin.copy()
    else:
        batch += _bin
print()
print('total number in batch draft: %d'%(len(batch)))

## filter place names
#places = pd.read_csv('STR.csv')
#for place in places['feature']:
#    for cue in batch:
#        if place in cue:
#            batch.remove(cue)
#print(len(batch))

# save batch draft
batch = pd.DataFrame(batch)
batch.to_csv('batch.csv', index=False, header=False)

print()

