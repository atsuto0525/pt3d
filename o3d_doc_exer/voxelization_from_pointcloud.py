import numpy as np
import open3d as o3d

print('input')
armadillo = o3d.data.ArmadilloMesh()
mesh = o3d.io.read_triangle_mesh(armadillo.path)

N = 2000
pcd = mesh.sample_points_poisson_disk(N)
# fit to unit cube
pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()),
          center=pcd.get_center())

pcd.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(N, 3)))
o3d.visualization.draw_geometries([pcd],
                                  window_name="mesh-poisson-pointcloud",
                                  width=1080,
                                  height=720)

print("voxelization")
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.03)
o3d.visualization.draw_geometries([voxel_grid],
                                  window_name="voxelized with voxel size of 0.03",
                                  width=1080,
                                  height=720)
