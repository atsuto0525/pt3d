import socket
from math import radians, cos, sin

import numpy as np
import open3d as o3d

# 垂直角度 w 列表,单位:角度/° [来源请参考VLP16手册]
g_vertical_angle_list = [-15, 1, -13, 3, -11, 5, -9, 7, -7, 9, -5, 11, -3, 13, -1, 15]
# 垂直距离矫正列表,单位:毫米/mm [来源请参考VLP16手册]
g_vertical_correction_list = [11.2, -0.7, 9.7, -2.2, 8.1, -3.7, 6.6, -5.1, 5.1, -6.6, 3.7, -8.1, 2.2, -9.7, 0.7, -11.2]


# 将点云保存到ply文件
def save_to_ply(save_file, point_list):
    length = len(point_list)
    with open(save_file, 'w') as f:
        f.writelines((
            "ply\n",
            "format ascii 1.0\n",
            "element vertex {}\n".format(length),
            "property float x\n",
            "property float y\n",
            "property float z\n",
            "property uchar red\n",
            "property uchar green\n",
            "property uchar blue\n",
            "element face 0\n",
            "property list uint8 int32 vertex_index\n",
            "end_header\n"))

        for i in range(length):
            f.writelines("%f %f %f %d %d %d\n" % (point_list[i][0], point_list[i][1], point_list[i][2],
                                                  point_list[i][3], point_list[i][4], point_list[i][5]))


class PointCloud:
    # @ distance：测出的点云距离，单位：m(米)
    # @ azimuth_angle：数据点与发射中心点的连线在XOY面的分向量与Y轴的夹角,即:方位角
    # @ w_angle：数据点与发射中心点的连线与平面的夹角,或激光的俯仰角
    # @ reflect：反射率，单位(百分比 % )
    #  [坐标换算请参考VLP16手册]
    def __init__(self, distance, azimuth_angle, w_angle, reflect, correction_index):
        # 根据手册提供的关系式求出 XYZ 坐标
        launch_radius = 41.910 / 1000  # 单位：m/米
        w_angle = radians(w_angle)  # 弧度转换
        azimuth_angle = radians(azimuth_angle)  # 弧度转换
        self.x = (distance * cos(w_angle) + launch_radius) * sin(azimuth_angle)
        self.y = (distance * cos(w_angle) + launch_radius) * cos(azimuth_angle)
        self.z = distance * sin(w_angle) + g_vertical_correction_list[correction_index] / 1000
        self.r = reflect  # 颜色以反射率为基准
        self.g = reflect
        self.b = reflect
        self.reflect = reflect

    def to_string(self):
        return '(' + str(self.x) + 'm,' + str(self.y) + 'm,' + str(self.z) + 'm) '


def de_code_lidar_data(data):
    delta_count = 0
    delta_value = 0
    point_cloud_list = []
    azimuth_angle_list = []

    # 计算并存储12个 data block 的方位角(azimuth_angle) [详细来源请参考VLP16手册]
    for i in range(0, 12):
        block_index = i * 100
        azimuth_angle_index = block_index + 2
        azimuth_angle = float(int(data[azimuth_angle_index + 1] << 8) + data[azimuth_angle_index]) * 0.01
        azimuth_angle_list.append(azimuth_angle)

    # 计算出每个data block的第15-31个点的方位角并存储至 azimuth_angle_list [详细来源请参考VLP16手册]
    azimuth_angle_list_tmp = azimuth_angle_list.copy()
    for i in range(0, 11):
        a1 = azimuth_angle_list[i]
        a2 = azimuth_angle_list[i + 1]
        if a2 < a1:
            a2 += 360
        avg = (a1 + a2) / 2
        delta_value += (a2 - a1) / 2
        delta_count += 1
        azimuth_angle_list_tmp.insert(i * 2 + 1, avg)
    # 方位角平均增量
    delta_degrees_inc = delta_value / delta_count
    # 求出最后一个数据序列的方位角
    azimuth_angle_list_tmp.append(azimuth_angle_list_tmp[len(azimuth_angle_list_tmp) - 1] + delta_degrees_inc)
    azimuth_angle_list = azimuth_angle_list_tmp.copy()

    # 遍历12个 data block 的每个数据点  [详细来源请参考VLP16手册]
    for i in range(0, 12):  # 每个数据包的第 i 个block  [详细来源请参考VLP16手册]
        block_index = i * 100
        block_point_index = block_index + 4
        data_flag = int(data[block_index] << 8) + int(data[block_index + 1])
        if data_flag == 0xffee:
            for j in range(0, 2):  # 每个block的第 j 组数据  [详细来源请参考VLP16手册]
                azimuth_angle = azimuth_angle_list[i * 2 + j]
                if 0.0 <= azimuth_angle <= 1.0:  # 筛选方向角为 0 - 1 的数据点
                    print('azimuth_angle = ' + str(azimuth_angle))
                    for k in range(0, 16):  # 16线中的第 k 个线
                        # 对应线路的俯仰角  [详细来源请参考VLP16手册]
                        w_angle = g_vertical_angle_list[k]
                        # 点到激光雷达中心的距离  [详细来源请参考VLP16手册]
                        distance = (int(data[block_point_index + j * 48 + k * 3 + 1] << 8) + int(
                            data[block_point_index + j * 48 + k * 3])) / 500
                        # 点的反射率  [详细来源请参考VLP16手册]
                        reflectivity = int(data[block_point_index + j * 48 + k * 3 + 2])

                        print('w_angle = ' + str(w_angle) + ',distance = ' + str(distance) + ',degrees = ' + str(
                            azimuth_angle))
                        # 生成点云对象
                        point = PointCloud(distance, azimuth_angle, w_angle, reflectivity, k)
                        # 数据存入点云列表
                        point_cloud_list.append([point.x, point.y, point.z, point.r, point.g, point.b])
        else:
            print('data error !')
    return point_cloud_list


if __name__ == '__main__':
    np_points = []
    target_running_time = 5  # 单位:秒/s
    start_record_time_flag = 0

    ip_config = ('', 2368)  # VLP16 的UDP协议端口号为 2368, 可不指定IP地址  [详细来源请参考VLP16手册]
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.bind(ip_config)

    while True:
        lidar_data, address = my_socket.recvfrom(1206)
        # 计算数据包的时间戳, 单位:微妙/us  [详细来源请参考VLP16手册]
        time_stamp = int(lidar_data[1203] << 24) + int(lidar_data[1202] << 16) + int(lidar_data[1201] << 8) + int(
            lidar_data[1200])

        if start_record_time_flag == 0:
            first_lidar_data_time_stamp = time_stamp
            time_stamp_old = time_stamp
            start_record_time_flag = 1

        np_points += de_code_lidar_data(lidar_data)

        running_time = (time_stamp - first_lidar_data_time_stamp) / 1000000
        if running_time >= target_running_time:
            break

    file_name = 'C:/lidar_point_cloud_01.ply'
    save_to_ply(file_name, np_points)

    # 利用 open3d 显示点云
    print(np_points)
    pcd = o3d.io.read_point_cloud(file_name)
    pcd.points = o3d.utility.Vector3dVector(pcd.points)
    print(pcd)
    print(np.asarray(pcd.points))
    o3d.visualization.draw_geometries([pcd])
