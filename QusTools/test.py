import numpy as np
from scipy.interpolate import griddata

def create_enclosing_surface_of_best_fit(x, y, z, resolution=100):
    """Create an enclosing surface of best fit for 3D data using spline interpolation."""

    # Generate a regular grid for the x and y data
    x_range = np.linspace(np.min(x), np.max(x), resolution)
    y_range = np.linspace(np.min(y), np.max(y), resolution)
    x_grid, y_grid = np.meshgrid(x_range, y_range)

    # Generate a 1D grid for the z data
    z_grid = np.zeros_like(x_grid)
    for i, xi in enumerate(x_range):
        mask = x == xi
        if np.any(mask):
            z_values = z[mask]
            y_values = y[mask]
            sorted_indices = np.argsort(y_values)
            z_values = z_values[sorted_indices]
            y_values = y_values[sorted_indices]
            z_values = np.pad(z_values, (0, resolution - len(z_values)), mode='edge')
            z_grid[:, i] = z_values

    # Interpolate the 1D grid to the 2D grid using cubic spline interpolation
    z_interp = griddata((x.ravel(), y.ravel()), z.ravel(), (x_grid, y_grid), method='cubic')

    return x_grid, y_grid, z_interp


import matplotlib.pyplot as plt

# Generate some random 3D data
x = np.random.rand(100)
y = np.random.rand(100)
z = np.sin(x * y) / (x * y)

# Create an enclosing surface of best fit using spline interpolation
x_grid, y_grid, z_interp = create_enclosing_surface_of_best_fit(x, y, z, resolution=200)

# Plot the surface
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(x_grid, y_grid, z_interp, cmap='viridis')
plt.show()
