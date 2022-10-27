import open3d as o3d
import numpy as np

# --------------------------- 加载点云 ---------------------------
print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("dataset/table_scene_lms400.pcd")
print("原始点云：", pcd)
# ==============================================================

# ------------------------- 构建Octree --------------------------
print('octree 分割')
octree = o3d.geometry.Octree(max_depth=19)
octree.convert_from_point_cloud(pcd, size_expand=0.02)
print("->正在可视化Octree...")
o3d.visualization.draw_geometries([octree])
# ==============================================================
