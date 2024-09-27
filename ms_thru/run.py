'''
Simple microstrip thru line, 50 ohms over a slab of dielectric

Usage: python3 -i run.py

Geometry:
Signal travels from x=0 to x=geom__ms_length
The signal trace lives in the z=0 plane. The substrate slab is located below the signal trace, and the air above it.
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

# Simulation parameters
# resolution = 50  # pixels per micron
resolution = 10 # pixels per micron

# Global parameters
geom__ms_width = 1 # signal trace width
geom__ms_sub = 3 # substrate height
geom__ms_air = geom__ms_sub # height of air above the signal trace
geom__ms_length = 10 # microstrip line length

# total cell size
sx = geom__ms_length
sy = 9*geom__ms_width
sz = geom__ms_sub + geom__ms_air

# Define materials
air = mp.Medium(epsilon=1)
substrate = mp.Medium(epsilon=4)  # Dielectric substrate
metal = mp.metal  # PEC for metal strip

# Geometry of the microstrip: suibstrate slab, metal line and slab of air on top
geometry = [
    mp.Block( # slab of air
        size=mp.Vector3(geom__ms_length, sy, geom__ms_air), 
        center=mp.Vector3(0, 0, geom__ms_air/2), 
        material=air),
        # material=mp.Medium(epsilon=2)),
    mp.Block( # slab of substrate
        size=mp.Vector3(geom__ms_length, sy, geom__ms_sub), 
        center=mp.Vector3(0, 0, -geom__ms_sub/2), 
        material=substrate),
    mp.Block( # metal ground plane
        size=mp.Vector3(geom__ms_length, sy, 0), 
        # size=mp.Vector3(geom__ms_length, geom__ms_width, 0), 
        center=mp.Vector3(0, 0, -geom__ms_sub), 
        material=metal),
    mp.Block( # metal signal trace
        size=mp.Vector3(geom__ms_length, geom__ms_width, 0), 
        center=mp.Vector3(0, 0, 0), 
        material=metal),
]

# Boundary conditions
PML_THICKNESS = 1
pml_layers = [mp.PML(thickness=PML_THICKNESS)]  # PML absorbing layers
# # pml_layers = [mp.Absorber(thickness=PML_THICKNESS)]  # can also use 'absorber' instead of PML
sx += 2*PML_THICKNESS
sy += 2*PML_THICKNESS
sz += 2*PML_THICKNESS
cell = mp.Vector3(sx, sy, sz)  # 3D simulation, z>0

# sources = []      
# Source (continuous wave - CW source)
# frequency = 1.0  # Frequency of the source
frequency = 1/5  # Frequency of the source
sources = [
    mp.Source(
                mp.ContinuousSource(frequency=frequency),
                component=mp.Ez,
                # center=mp.Vector3(0, 0, -geom__ms_sub/2),
                # center=mp.Vector3(-geom__ms_length/2, 0, -geom__ms_sub/2),
                center=mp.Vector3(0, 0, -geom__ms_sub/2), # place midway along TL
                size=mp.Vector3(0,3*geom__ms_width,geom__ms_sub)
        )
]

# # DEBUG: To visualize sources
# _dummySource = mp.Block(
#     size=mp.Vector3(0,2*geom__ms_width,geom__ms_sub),
#     center=mp.Vector3(-geom__ms_length/2, 0, -geom__ms_sub/2),
#     material=mp.Medium(epsilon=0.9)
# )
# geometry.append(_dummySource)

# Simulation object
sim = mp.Simulation(cell_size=cell,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=sources,
                    # symmetries=[mp.Mirror(direction=mp.Y)], # Use with caution, this can forbid some modes from being launched!
                    resolution=resolution)

# Run the simulation for a certain number of timesteps
# sim.run(until=50)
# --------------------------------------------------
# Initialize the simulation and output the epsilon (dielectric constant) map
sim.init_sim()

# Dummy run to output the epsilon file
sim.run(
    mp.at_beginning(mp.output_epsilon),
    mp.at_every(1,mp.output_efield_x),
    mp.at_every(1,mp.output_efield_y),
    mp.at_every(1,mp.output_efield_z),
    mp.at_every(1,mp.output_hfield_x),
    mp.at_every(1,mp.output_hfield_y),
    mp.at_every(1,mp.output_hfield_z),
    until=10)

import os
# os.system("h5tovtk *.h5")
os.system("mv *.h5 h5_files")
print("Done! ====================")

# DEBUGGING EPS
# data = eps.flatten()
# plt.hist(data, bins=20, color='blue', edgecolor='black')