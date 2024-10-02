'''
Visualize the vector fields for E, H or S (Poynting vector) in the problem volume
- Optional dielectric overlay
'''

import argparse
from mayavi import mlab
import h5py
import numpy as np

parser = argparse.ArgumentParser()
# parser.add_argument('file_template',type=str,default="data_WR-12/trial_rectWvgApertures-{}{}-001840.70.h5")
# args = parser.parse_args()
# file_template = args[file_template]

# =====================================================
# Test input
file_template = "./h5_files/run-{}{}-000018.00.h5"

def fetchVectorData(file_template, field='e'):
    # field can be either 'e','h', or 's' (Poynting vector)
    data = {} # dict for x,y,z arrays
    for c in ['x','y','z']:
        filename = file_template.format(field,c)
        print(f'Reading {filename} ...')
        f = h5py.File(filename)
        data[f'{field}{c}'] = np.array(f[f'{field}{c}'])

    u = data[f'{field}x']
    v = data[f'{field}y']
    w = data[f'{field}z']
    return u,v,w

# field can be either 'e','h', or 's' (Poynting vector)
u,v,w = fetchVectorData(file_template,field='e')
src = mlab.pipeline.vector_field(u, v, w)
# mlab.pipeline.vectors(src, mask_points=10, scale_factor=3.)
# mlab.outline()

# An interactive cut-plane on which the quiver plot is rendered
s = mlab.pipeline.vector_cut_plane(src, mask_points=1, scale_factor=3)
# mlab.outline()
mlab.colorbar()


# # =====================================================
# # Optional dielectric map overlay
# filename = "./h5_files/run-eps-000000.00.h5"
# print(f'Reading dielectric map from {filename} ...')
# f = h5py.File(filename)
# eps = np.array(f['eps'])
# src = mlab.pipeline.scalar_field(eps)
# # mlab.pipeline.volume(src)
# # mlab.pipeline.volume_slice(src)
# mlab.colorbar()
# # mlab.pipeline.iso_surface(src, contours=[s.min()+0.1*s.ptp(), ], opacity=0.1)


# =================================================
# Visualize epsilon map
from mayavi import mlab
import h5py
import numpy as np

filename = "./h5_files/run-eps-000000.00.h5"
print(f'Reading dielectric map from {filename} ...')
f = h5py.File(filename)
eps = np.array(f['eps'])
# src = mlab.pipeline.scalar_field(eps)
# mlab.pipeline.volume(src)
# mlab.volume_slice(eps, plane_orientation='x_axes')
# mlab.colorbar()

# # Sometimes when the metal thickness is nonzero, the epsilon might turn 'all black'. 
# # In such cases use the eps_dielectricOnly to visualize
# # metal pixels have dielectric constant -1e20
# _mask_metalOnly = (eps == -1e20) # true for metal pixels
# _mask_notMetal = (eps != -1e20) # true for dielectric pixels
# eps_metalOnly = np.where(_mask_metalOnly, eps, 0)
# eps_dielectricOnly = np.where(_mask_notMetal, eps, 0)

# src = mlab.pipeline.scalar_field(eps)
# # src = mlab.pipeline.scalar_field(eps_dielectricOnly)
# mlab.pipeline.volume(src)
# mlab.colorbar()
