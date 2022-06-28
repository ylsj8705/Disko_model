# Fix input data to ATS Disko,

import numpy as np
import h5py

timstep = 86400 # Timestep for output in seconds

data = np.genfromtxt('../data_raw/spinup_data.txt', dtype=float, usecols=(2,3,4,5,7,8), delimiter=" ", skip_header=1)
sw = data[:,3]
RH = data[:,1]
wind = data[:,2]
Ps = data[:,5]
Pr = data[:,4]
AT = data[:,0]


# Run data
data2 = np.genfromtxt('../data_raw/DSK_FutureScen_22-06-01_1421_RCPScen.txt', dtype=float, usecols=(1,2,3,4,6,7,8,9,10,11,12,13,14,15,16), delimiter=" ", skip_header=1)
sw_r = data2[:,3]
RH_r = data2[:,1]
wind_r = data2[:,2]
Ps_r = data2[:,5]
Pr_r = data2[:,4]
AT_r = data2[:,0]
AT_rcp26 = data2[:,6]
AT_rcp45 = data2[:,9]
AT_rcp85 = data2[:,12]
Pr_26 = data2[:,7]
Ps_26 = data2[:,8]
Pr_45 = data2[:,10]
Ps_45 = data2[:,11]
Pr_85 = data2[:,13]
Ps_85 = data2[:,14]

# AT_2016 = AT_r[5844:6210]
# Ps_2016 = Ps_r[5844:6210]
# Pr_2016 = Pr_r[5844:6210]

# make series combing 10 yrs spinup and then run data
# AT = np.concatenate((AT[0:3650], AT_2016))
# Ps = np.concatenate((Ps[0:3650], Ps_2016))
# Pr = np.concatenate((Pr[0:3650], Pr_2016))

AT = np.concatenate((AT[0:3650], AT_r))
AT_26 = np.concatenate((AT[0:3650], AT_rcp26))
AT_45 = np.concatenate((AT[0:3650], AT_rcp45))
AT_85 = np.concatenate((AT[0:3650], AT_rcp85))
Ps = np.concatenate((Ps[0:3650], Ps_r))
Pr = np.concatenate((Pr[0:3650], Pr_r))
Ps_26 = np.concatenate((Ps[0:3650], Ps_26))
Pr_26 = np.concatenate((Pr[0:3650], Pr_26))
Ps_45 = np.concatenate((Ps[0:3650], Ps_45))
Pr_45 = np.concatenate((Pr[0:3650], Pr_45))
Ps_85 = np.concatenate((Ps[0:3650], Ps_85))
Pr_85 = np.concatenate((Pr[0:3650], Pr_85))
sw = np.concatenate((sw[0:3650], sw_r))
RH = np.concatenate((RH[0:3650], RH_r))
wind = np.concatenate((wind[0:3650], wind_r))

# Inflow at the top of the hillslope
# data3 = np.genfromtxt('../data_raw/DSK_Inflow_TopSlope_21-11-29_1433_Prec_based.txt', dtype=float, usecols=(1,2,3,4,5), delimiter=" ", skip_header=1)
# Pr_top = np.concatenate((data3[0:3650,0],data3[5844:6210,0]))
# Pr_top08 = np.concatenate((data3[0:3650,1],data3[5844:6210,1]))
# Pr_top06 = np.concatenate((data3[0:3650,2],data3[5844:6210,2]))
# Pr_top04 = np.concatenate((data3[0:3650,3],data3[5844:6210,3]))
# Pr_top02 = np.concatenate((data3[0:3650,4],data3[5844:6210,4]))

# Vary precipitation
Ps_3, Ps_4, Ps_5, Ps_6 = Ps*3, Ps*4, Ps*5, Ps*6
Pr = Pr*1.2

### Time stamp
dys = len(AT)
lastday = (timstep*dys)-timstep
Time = np.linspace(0,lastday,dys)  #  in seconds, daily time step

hf = h5py.File('../data_processed/spinup_run_disko2.h5', 'w')
hf.create_dataset('Ta', data=AT)
hf.create_dataset('Ta_rcp26', data=AT_26)
hf.create_dataset('Ta_rcp45', data=AT_45)
hf.create_dataset('Ta_rcp85', data=AT_85)
hf.create_dataset('Us', data=wind)
hf.create_dataset('Ps', data=Ps)
hf.create_dataset('Ps_3', data=Ps_3)
hf.create_dataset('Ps_4', data=Ps_4)
hf.create_dataset('Ps_5', data=Ps_5)
hf.create_dataset('Ps_6', data=Ps_6)
hf.create_dataset('Ps_rcp26', data=Ps_26)
hf.create_dataset('Ps_rcp45', data=Ps_45)
hf.create_dataset('Ps_rcp855', data=Ps_85)
hf.create_dataset('Pr', data=Pr)
hf.create_dataset('Pr_rcp26', data=Pr_26)
hf.create_dataset('Pr_rcp45', data=Pr_45)
hf.create_dataset('Pr_rcp855', data=Pr_85)
# hf.create_dataset('Pr_top', data=Pr_top)
# hf.create_dataset('Pr_top08', data=Pr_top08)
# hf.create_dataset('Pr_top06', data=Pr_top06)
# hf.create_dataset('Pr_top04', data=Pr_top04)
# hf.create_dataset('Pr_top02', data=Pr_top02)
hf.create_dataset('RH', data=RH)
hf.create_dataset('Qswin', data=sw)
hf.create_dataset('time', data=Time)
hf.close()
