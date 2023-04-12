import argparse
parser = argparse.ArgumentParser()
# parser.add_argument('file_template',type=str,default="data_WR-12/trial_rectWvgApertures-{}{}-001840.70.h5")
# args = parser.parse_args()
# file_template = args[file_template]

# file_template = "rectWvg-{}{}-001951.22.h5"
file_template = "rectWvg-{}{}-001560.98.h5"

import h5py
import numpy as np

def fetchVectorData(file_template):

    data = {} # dict for x,y,z arrays
    field = 'e' # 'e' or 'h'
    for c in ['x','y','z']:
        filename = file_template.format(field,c)
        print(f'Reading {filename} ...')
        f = h5py.File(filename)
        data[f'{field}{c}'] = np.array(f[f'{field}{c}'])

    u = data[f'{field}x']
    v = data[f'{field}y']
    w = data[f'{field}z']
    return u,v,w

u,v,w = fetchVectorData(file_template)
from mayavi import mlab

src = mlab.pipeline.vector_field(u, v, w)
# mlab.pipeline.vectors(src, mask_points=10, scale_factor=3.)
# mlab.outline()


# An interactive cut-plane! Mayavi is AWESOME!
s = mlab.pipeline.vector_cut_plane(src, mask_points=1, scale_factor=3)
# mlab.outline()
# =======================================================
# import vtk

# # Create a reader object and specify the VTK file to read
# reader = vtk.vtkDataSetReader()
# reader.SetFileName(filename)

# # Update the reader to read the file
# reader.Update()

# # Get the output data object from the reader
# data = reader.GetOutput()

# # Access the data as a structured grid
# structured_grid = vtk.vtkStructuredGrid.SafeDownCast(data)

# # Get the point data
# point_data = structured_grid.GetPointData()

# # Get the electric field data array
# e_field_array = point_data.GetArray("E")

# # Get the scalar range of the data array
# scalar_range = e_field_array.GetRange()

# # Print some information about the data array
# print("Electric field array name:", e_field_array.GetName())
# print("Scalar range:", scalar_range)
