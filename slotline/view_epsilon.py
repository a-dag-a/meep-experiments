from mayavi import mlab
import h5py
import numpy as np

filename = "./h5_files/run-eps-000000.00.h5"
print(f'Reading dielectric map from {filename} ...')
f = h5py.File(filename)
eps = np.array(f['eps'])

src = mlab.pipeline.scalar_field(eps)
mlab.pipeline.volume(src)
mlab.volume_slice(eps, plane_orientation='x_axes')
mlab.colorbar()