'''
Simple microstrip thru line, 50 ohms over a slab of dielectric

Usage (serial): python3 -i run.py
Usage (parallel): mpirun -np <number of cores> python3 -i run.py

Geometry:
Signal travels from x=0 to x=geom__ms_length
The signal trace lives in the z=0 plane. The substrate slab is located below the signal trace, and the air above it.

Other notes:
```
sudo apt install mpich
```


Use this bash script to setup parallel meep in VCL
```
#!/bin/bash
# Simple setup script for VCl environment
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p /home/bgpillai/miniconda
export PATH= /home/bgpillai/miniconda/bin:$PATH


# conda init

# Call conda init once to setup the shell
~/miniconda/bin/conda init

# Serial variant of pymeep
# conda create -n mp -c conda-forge pymeep pymeep-extras


# Parallel variant of pymeep
conda create -n pmp -c conda-forge pymeep=*=mpi_mpich_*
#conda activate pmp
```
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
# resolution = 10 # pixels per micron
resolution = 5 # pixels per micron

# Global parameters
geom__ms_width = 5 # signal trace width
# geom__ms_sub = 20 # substrate height
geom__ms_sub = 10 # substrate height
geom__ms_air = geom__ms_sub # height of air above the signal trace
# geom__ms_length = 100 # microstrip line length
geom__ms_length = 100 # microstrip line length

# total cell size
sx = geom__ms_length
# sy = 9*geom__ms_width
sy = 5*geom__ms_width
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
# pml_layers = [mp.Absorber(thickness=PML_THICKNESS)]  # can also use 'absorber' instead of PML
sx += 2*PML_THICKNESS
sy += 2*PML_THICKNESS
sz += 2*PML_THICKNESS
cell = mp.Vector3(sx, sy, sz)  # 3D simulation, z>0

# ========================================================
# Sources
# ========================================================
# REGULAR SOURCES
# 60GHz would rescale to 200 meepHz frequency
_source_wavelength = 100/3 # this happens to be 9 THz in real life!
_source_freq = 1/_source_wavelength

# _realFreq2meepFreq = (200/(60e9)) # mutliplication factor for obtaining meep frequencies 
# _source_freq = 200 # 60GHz in real life

# Gaussian pulse source
# _source_freq = 1/(geom__ms_length/2)
# sources = [
#     mp.Source(
#         mp.GaussianSource(
#             _source_freq,
#             fwidth = 0.1*_source_freq,
#             cutoff=2, # shut down the source after 2 temporal widths
#         ),
#         component = mp.Ez,
#         center=mp.Vector3(0, 0, -geom__ms_sub/2), # place midway along TL
#         size=mp.Vector3(0,3*geom__ms_width,geom__ms_sub)
#     )
# ]

# Source (continuous wave - CW source)
sources = [
    mp.Source(
                mp.ContinuousSource(frequency=_source_freq),
                component=mp.Ez,
                # center=mp.Vector3(0, 0, -geom__ms_sub/2),
                # center=mp.Vector3(-geom__ms_length/2, 0, -geom__ms_sub/2),
                center=mp.Vector3(0, 0, -geom__ms_sub/2), # place midway along TL
                size=mp.Vector3(0,3*geom__ms_width,geom__ms_sub)
        )
]
# ========================================================
# Eigenmode source
# See https://meep.readthedocs.io/en/latest/Python_User_Interface/#eigenmodesource




# FIXME: EIgenmode source does not work, program aborts saying "Abort(1) on node 3 (rank 3 in comm 0): application called MPI_Abort(MPI_COMM_WORLD, 1)"
# _src_kpoint = mp.Vector3(x=_source_freq) # Meep units of 2π/(unit length), the pi is already absorbed in there
_bnum = 1 #FIXME: this is a guess, we need the actual branch number of the usual microstrip TEM mode

sources = [mp.EigenModeSource(src=mp.ContinuousSource(_source_freq), # NOTE: This freq might get overrided by a frequency computed by MPB for our requested k point, based on the dispersion relation computed by MPB
                                center=mp.Vector3(),
                                size=mp.Vector3(0,3*geom__ms_width,geom__ms_sub + geom__ms_air),
                                direction=mp.X, # chooses the normal of the eigsource region
                                # eig_kpoint=_src_kpoint,
                                eig_band=_bnum,
                                eig_parity=mp.EVEN_Y, # for this TL port orientation
                                # eig_match_freq=False)]
                                eig_match_freq=True)]
# NOTE: "Also, the eigenmode frequency computed by MPB overwrites the frequency parameter of the src property for a GaussianSource and ContinuousSource"

# DEBUG: To visualize sources
# _dummySource = mp.Block(
#     size=mp.Vector3(0,2*geom__ms_width,geom__ms_sub),
#     center=mp.Vector3(0, 0, -geom__ms_sub/2),
#     # center=mp.Vector3(-geom__ms_length/2, 0, -geom__ms_sub/2),
#     material=mp.Medium(epsilon=8)
# )
# geometry.append(_dummySource)
# ========================================================

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
    # mp.at_every(1,mp.output_efield_x),
    # mp.at_every(1,mp.output_efield_y),
    mp.at_every(1,mp.output_efield_z),
    # mp.at_every(1,mp.output_hfield_x),
    # mp.at_every(1,mp.output_hfield_y),
    # mp.at_every(1,mp.output_hfield_z),
    until=200)
    # until=10)

import os
# os.system("h5tovtk *.h5")
os.system("mv *.h5 h5_files")
print("Done! ====================")

# DEBUGGING EPS
# data = eps.flatten()
# plt.hist(data, bins=20, color='blue', edgecolor='black')

