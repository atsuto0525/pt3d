import open3d as o3d

print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("pt_output/voxel_down_sample.pcd")
print(pcd)

# # 法线估计
# radius = 0.02   # 搜索半径
# max_nn = 50     # 邻域内用于估算法线的最大点数
# pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius, max_nn))     # 执行法线估计

# 可视化
o3d.visualization.draw_geometries([pcd],
                                  window_name = "可视化参数设置",
                                  width = 600,
                                  height = 450,
                                  left = 30,
                                  top = 30,
                                  point_show_normal = True)
