import sys,os
import numpy as np
import h5py
import ats_xdmf

# run this in the 1d run folder, where the data is.

vis = ats_xdmf.VisFile()
vis.loadMesh(columnar=True)
vis.filterIndices(-1)

pres = vis.getArray('pressure')
temp = vis.getArray('temperature')

# In the column mesh, top z is 0 and all other values negative
zc = vis.centroids[:,2]
z0 = 100 # z at top of 2d mesh (100 in this case)
z_depth = 100 +  zc

with h5py.File("../data_processed/column_data.h5", 'w') as fout:
    fout.create_dataset('z', data=zc)
    fout.create_dataset('pressure', data=pres[0,:])
    fout.create_dataset('temperature', data=temp[0,:])

# The below options are for meshes with different directions/numbering of z
# with h5py.File("column_data.h5", 'w') as fout:
#     fout.create_dataset('z', data=z_depth)
#     fout.create_dataset('pressure', data=pres[0,:])
#     fout.create_dataset('temperature', data=temp[0,:])
#
# with h5py.File("column_data.h5", 'w') as fout:
#     fout.create_dataset('z', data=np.flipud(z_depth))
#     fout.create_dataset('pressure', data=np.flipud(pres[0,:]))
#     fout.create_dataset('temperature', data=np.flipud(temp[0,:]))
