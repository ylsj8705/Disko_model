# Fix input data to ATS Disko,

import numpy as np
import h5py
import matplotlib.pyplot as plt


timstep = 86400 # Timestep for output in seconds

data = np.genfromtxt('../data_raw/spinup_data.txt', dtype=float, usecols=(2,3,4,5,7,8), delimiter=" ", skip_header=1)
sw = data[:,3]
RH = data[:,1]
wind = data[:,2]
Ps = data[:,5]
Pr = data[:,4]
AT = data[:,0]


# Run data
data = np.genfromtxt('../data_raw/DSK_WeatherDriver_21-11-17_1728_COMBI.txt', dtype=float, usecols=(1,2,3,4,6,7), delimiter=" ", skip_header=1)
#sw_r = data[:,3]
#RH_r = data[:,1]
#wind_r = data[:,2]
Ps_r = data[:,5]
Pr_r = data[:,4]
AT_r = data[:,0]

AT_2016 = AT_r[5844:6210]
Ps_2016 = Ps_r[5844:6210]
Pr_2016 = Pr_r[5844:6210]

# make series combing 10 yrs spinup and then run data
AT = np.concatenate((AT[0:3650], AT_2016))
Ps = np.concatenate((Ps[0:3650], Ps_2016))
Pr = np.concatenate((Pr[0:3650], Pr_2016))

# Vary precipitation
Ps_3, Ps_4, Ps_5, Ps_6 = Ps*3, Ps*4, Ps*5, Ps*6
Pr = Pr*1.2

### Time stamp
dys = len(AT)
lastday = (timstep*dys)-timstep
Time = np.linspace(0,lastday,dys)  #  in seconds, daily time step

hf = h5py.File('../data_processed/spinup_disko.h5', 'w')
hf.create_dataset('Ta', data=AT)
hf.create_dataset('Us', data=wind[0:4016])
hf.create_dataset('Ps', data=Ps)
hf.create_dataset('Ps_3', data=Ps_3)
hf.create_dataset('Ps_4', data=Ps_4)
hf.create_dataset('Ps_5', data=Ps_5)
hf.create_dataset('Ps_6', data=Ps_6)
hf.create_dataset('Pr', data=Pr)
hf.create_dataset('RH', data=RH[0:4016])
hf.create_dataset('Qswin', data=sw[0:4016])
hf.create_dataset('time', data=Time)
hf.close()
