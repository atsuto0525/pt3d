import open3d as o3d
import numpy as np

print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("dataset/table_scene_lms400.pcd")
print(pcd)

print("->正在可视化原始点云")
o3d.visualization.draw_geometries([pcd],
                                  window_name="original point cloud",
                                  width=800,
                                  height=800,
                                  left=30,
                                  top=30)

print("->正在体素下采样...")
voxel_size = 0.06
downpcd = pcd.voxel_down_sample(voxel_size)
print(downpcd)

print("->正在可视化下采样点云")
o3d.visualization.draw_geometries([downpcd],
                                  window_name="down sampled point cloud",
                                  width=800,
                                  height=800,
                                  left=30)

print("->正在保存点云")
o3d.io.write_point_cloud("pt_output/voxel_down_sample.pcd", downpcd, True)  # 默认false，保存为Binarty；True 保存为ASICC形式
print(downpcd)
