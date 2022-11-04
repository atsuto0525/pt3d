import open3d as o3d
import numpy as np

print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("dataset/table_scene_lms400.pcd")
rabbit = o3d.io.read_point_cloud("dataset/rabbit.pcd")
print(pcd)

print("->正在计算点云凸包...")
hull, _ = pcd.compute_convex_hull()
hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
hull_ls.paint_uniform_color((1, 0, 0))
o3d.visualization.draw_geometries([pcd, hull_ls])

print("->computing oriented bounding box")

obb = pcd.get_oriented_bounding_box()
obb.color =(0,1,0)
o3d.visualization.draw_geometries([pcd, obb])

obb_rabbit = rabbit.get_oriented_bounding_box()
obb_rabbit.color = (100,0,100)
o3d.visualization.draw_geometries([rabbit,obb_rabbit])