# GOT IT, A BEAUTIFUL TE10 MODE!
# In TEmn, m denotes the number of halfwaves (anitinodes) in the field pattern along the 'a' dimension (longer edge of the waveguide). n denotes the same along the 'b' edge
# I have had to align the waveguide such that the longer edge is parallel to the Y axis in order to get the mode right
# This is likely due to the fact that the eig_parity argument has'nt got any options for symmetry wrt X axis, it has only options for ODD/EVEN symmetry along Y and Z.

# NOTE: Script generates the correct result, but is still WIP, lot of cleanup to be done!
import meep as mp

# a = 1 (meep length unit) = 10 mils
rect_a = 61 ####122 # 122 mils
rect_b = 122 ####61 # 61 mils

src_wavelength = 158 #rect_a/3.1 #158 # 158 mils = 4 mm, wavelength
rect_len = 6*rect_b ####6*rect_a #6*src_wavelength
d_pml = rect_b ####rect_a #src_wavelength
cell_size = mp.Vector3(2*d_pml+rect_a,2*d_pml+rect_b,2*d_pml+rect_len)

# OVERALL GEOMETRY
geometry = []
geometry.append(mp.Block(center=mp.Vector3(), size=cell_size, material=mp.metal))
geometry.append(mp.Block(center=mp.Vector3(), size=mp.Vector3(rect_a,rect_b,rect_len), material=mp.air))

# BOUNDARY CONDITIONS
# boundary_layers = []
boundary_layers = [mp.PML(thickness=d_pml,direction=mp.Z)] # PML boundaries only on open ends of the waveguide

# FREQUENCY, RESOLUTION, AND RUN TIME
f_cen = 1/src_wavelength
f_wid = 0.001 # calculated value for 71-86 GHz
resolution = round(5/rect_a,3) ####round(5/rect_b,3) # 5 cells per shorter edge of the waveguide # 10/src_wavelength # 10 cells per wavelength
run_time = cell_size.z # enough to reach the other end 10*src_wavelength # 15 cycles of the center tone

num_cells = [s*resolution for s in [cell_size.x, cell_size.y, cell_size.z]]
print(f'Info: Number of cells is {num_cells[0]}x{num_cells[1]}x{num_cells[2]} = {num_cells[0]*num_cells[1]*num_cells[2]} cells for {run_time*2*resolution} time steps')
input('Proceed? Press any normal character to proceed (Hit Ctrl+C to abort)')

# EIGENMODE SOURCE
# We need to excite the first TE mode, so we configure the Eigenmode source as follows
kpoint = mp.Vector3(0,0,-1) # multiples of 2pi/a?

# bnum = 1 # a TM mode
# bnum = 2 # TE30 mode,
bnum = 1
sources = [
    mp.EigenModeSource(
    # mp.GaussianSource(frequency=f_cen,fwidth=f_wid),
    mp.ContinuousSource(frequency=f_cen,fwidth=f_wid),
    center=mp.Vector3(0,0,-(cell_size.z/2-d_pml)),
    size=mp.Vector3(rect_a,rect_b,0), # just the waveguide cavity
    # size=mp.Vector3(cell_size.x,cell_size.y,0), # the entire cross section, including metal walls
    direction=mp.NO_DIRECTION, # try changing this to mp.Z
    eig_kpoint=kpoint,
    eig_band=bnum,
    eig_parity=mp.EVEN_Y,
    eig_match_freq=True)
]

# MONITOR PLANES
fr_neg = mp.FluxRegion(center=mp.Vector3(0,0,-cell_size.z/4),size=mp.Vector3(rect_a,rect_b,0))
fr_pos = mp.FluxRegion(center=mp.Vector3(0,0,cell_size.z/4),size=mp.Vector3(rect_a,rect_b,0))

sim = mp.Simulation(
    cell_size=cell_size,
    geometry=geometry,
    resolution=resolution,
    sources=sources,
    boundary_layers=boundary_layers,
    eps_averaging=False
)
nfreqs = 501
flux_neg = sim.add_flux(f_cen,2*f_wid,nfreqs,fr_neg)
flux_pos = sim.add_flux(f_cen,2*f_wid,nfreqs,fr_pos)

interval = 100# 30
sim.run(mp.at_beginning(mp.output_epsilon),
mp.at_every(interval, mp.output_efield_x),
mp.at_every(interval, mp.output_efield_y),
mp.at_every(interval, mp.output_efield_z),
mp.at_every(interval, mp.output_hfield_x),
mp.at_every(interval, mp.output_hfield_y),
mp.at_every(interval, mp.output_hfield_z),
mp.at_every(interval, mp.output_sfield_x),
mp.at_every(interval, mp.output_sfield_y),
mp.at_every(interval, mp.output_sfield_z),
until=2*run_time
# until_after_sources=src_wavelength # one period after cutoff
)

print('='*30)
print('DONE!')

# =============================================================================

import matplotlib.pyplot as plt
# sim.plot2D(output_plane=center_slice)
sim.plot2D(output_plane=mp.Volume(center=mp.Vector3(),size=mp.Vector3(0,cell_size.y,cell_size.z)), fields=mp.Ex)
plt.show()

# DISPLAYING FLUXES
import numpy as np
# freqs = np.linspace(f_cen-f_wid/2,f_cen+f_wid/2,nfreqs)
freqs = mp.get_flux_freqs(flux_neg)
data_flux_neg = mp.get_fluxes(flux_neg)
data_flux_pos = mp.get_fluxes(flux_pos)
# or use sim.display_fluxes()
# plt.plot(freqs,data_flux_neg[0])
# plt.plot(freqs,data_flux_pos[0])
plt.plot(freqs,data_flux_neg)
plt.plot(freqs,data_flux_pos)
plt.grid()
plt.title('Recorded fluxes (FFT)')
plt.show()


# USEFUL FOR FLUX SUBTRACTION
# # Split chunks based on amount of work instead of size
# sim1 = mp.Simulation(..., split_chunks_evenly=False)
# norm_flux = sim1.add_flux(...)
# sim1.run(...)
# sim1.save_flux(...)

# # Make sure the second run uses the same chunk layout as the first
# sim2 = mp.Simulation(..., chunk_layout=sim1)
# flux = sim2.add_flux(...)
# sim2.load_minus_flux(...)
# sim2.run(...)

# POYNTING VECTOR ANIMATION
# import os
# file_list = [k if k.endswith('h5') for k in os.list_dir()]

