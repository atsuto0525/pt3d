import open3d as o3d

bunny = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(bunny.path)
mesh.compute_vertex_normals()

pcd = mesh.sample_points_possion_disk(750)
o3d.visualization.draw_geometries([pcd],
                                  window_name="bunny")
alpha=0.03
print(f"alpha={alpha:.3f}")
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
mesh.compute_vertext_normals()
o3d.visualization.draw_geometries([mesh],mesh_show_back_face=True)

