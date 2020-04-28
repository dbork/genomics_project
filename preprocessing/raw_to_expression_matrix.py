import numpy as np
import os
import pandas as pd
import sys

if len(sys.argv) != 2:
	print 'Usage: python raw_to_expression_matrix.py <subdirectory>'
	sys.exit()

subdir = sys.argv[1]

#f = open('/Users/dbork/Documents/genomics_project/code/data/{}/preprocessed.txt'.format(subdir), 'w')
  
filenames = os.listdir('/Users/dbork/Documents/genomics_project/code/data/{}/'.format(subdir))
celltypes = []
for name in filenames:
	celltypes.append(name.split('/')[-1].split('_')[1])

#index = pd.MultiIndex.from_arrays([celltypes, filenames], 
print filenames[:10]
print celltypes[:10]

#for filename in os.listdir('/Users/dbork/Documents/genomics_project/code/data/{}/'.format(subdir)):
#	print filename
