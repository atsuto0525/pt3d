import open3d.core as o3c
import numpy as np

# Tensor from list.
a = o3c.Tensor([0, 1, 2])
print("Created from list:\n{}".format(a))

# Tensor from Numpy.
a = o3c.Tensor(np.array([0, 1, 2]))
print("\nCreated from numpy array:\n{}".format(a))

# Dtype and inferred from list.
a_float = o3c.Tensor([0.0, 1.0, 2.0])
print("\nDefault dtype and device:\n{}".format(a_float))

# Specify dtype.
a = o3c.Tensor(np.array([0, 1, 2]), dtype=o3c.Dtype.Float64)
print("\nSpecified data type:\n{}".format(a))

# Specify device.
a = o3c.Tensor(np.array([0, 1, 2]), device=o3c.Device("CUDA:0"))
print("\nSpecified device:\n{}".format(a))