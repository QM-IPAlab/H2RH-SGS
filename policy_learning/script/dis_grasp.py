#compute the rot and trans differece between grasp pose and pre grasp pose
import argparse
import numpy as np
import transforms3d
import numpy as np
import open3d as o3d


def compute_min_distance(pose, point_cloud):
    # 计算姿态到点云每个点的欧几里得距离
    pose_t = pose[:3, 3]
    distances = np.linalg.norm(point_cloud - pose_t, axis=1)
    min_distance = np.min(distances)
    return min_distance





def parse_args():
    parser = argparse.ArgumentParser(description="Compute Euler angles and translation difference between two 4x4 pose matrices.")
    parser.add_argument("--predict_grasp_file", type=str, required=True, help="First pose matrix npz file")
    parser.add_argument('--object_pcl_file',type=str,required=True)
    parser.add_argument('--hand_pcl_file',type=str,required=True)
    parser.add_argument("--grasp_pose_file",  type=str, required=True, help="Second pose matrix npz file")
    

    return parser.parse_args()

def matrix_to_euler_and_translation(pose_matrix):
    # 从4x4矩阵提取欧拉角和位移
    rotation_matrix = pose_matrix[:3, :3]
    translation = pose_matrix[:3, 3]
    
    # 将旋转矩阵转换为欧拉角 (假设使用xyz顺序)
    euler_angles = transforms3d.euler.mat2euler(rotation_matrix, 'sxyz')
    euler_angles = np.array(euler_angles)

    return euler_angles, translation

def main():
    args = parse_args()
    
    # Reshape input matrices
    pre_grasp_file = np.load(args.predict_grasp_file)
    # grasp_pose_file = np.load(args.gt_pregrasp_pose_file)
    gt_grasp_pose_file = np.load(args.grasp_pose_file)
    
    # Compute Euler angles and translations
    euler1, trans1 = matrix_to_euler_and_translation(pre_grasp_file)
    # euler2, trans2 = matrix_to_euler_and_translation(grasp_pose_file)
    euler3, trans3 = matrix_to_euler_and_translation(gt_grasp_pose_file)
    
    
    # Compute differences
    # euler_diff = euler2 - euler1
    # translation_diff_predic_pregrasp = np.linalg.norm(trans2 - trans1)
    translation_diff_predic_grasp = np.linalg.norm(trans3 - trans1)


    pcd_h = o3d.io.read_point_cloud(args.hand_pcl_file)
    pcd_h = np.asarray(pcd_h.points)
    pcd_o = o3d.io.read_point_cloud(args.object_pcl_file)
    pcd_o = np.asarray(pcd_o.points)

    dis_h = compute_min_distance(pre_grasp_file,pcd_h)
    dis_o = compute_min_distance(pre_grasp_file,pcd_o)

    
    # Print results
    # print("Euler angles of pre_grasp_file (XYZ, degrees):", euler1)
    # print("Euler angles of grasp_pose_file (XYZ, degrees):", euler2)
    # print("Difference in Euler angles (degrees):", euler_diff)
    # print("Translation of pre_grasp_file:", trans1)
    # print("Translation of grasp_pose_file:", trans2)
    # print("Translation distance difference predict-pregrasp:", translation_diff_predic_pregrasp)
    print("Translation distance difference predict-grasp:", translation_diff_predic_grasp)
    print("distance between hand and predict pose:",dis_h)
    print("distance between object and predict pose:",dis_o)

if __name__ == "__main__":
    main()
