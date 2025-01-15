import subprocess
import argparse
import os
import subprocess
import re

def execute_commands(safe_grasp_folder):
    # 定义要执行的命令
    commands = [
        f"python -m demo.main --safe_grasp_folder {safe_grasp_folder}",
        f"python -m demo.sample --base_dir {safe_grasp_folder}"
    ]

    # 执行命令
    for cmd in commands:
        print(f"Executing: {cmd}")
        try:
            # 使用 shell=True 来允许 conda activate 命令正常工作
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {cmd}")
            print(f"Error message: {e}")
            return False  # 如果有错误发生，返回False
        print(f"Command completed: {cmd}\n")

    print("All commands executed.")
    return True  # 如果所有命令都成功执行，返回True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='task 3 and 4')
    
    # 添加参数及其默认值
    parser.add_argument('--grasp_one_frame', type=str, default='/home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame',help='dataset for one frame')
    parser.add_argument('--dataset_path', type=str, default='/home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341')
    parser.add_argument('--BigDataset_path', type=str, default='/home/e/eez095/dexycb_data/20200813-subject-02')
    

    args = parser.parse_args()
    grasp_one_frame = args.grasp_one_frame
    dataset_path = args.dataset_path
    BigDataset_path = args.BigDataset_path


    ### process data like /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341
    data_frames = [f for f in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, f))]
    # Execute frame-specific command for each data_frame
    for data_frame in data_frames:
        if not re.match(r'\d+_frame$', os.path.basename(data_frame)):
            continue
        else:
            success = execute_commands(os.path.join(dataset_path, data_frame))
            if success:
                # print("All commands executed successfully.")
                continue
            else:
                print(f"There was an error during execution {data_frame}.")


    ### process data for one frame like /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame
    # success = execute_commands(grasp_one_frame)
    # if success:
    #     print("All commands executed successfully.")
    # else:
    #     print(f"There was an error during execution.")

    ### process data like /home/e/eez095/dexycb_data/20200813-subject-02
    # dataset_paths = [a for a in os.listdir(BigDataset_path) if os.path.isdir(os.path.join(BigDataset_path, a))]
    # for d in dataset_paths:
    #     dataset_path_ = os.path.join(BigDataset_path,d)
    #     data_frames = [f for f in os.listdir(dataset_path_) if os.path.isdir(os.path.join(BigDataset_path,dataset_path_, f))]
    #     # Execute frame-specific command for each data_frame
    #     for data_frame in data_frames:
    #         if not re.match(r'\d+_frame$', os.path.basename(data_frame)):
    #             continue
    #         else:
    #             success = execute_commands(os.path.join(dataset_path_, data_frame))
    #             if success:
    #                 # print("All commands executed successfully.")
    #                 continue
    #             else:
    #                 print(f"There was an error during execution {data_frame}.")