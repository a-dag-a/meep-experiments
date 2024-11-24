from utils import visualize
import numpy as np
# test = "ms_thru/out_LATEST/out__data.pickle"
test = "ms_thru/out_LATEST/out__map_eps.pickle"
# data = visualize.load_pickle(test)
eps_data = visualize.load_pickle(test)


# # Plotting the fields (requires matplotlib)
# import matplotlib.pyplot as plt
# plt.imshow(np.flipud(np.transpose(data)), interpolation='spline36', cmap='RdBu')
# # plt.title('$E_z$ data')
# plt.title('Epsilon Map')
# plt.savefig('dump_post_process.png')
# plt.colorbar()
# plt.show()




# ====================================

# ====================================
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to visualize the 3D epsilon data with transparency (no interactivity)
def plot_epsilon_3d_static(eps_data,x,y):
    # Get the dimensions of the eps_data
    x_len, y_len, z_len = eps_data.shape

    # Set up the figure and 3D axis
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Create a meshgrid for plotting
    x = np.arange(0, x_len)
    y = np.arange(0, y_len)
    # X, Y = np.meshgrid(x, y)
    X, Y = np.meshgrid(y, x)

    # Loop through slices in the z-direction and plot with transparency
    # for z_index in range(z_len):
    for z_index in range(0,z_len,2): # decimate for lightweight plotting
        Z = eps_data[:, :, z_index]
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.6)
    fig.colorbar(ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.6), ax=ax)


    # Set plot labels and title
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_zlabel('Epsilon')
    ax.set_title('3D Epsilon Data with Transparency')

    plt.show()

# # Generate some test 3D data (a sine wave)
# x = np.linspace(0, 2 * np.pi, 30)
# y = np.linspace(0, 2 * np.pi, 30)
# z = np.linspace(0, 2 * np.pi, 30)
# X, Y, Z = np.meshgrid(x, y, z)

# Example test data: 3D sine wave
# eps_data_test = np.sin(X) * np.sin(Y) * np.sin(Z)

# Plot the static 3D data with transparency
# plot_epsilon_3d_static(eps_data_test)


# Read in the grid co-ordinates
grid_vals = visualize.load_pickle('ms_thru/out_LATEST/out__grid.pickle')
x = grid_vals['X']
y = grid_vals['Y']
z = grid_vals['Z']
# X, Y, Z = np.meshgrid(y,x,z)
# plot_epsilon_3d_static(eps_data)
plot_epsilon_3d_static(eps_data,x,y)

import sys
sys.exit()


# ====================================
# ====================================
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider
from mpl_toolkits.mplot3d import Axes3D

# Function to visualize the 3D epsilon data
def plot_epsilon_3d(eps_data):
    # Get the dimensions of the eps_data
    x_len, y_len, z_len = eps_data.shape

    # Function to plot a specific slice in the z-direction
    def plot_slice(z_index):
        plt.figure(figsize=(8, 6))
        ax = plt.axes(projection='3d')

        # Create a meshgrid for plotting
        x = np.arange(0, x_len)
        y = np.arange(0, y_len)
        X, Y = np.meshgrid(x, y)
        Z = eps_data[:, :, z_index]

        # Plot the surface
        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

        # Set plot labels and title
        ax.set_xlabel('X-axis')
        ax.set_ylabel('Y-axis')
        ax.set_zlabel('Epsilon')
        ax.set_title(f'Epsilon Slice at z = {z_index}')

        plt.show()

    # Create an interactive slider to move through z-index slices
    interact(plot_slice, z_index=IntSlider(min=0, max=z_len-1, step=1, value=z_len//2))

# Example usage with eps_data
# eps_data should be a 3D numpy array. For example: eps_data = np.random.rand(30, 30, 30)
plot_epsilon_3d(eps_data)

