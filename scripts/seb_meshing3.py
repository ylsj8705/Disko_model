import sys,os
sys.path.append(os.path.join(os.environ['ATS_SRC_DIR'],'tools','meshing','meshing_ats'))
import meshing_ats

import numpy as np
from matplotlib import pyplot as plt




###### based on observed data

# Observed topo data disko
data = np.genfromtxt('../data_raw/DSK_TopoEXT_long.txt', dtype=float, usecols=(0,1,2), delimiter=" ", skip_header=1)
x_obs = data[:,0]
z_obs = data[:,2]
org_obs = data[:,1]

m2 = meshing_ats.Mesh2D.from_Transect(x_obs,z_obs)
print(f'# of cells: {m2.num_cells()}')

# 1) with steady org layer thickness
# Organic thickness

org_layer_thickness = np.repeat(z_obs - org_obs,2)

layer_types = []
layer_data = []
layer_ncells = []
layer_mat_ids = []
layer_depth = []

# here we will only use 1 cell per layer, so layer thickness = dz.
# We will also telescope the mesh, starting at 1cm grid cell and growing it larger in each layer.
dz = .01
i = 0
current_depth = 0
while dz < 2:
    if i<=20:            #organic
        dz *= 1.2
    elif (20<i)&(i<=26): #mineral
        dz *= 1.4
    else:                #bedrock
        dz *= 1.5
    layer_types.append("constant")
    layer_data.append(dz)
    layer_ncells.append(1)
    current_depth += dz
    layer_depth.append(current_depth)
    i += 1

# now add in a bunch of cells to reach 45 m, of equal dz that is ~2m.
num_of_layers=len(layer_data)
layer_types.append('constant')
layer_data.append(45 - sum(layer_data))  # note sum(layer_data) == the total mesh thickness at this point
layer_ncells.append(int(np.floor(layer_data[-1]/dz)))
layer_depth.append(45)

# allocate 2D matrix with cols=#cells, rows=21
mat_ids=np.zeros((m2.num_cells(), 21), 'i')
for i in range(m2.num_cells()):
    for j in range(21): # after layer 20 everything is bedrock
        if (layer_depth[j] < org_layer_thickness[i]):
            mat_ids[i,j]=1001
        else:
            mat_ids[i,j]=1002

# filling out layer_mat_ids
layer_mat_ids = np.zeros((sum(layer_ncells), m2.num_cells()),'i')
for j in range(21):
    layer_mat_ids[j,:]=mat_ids[:,j]
for j in range(21,sum(layer_ncells)):
    layer_mat_ids[j,:]=101

print(f'# of rows, # of cells:{np.shape(layer_mat_ids)}')

# make the mesh, save it as an exodus file
m3 = meshing_ats.Mesh3D.extruded_Mesh2D(m2, layer_types,layer_data, layer_ncells, layer_mat_ids)
if os.path.exists('disko_TopoEXT_long.exo'):
    os.remove('disko_TopoEXT_long.exo')
m3.write_exodus("disko_TopoEXT_long.exo")


