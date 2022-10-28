import open3d as o3d
import numpy as np

# --------------------------- 加载点云 ---------------------------
print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("dataset/table_scene_lms400.pcd")
print("原始点云：", pcd)
# ==============================================================

# ------------------------- Alpha shapes -----------------------
alpha = 0.05
print(f"alpha={alpha:.3f}")
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
mesh.compute_vertex_normals()
o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)
# ==============================================================
