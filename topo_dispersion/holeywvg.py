import meep as mp
# Some parameters to describe the geometry:
eps = 13    # dielectric constant of waveguide
w = 1.2     # width of waveguide
r = 0.36    # radius of holes


w = 4
r=1
# The cell dimensions
sy = 12     # size of cell in y direction (perpendicular to wvg.)
dpml = 1    # PML thickness (y direction only!)
cell_size = mp.Vector3(1, sy)

b = mp.Block(size=mp.Vector3(1e20, w, 1e20), material=mp.Medium(epsilon=eps))
c = mp.Cylinder(radius=r)
geometry = [b,c]
geometry = [b]
resolution=20

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

# sim.k_point = mp.Vector3(kx)
# sim.run(mp.at_beginning(mp.output_epsilon),
#         mp.after_sources(mp.Harminv(mp.Hz, mp.Vector3(0.1234), fcen, df)),
#         until_after_sources=300)

# sim.run(mp.at_every(1/fcen/20, mp.output_hfield_z), until=1/fcen)


# sim.run_k_points(300, mp.interpolate(k_interp, [mp.Vector3(0), mp.Vector3(0.5)]))
sim.run_k_points(10, mp.interpolate(k_interp, [mp.Vector3(0), mp.Vector3(0.5)]))

# Dump epsilon
from uuid import uuid4
import matplotlib.pyplot as plt
sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(cell_size.x,cell_size.y,0)), fields=mp.Hz)
plt.title(str(uuid4()))
plt.savefig('epsilon.png')
