import time

import open3d as o3d

def keypoints_to_spheres(keypoints):
    spheres = o3d.geometry.TriangleMesh()
    for keypoints in keypoints.points:
        sphere = o3d.geometry.TriangleMesh.create_sphere(radius=0.001)
        sphere.translate(keypoints)
        sphere +=spheres
    spheres.paint_uniform_color([1.0, 0.75, 0.0])
    return spheres

bunny = o3d.data.BunnyMesh()
mesh = o3d.io.read_triangle_mesh(bunny.path)
mesh.compute_vertex_normals()

pcd = o3d.geometry.PointCloud()
pcd.points = mesh.vertices
tic= time.time()
keypoints = o3d.geometry.keypoint.compute_iss_keypoints(pcd,
                                               salient_radius=0.005,
                                               non_max_radius=0.005,
                                               gamma_21=0.5,
                                               gamma_32=0.5)
toc = 1000 * (time.time() - tic)
print("ISS Computation took {:.0f} [ms]".format(toc))

mesh.compute_vertex_normals()
mesh.paint_uniform_color([0.5, 0.5, 0.5])
o3d.visualization.draw_geometries([keypoints_to_spheres(keypoints), mesh])
