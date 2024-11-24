'''
Simple Demo of a source in a box.

1. `source_wavelength` is indeed equal to the value that we enter (in microns)
2. Speed of light here really is ~7um/7sec = 1 (um/sec)
3. `resolution=10` seems adequate
'''
# import meep as mp
from meep.materials import Cu as Cu

#TODO:
# Do a basic sim and figure out visaulization of
# - [ ] Visualizing source positions
# - [ ] Visualizing vector fields (quiver plots)

# Geometry

# Port setup
# TODO: Setup ports using class later
# --------------------------------------------------
import meep as mp
import numpy as np

# # Simulation parameters
# # resolution = 50  # pixels per micron
# resolution = 10 # pixels per micron

# # total cell size
# sx = 10
# sx = 40
# # sy = 9*geom__ms_width
# sy = 10
# sz = 10



resolution = 10 # pixels per micron
sx, sy, sz = 40,5,5


# Define materials
air = mp.Medium(epsilon=1)

# Geometry of the microstrip: suibstrate slab, metal line and slab of air on top
geometry = [
    mp.Block( # slab of air
        size=mp.Vector3(sx,sy,sz), 
        center=mp.Vector3(0, 0, 0), 
        material=air),
        # material=mp.Medium(epsilon=2)),
    ]

# Boundary conditions
PML_THICKNESS = 5
pml_layers = [mp.PML(thickness=PML_THICKNESS)]  # PML absorbing layers
# pml_layers = [mp.Absorber(thickness=PML_THICKNESS)]  # can also use 'absorber' instead of PML
sx += 2*PML_THICKNESS
sy += 2*PML_THICKNESS
sz += 2*PML_THICKNESS
cell = mp.Vector3(sx, sy, sz)  # 3D simulation, z>0

# Sources
_source_wavelength = 7
_source_freq = 1/_source_wavelength

# _source_freq = 200 # 60GHz in real life

# # Source (continuous wave - CW source)
# sources = [
#     mp.Source(
#                 mp.ContinuousSource(frequency=_source_freq),
#                 component=mp.Ez,
#                 # center=mp.Vector3(0, 0, -geom__ms_sub/2),
#                 # center=mp.Vector3(-geom__ms_length/2, 0, -geom__ms_sub/2),
#                 center=mp.Vector3(0, 0, 0),
#                 size=mp.Vector3(1,1,1)
#         )
# ]

# Gaussian pulse source
sources = [
    mp.Source(
        mp.GaussianSource(
            _source_freq,
            # fwidth = 0.1*_source_freq,
            width = 5, # spatial width of pulse. NOTE: Should be longer than a few wavelengths for a prperly modulated Gaussian wavepacket!
            cutoff=2, # shut down the source after 2 temporal widths
        ),
        component = mp.Ez,
        center=mp.Vector3(0, 0, 0),
        size=mp.Vector3(1,1,1)
    )
]

# Simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    # symmetries=[mp.Mirror(direction=mp.Y)], # Use with caution, this can forbid some modes from being launched!
                    resolution=resolution,
                    # eps_averaging=False
                    )

# Run the simulation for a certain number of timesteps
# sim.run(until=50)
# --------------------------------------------------
# Initialize the simulation and output the epsilon (dielectric constant) map
sim.init_sim()

# Dummy run to output the epsilon file
sim.run(
    mp.at_beginning(mp.output_epsilon),
    # until=0) # just for geometry export
    mp.at_every(1,mp.output_efield_x),
    mp.at_every(1,mp.output_efield_y),
    mp.at_every(1,mp.output_efield_z),
    # mp.at_every(1,mp.output_hfield_x),
    # mp.at_every(1,mp.output_hfield_y),
    # mp.at_every(1,mp.output_hfield_z),
    until=30)
    # until=10)

import os
# os.system("h5tovtk *.h5")
os.system("mv *.h5 h5_files_demo")
print("Done! ====================")

# DEBUGGING EPS
# data = eps.flatten()
# plt.hist(data, bins=20, color='blue', edgecolor='black')

