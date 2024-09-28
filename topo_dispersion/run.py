import meep as mp
import numpy as np
# Some parameters to describe the geometry:
# Define materials
air = mp.Medium(epsilon=1)
substrate = mp.Medium(epsilon=4)  # Dielectric substrate
metal = mp.metal  # PEC for metal strip

# lattice vectors
_scaling = 5
_vec_a = mp.Vector3(1,0,0)*_scaling
_vec_b = mp.Vector3(np.cos(np.pi/3),np.sin(np.pi/3),0)*_scaling
_radius = 1 #0.1*_scaling #(0.25*np.sin(np.pi/3))#*_scaling

# Unit cell geometry parameters
p = 0.1 # p=0 is symmetric, p=1 is maximum antisymmetry (one hole shrinks to zero size)
_d = mp.Vector3(np.cos(np.pi/6),np.sin(np.pi/6),0)
_offset = 1/(2*(3**0.5))*_scaling

sx = _vec_a.x
sy = _vec_a.x*np.sin(np.pi/3)


dpml = 1    # PML thickness (y direction only!)
sx += 2*dpml
sy += 2*dpml
cell_size = mp.Vector3(sx, sy)

# b = mp.Block(size=mp.Vector3(1e20, w, 1e20), material=mp.Medium(epsilon=eps))
# c = mp.Cylinder(radius=r)
# geometry = [b,c]
resolution=20

geometry = []
geometry.append(mp.Block( # slab of substrate
        size=mp.Vector3(sx, sy, 1e20), 
        center=mp.Vector3(0, 0), 
        material=substrate))

topo_sw = 1
_cell_size_center = mp.Vector3(0,0,0) # 0*_vec_a + 0*_vec_b
# Type A and TYpe B holes
geometry.append(mp.Cylinder(_radius*(1+p), center=_cell_size_center + _offset*_d*topo_sw))
geometry.append(mp.Cylinder(_radius*(1-p), center=_cell_size_center - _offset*_d*topo_sw))

# ==============================
pml_layers = [mp.PML(dpml, direction=mp.Y)]

fcen = 0.25  # pulse center frequency
fcen=1/4
df = 1.5     # pulse freq. width: large df = short impulse

s = [mp.Source(src=mp.GaussianSource(fcen, fwidth=df), component=mp.Hz,
              center=mp.Vector3(0.1234,0))
]
sym = mp.Mirror(direction=mp.Y, phase=-1)

k_interp = 19

kx = 0.4
sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=pml_layers,
                    geometry=geometry,
                    sources=s,
                    # symmetries=[mp.Mirror(direction=mp.Y)], # Use with caution, this can forbid some modes from being launched!
                    resolution=resolution,
                    # eps_averaging=False # comment out for actual simulation
                    )

k_interp = 3
sim.run_k_points(10, mp.interpolate(k_interp, [mp.Vector3(0), mp.Vector3(0.5)]))

# Dump epsilon
from uuid import uuid4
import matplotlib.pyplot as plt
sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(cell_size.x,cell_size.y,0)), fields=mp.Hz)
plt.title(str(uuid4()))
plt.savefig('epsilon.png')
