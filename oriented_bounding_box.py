import open3d as o3d
import numpy as np

print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("dataset/table_scene_lms400.pcd")
print(pcd)

print("->正在计算点云轴向最小包围盒...")
aabb = pcd.get_axis_aligned_bounding_box()
aabb.color = (1, 0, 0)
print("->正在计算点云最小包围盒...")
obb = pcd.get_oriented_bounding_box()
obb.color = (0, 1, 0)
o3d.visualization.draw_geometries([pcd, aabb, obb])
