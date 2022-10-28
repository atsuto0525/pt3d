import open3d as o3d
import numpy as np

# ---------------------- 定义点云体素化函数 ----------------------
def get_mesh(_relative_path):
    mesh = o3d.io.read_triangle_mesh(_relative_path)
    mesh.compute_vertex_normals()
    return mesh
# =============================================================

# ------------------------- 点云体素化 --------------------------
print("->正在进行点云体素化...")
_relative_path = "dataset/table_scene_lms400.pcd"    # 设置相对路径
N = 2000        # 将点划分为N个体素
pcd = get_mesh(_relative_path).sample_points_poisson_disk(N)

# fit to unit cube
pcd.scale(1 / np.max(pcd.get_max_bound() - pcd.get_min_bound()),
          center=pcd.get_center())
pcd.colors = o3d.utility.Vector3dVector(np.random.uniform(0, 1, size=(N, 3)))
print("体素下采样点云：", pcd)
print("正在可视化体素下采样点云...")
o3d.visualization.draw_geometries([pcd])

print('执行体素化点云')
voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd, voxel_size=0.05)
print("正在可视化体素...")
o3d.visualization.draw_geometries([voxel_grid])
# ===========================================================
