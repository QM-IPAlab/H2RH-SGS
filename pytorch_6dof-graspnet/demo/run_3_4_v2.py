# multi thread process data like /home/e/eez095/dexycb_data/20200813-subject-02
import subprocess
import os
import re
import argparse
from tqdm import tqdm
import concurrent.futures
from threading import Lock

# 锁，用于文件写入操作的线程安全
lock = Lock()

def execute_commands(safe_grasp_folder, error_file):
    """执行指定命令并记录错误"""
    commands = [
        f"python -m demo.main --safe_grasp_folder {safe_grasp_folder}",
        f"python -m demo.sample --base_dir {safe_grasp_folder}"
    ]

    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            with lock, open(error_file, 'a') as ef:
                ef.write(f"Error executing command: {cmd}\n")
                ef.write(f"Error message: {e}\n\n")
            return False
    return True

def process_dataset_path(dataset_path, completed_file, error_file):
    """处理单个 dataset_path 的所有帧目录"""
    data_frames = [
        f for f in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, f)) and re.match(r'\d+_frame$', os.path.basename(f))
    ]

    all_success = True
    for data_frame in data_frames:
        safe_grasp_folder = os.path.join(dataset_path, data_frame)
        success = execute_commands(safe_grasp_folder, error_file)
        if not success:
            all_success = False

    with lock, open(completed_file, 'a') as cf:
        cf.write(f"{dataset_path}\n")
    return all_success

def process_big_dataset(BigDataset_path, completed_file, error_file, max_workers=4):
    """处理大数据集路径中的所有子数据集"""
    # 读取已处理数据集
    if os.path.exists(completed_file):
        with open(completed_file, 'r') as cf:
            completed_datasets = {line.strip() for line in cf.readlines()}
    else:
        completed_datasets = set()

    dataset_paths = [
        os.path.join(BigDataset_path, d)
        for d in os.listdir(BigDataset_path)
        if os.path.isdir(os.path.join(BigDataset_path, d))
    ]

    # 多线程处理数据集
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_dataset = {}

        for dataset_path in dataset_paths:
            if dataset_path in completed_datasets:
                print(f"Skipping already processed dataset: {dataset_path}")
                continue

            future = executor.submit(process_dataset_path, dataset_path, completed_file, error_file)
            future_to_dataset[future] = dataset_path

        # 监控任务完成情况
        for future in tqdm(concurrent.futures.as_completed(future_to_dataset), desc="Processing datasets"):
            dataset_path = future_to_dataset[future]
            try:
                if future.result():
                    print(f"Successfully processed dataset: {dataset_path}")
                else:
                    print(f"Failed to process dataset: {dataset_path}")
            except Exception as e:
                print(f"Error processing dataset {dataset_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process big dataset with error handling and tracking.')
    parser.add_argument('--BigDataset_path', type=str, required=True, help='Path to the big dataset.')
    parser.add_argument('--completed_file', type=str, default='./completed_datasets.txt', help='File to record completed datasets.')
    parser.add_argument('--error_file', type=str, default='./error.txt', help='File to record error messages.')
    parser.add_argument('--max_workers', type=int, default=4, help='Maximum number of concurrent workers.')

    args = parser.parse_args()

    process_big_dataset(
        BigDataset_path=args.BigDataset_path,
        completed_file=args.completed_file,
        error_file=args.error_file,
        max_workers=args.max_workers
    )
