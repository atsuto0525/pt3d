import numpy as np
import open3d as o3d

print('input')
bunny = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(bunny.path)

# fit to unit cube
mesh.scale(1 / np.max(mesh.get_max_bound() - mesh.get_min_bound()),
           center=mesh.get_center())

o3d.visualization.draw_geometries([mesh],
                                  width=1080,
                                  height=720)

print("voxelization")
voxel_grid = o3d.geometry.VoxelGrid.create_from_triangle_mesh(mesh, voxel_size=0.02)

o3d.visualization.draw_geometries([voxel_grid],
                                  window_name="voxelization with voxel size of 0.02",
                                  width=1080,
                                  height=720)
