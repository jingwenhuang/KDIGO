import numpy as np
from scipy.spatial.distance import squareform
from kdigo_funcs import pairwise_dtw_dist as ppd
from kdigo_funcs import arr2csv
import os

#------------------------------- PARAMETERS ----------------------------------#
#root directory for study
base_path = '/Users/taylorsmith/Google Drive/Documents/Work/Workspace/Kidney Pathology/KDIGO_eGFR_traj/'
sep = 'icu/'
id_fname = 'ex_keep_ids.txt'

#base for output filenames
res_base = 'test'
#-----------------------------------------------------------------------------#
#generate paths and filenames
data_path = base_path+'DATA/'+sep

res_path = base_path+'RESULTS/'+sep
if not os.path.exists(res_path):
    os.makedirs(res_path)

dmname = res_path+res_base+'_dm.csv'
dtwname = res_path+res_base+'_dtw.csv'

dmsname = res_path+res_base+'_dm_square.csv'

#get desired ids
id_file = data_path + id_fname
keep_ids = np.loadtxt(id_file,dtype=int)

#load kdigo vector for each patient
kd_fname = data_path + 'kdigo.csv'
f = open(kd_fname,'r')
ids = []
kdigos = []
for l in f:
    if int(l.split(',')[0]) in keep_ids:
        ids.append(l.split(',')[0])
        kdigos.append([int(float(x)) for x in l.split(',')[1:]])
ids = np.array(ids,dtype=int)
f.close()

#perform pairwise DTW + distance calculation
cdm = ppd(kdigos, dmname, dtwname)


#condensed matrix -> square
ds = squareform(cdm)

arr2csv(dmsname,ds,ids,fmt='%f',header=True)