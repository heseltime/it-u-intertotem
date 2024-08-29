import os

import numpy as np
import pyvista
import scipy.signal

# The file has been exported in script iris_data_request.
data_dir = './data'
in_filename = 'envelope.csv'
in_filepath = os.path.join(data_dir,
                           in_filename)
envelope = np.loadtxt(in_filepath,
                      delimiter = ',')

time = envelope[:, 0]
data = envelope[:, 1]

# Smooth the data
kernel_size = 2000
kernel = np.ones(kernel_size) / kernel_size
data = np.convolve(data,
                   kernel,
                   mode = 'same')

# Resample the data.
decimation_rate = 500
n_points_resamp = len(data) / decimation_rate
n_points_resamp = int(n_points_resamp)
data = scipy.signal.resample(data, n_points_resamp)


# Set physical propertis
# length of the sculpture [mm]
length = 100
# width of the sculpture [mm]
width = 50
# offset from z-axis [mm]
z_offset = 5

# Prepare the 3D points.
z_data_norm = data / (np.max(np.abs(data)))
z_data_mm = z_data_norm * ((width - z_offset) / 2) + z_offset

x_data = np.linspace(0, 1, len(z_data_mm))
x_data_mm = x_data * length

x_data_mm = x_data_mm[:, np.newaxis]
z_data_mm = z_data_mm[:, np.newaxis]
points = np.concatenate([x_data_mm,
                         np.zeros_like(z_data_mm),
                         z_data_mm],
                        axis = 1)



# Create line data from 3D points.
mesh = pyvista.lines_from_points(points)

# Create the mesh by rotation of the line mesh.
mesh = mesh.extrude_rotate(resolution = 10,
                           rotation_axis = (1, 0, 0))

mesh.plot(color = 'lightblue',
          show_edges = True)

mesh.save('envelope_mesh.ply')

