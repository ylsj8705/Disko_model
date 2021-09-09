# Fix input data to ATS Disko,

import numpy as np
import h5py
import matplotlib.pyplot as plt


timstep = 86400 # Timestep for output in seconds

data = np.genfromtxt('../data_raw/spinup_data.txt', dtype=float, usecols=(2,3,4,5,7,8), delimiter=" ", skip_header=1)
sw = list(map(float, data[:,3]))
RH = list(map(float, data[:,1]))
wind = list(map(float, data[:,2]))
Ps = data[:,5]
Pr = list(map(float, data[:,4]))
AT = list(map(float, data[:,0]))

Ps = Ps*3
### Time stamp
dys = len(sw)
lastday = (timstep*dys)-timstep
Time = np.linspace(0,lastday,dys)  #  in seconds, daily time step

hf = h5py.File('../data_processed/spinup_disko.h5', 'w')
hf.create_dataset('Ta', data=AT)
hf.create_dataset('Us', data=wind)
hf.create_dataset('Ps', data=Ps)
hf.create_dataset('Pr', data=Pr)
hf.create_dataset('RH', data=RH)
hf.create_dataset('Qswin', data=sw)
hf.create_dataset('time', data=Time)
hf.close()
