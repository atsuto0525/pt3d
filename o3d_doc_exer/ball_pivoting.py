import matplotlib.pyplot as plt
import open3d as o3d
import numpy as np

bunny = o3d.data.BunnyMesh()
gt_mesh = o3d.io.read_triangle_mesh(bunny.path)
gt_mesh.compute_vertex_normals()

pcd = gt_mesh.sample_points_poisson_disk(3000)
o3d.visualization.draw_geometries([pcd],
                                  window_name="bunny",
                                  width=1080,
                                  height=720)

radii = [0.005, 0.01, 0.02, 0.04]
rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(radii))
o3d.visualization.draw_geometries([pcd, rec_mesh])

