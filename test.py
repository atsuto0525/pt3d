import open3d as o3d
import numpy as np
import pandas as pd
import six as six
print("->正在加载点云... ")
pcd = o3d.io.read_point_cloud("dataset/table_scene_lms400.pcd")
print(pcd)

print("->正在保存点云")
o3d.io.write_point_cloud("pt_output/write.pcd", pcd, True)	# 默认false，保存为Binarty；True 保存为ASICC形式
print(pcd)