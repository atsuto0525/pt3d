import open3d as o3d
import numpy as np

print("->正在加载original点云... ")
pcd = o3d.io.read_point_cloud("dataset/rabbit.pcd")
print(pcd)

# print("->正在可视化原始点云")
# o3d.visualization.draw_geometries([pcd],
#                                   window_name="original point cloud",
#                                   width=800,
#                                   height=800,
#                                   left=30,
#                                   top=30)

print("->正在体素下采样...")
voxel_size = 0.6
down_pcd = pcd.voxel_down_sample(voxel_size)
print(down_pcd)

print("->正在保存点云")
o3d.io.write_point_cloud("pt_output/rabbit_voxel_down_sample2.pcd", down_pcd, True)  # 默认false，保存为Binarty；True 保存为ASICC形式
print(down_pcd)

# down_sample_pcd = o3d.io.read_point_cloud("pt_output/rabbit_voxel_down_sample2.pcd")

# 计算法向量
down_pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(0.01, 20))

print("->正在可视化下采样点云")
o3d.visualization.draw_geometries([down_pcd],
                                  window_name="down sampled point cloud",
                                  width=800,
                                  height=800,
                                  left=30,
                                  point_show_normal=True)
