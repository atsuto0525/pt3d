import open3d as o3d
import  numpy as np

print("testing IO for point cloud ...")
# sample_pcd_data = o3d.data.PCDPointCloud()
pcd = o3d.io.read_point_cloud("../dataset/rabbit.pcd")
print(pcd)
o3d.io.write_point_cloud("../pt_output/copy_of_rabbit.pcd", pcd, write_ascii=True)
