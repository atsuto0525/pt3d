import open3d as o3d
import numpy as np

# --------------------------- 加载点云 ---------------------------
print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("dataset/table_scene_lms400.pcd")
print("原始点云：", pcd)
o3d.visualization.draw_geometries([pcd],
                                  window_name="original point cloud",
                                  width=1080,
                                  height=720)
# ==============================================================

# ------------------------- Ball pivoting --------------------------
print('run Poisson surface reconstruction')
radius = 0.001   # 搜索半径
max_nn = 30         # 邻域内用于估算法线的最大点数
pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius, max_nn))     # 执行法线估计

with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=12)
print(mesh)
o3d.visualization.draw_geometries([mesh])
# ==============================================================
