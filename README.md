This is the official code release for the paper "Learning Human-to-Robot Handovers through 3D Scene Reconstruction".

PIPELINE 
1. Prepare DexYCB dataset for FSGS input
  Download data
    python -m gdown 14up6qsTpvgEyqOQ5hir-QbjMB_dHfdpA 
  Environment setup
    module load Miniconda3/4.12.0  
    module load  CUDA/11.7.0
    module load GCC/9.3.0
    module load GCCcore/9.3.0
    module load Python/3.8.2
 
    export DEX_YCB_DIR='/home/e/eez095/dexycb_data'
    cd project/dex-ycb-toolkit/
    source dexycb/bin/activate
    export DEX_YCB_DIR=/home/e/eez095/dexycb_data
  Generate data
    export DEX_YCB_DIR=/home/e/eez095/dexycb_data
如果没有全部的数据集的话，需要更改数据集：
dex_ycb.py:
_SUBJECTS = [
  '20200813-subject-02',
]
python examples/create_dataset.py
  choose6/7/8cameras：
  Dexycb 数据folder的meta里删去seris name就行
  但无法删除主相机
  得到dexycb的colmap格式
[dex-ycb-toolkit]$ python examples/get_pointcloud.py --name 20200813-subject-02/20200813_145341
-> 得到python examples/visualize_pose.py --src /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/0_frame 1_frame 2_frame....

   
3. Segmentate hand and object
   [dex-ycb-toolkit]$ python examples/visualize_pose.py --src /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/0_frame
 得到的结果在colmap格式文件夹下(0_frame)
 /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/0_frame/handover_3D

1-2步骤合并：
  环境配置：
  module purge
  module load Miniconda3/4.12.0  
  module load  CUDA/11.7.0
  module load GCC/9.3.0
  module load GCCcore/9.3.0
  module load Python/3.8.2
 
  export DEX_YCB_DIR='/home/e/eez095/dexycb_data'
  cd project/dex-ycb-toolkit/
  source dexycb/bin/activate

  如果没有全部的数据集的话，需要更改数据集：
    dex_ycb.py:
    _SUBJECTS = [
      '20200813-subject-02',
    ]
    python examples/create_dataset.py
#单线程 批处理数据 多种数据级别都可以
   python run_1_2.py --dataSet 20200813-subject-02/20200813_145341 --dataSetBig /home/e/eez095/dexycb_data/20200813-subject-02
   
  # 多线程 只能处理/home/e/eez095/dexycb_data/20200813-subject-02级别的数据：
  python run_1_2_v3.py  --dataSetBig /home/e/eez095/dexycb_data/20200813-subject-02 --completed_file xxx --error_file xxx

3. 6DOF grasp
在sulis中：
module purge
module load CUDA/11.3.1
module load GCCcore/9.3.0
module load Python/3.8.2
cd project/pytorch_6dof-graspnet
source pytorch_6dof_grspnet/bin/activate

python -m demo.main --safe_grasp_folder /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame/

#参数：
#可以修改 visualiztion_utils.py/ min_grasps = 100
#可以修改main.py 54-111的参数
#grasp_pose_w储存在/home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame/gpw.npy中

在PC中：
  将第二步的handover_3D文件夹上传DRIVE 下载至lab PC
[Image]
  在pc电脑上
conda activate /home/robot_tutorial/anaconda3/6dofgraspnet_pt
(/home/robot_tutorial/anaconda3/6dofgraspnet_pt) robot_tutorial@smrtcam05:~/vgn_ws/src/wyk/pytorch_6dof-graspnet$ python -m demo.main 

参数：
可以修改 visualiztion_utils.py/ min_grasps = 100
  得到 final grasp的pose
pointcloud mean:
 [ 0.30915505 -0.04401238  0.96253157]

pointcloud mean:
 [ 0.1084676  -0.35709527  0.7904169 ]
best grasp in world coordinate:
 [[-0.63040221  0.47139975  0.61674577  0.01396373]
 [ 0.20771237 -0.66309559  0.71913821 -0.45649095]
 [ 0.74796301  0.58145207  0.32010141  0.74379988]
 [ 0.          0.          0.          1.        ]]
 
 grasp_pose_w储存在gpw.npy中
 
4. Sample pose
在sulis中：
module purge
module load CUDA/11.3.1
module load GCCcore/9.3.0
module load Python/3.8.2
cd project/pytorch_6dof-graspnet
source pytorch_6dof_grspnet/bin/activate

python -m demo.sample_v4 --base_dir /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame 


#可改参数：391-403 采样的参数 
#得到位姿，dexycb_data/20200813-subject-02/20200813_145341/70_frame/trajectory文件夹，里面有很多子文件夹，代表了路径，每个路径里有该路径下采样的点
#含义： i_0.npy(start pose.)   i_1.npy i_2.npy .... i_15.npy(intermeditate pose )    i_taget.npy(grasp position)     
在pc中进行
conda activate /home/robot_tutorial/anaconda3/6dofgraspnet_pt
(/home/robot_tutorial/anaconda3/6dofgraspnet_pt) robot_tutorial@smrtcam05:~/vgn_ws/src/wyk/pytorch_6dof-graspnet$ 
python -m demo.sample --base_dir /home/robot_tutorial/vgn_ws/src/wyk/pytorch_6dof-graspnet/demo/data_safe_grasp/54_frame_handover_3D


#input:264-268 input 需要从sulis迁移过来
#可改参数：393-412 采样的参数
#得到位姿，npz文件夹，里面有很多子文件夹，代表了路径，每个路径里有该路径下采样的点
#含义： i_0.npy(start pose.)   i_1.npy i_2.npy .... i_15.npy(intermeditate pose )    i_taget.npy(grasp position)              
#再将npz传到网盘 传输到sulis里去 /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/54_frame/npz
3-4步合并：
在sulis中：
环境配置：
module purge
module load CUDA/11.3.1
module load GCCcore/9.3.0
module load Python/3.8.2
cd project/pytorch_6dof-graspnet
source pytorch_6dof_grspnet/bin/activate


运行：
如果只处理一个frame，42-54注释掉，57-62运行，命令行写上grasp_one_frame的地址。
如果要处理一个文件夹，42-54运行，57-62注释掉，命令行写上dataset_path的地址。dataset_path格式参考如下，里面有很多frame.
python -m demo.run_3_4 --grasp_one_frame /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame --dataset_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341 --BigDataset_path /home/e/eez095/dexycb_data/20200813-subject-02

多线程版本，只能处理/home/e/eez095/dexycb_data/20200813-subject-02这样的数据：
python -m demo.run_3_4_v2 --BigDataset_path /home/e/eez095/dexycb_data/20200813-subject-02 --completed_file ./completed_datasets.txt --error_file ./error.txt --max_workers 8

多线程版本，只能处理/home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341这样的数据
python -m demo.run_3_4_v1 --dataset_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341 --max_threads 4

多线程版本，选部分帧，使用sample_v4,只能处理/home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341这样的数据

多线程版本，选部分帧，使用sample_v4,只能处理/home/e/eez095/dexycb_data/20200813-subject-02这样的数据
python -m demo.run_3_4_v3  --BigDataset_path /home/e/eez095/dexycb_data/20200813-subject-02 --completed_file ./log/completed_datasets.txt --error_file ./log/error.txt --max_workers 8

检查complete.txt中的data中是否有轨迹，将有轨迹的放入/home/e/eez095/project/pytorch_6dof-graspnet/log/non_empty_paths.txt 用这个txt进行下一步的FSGS
python demo/check_complete_file.py
PC（不建议在PC做了）：
环境配置：conda activate /home/robot_tutorial/anaconda3/6dofgraspnet_pt
python -m demo.run
5. FSGS reconstruction and Render image
环境配置:
module purge
module load CUDA/11.3.1
module load GCCcore/9.3.0
module load Python/3.8.2
cd project/FSGS
source FSGS/bin/activate
Train+Render:
python train.py --source_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame  --model_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame/FSGS_output/ --iteration 10000 --kk 


#--source_path 是已生成的colmap格式数据文件夹 --model_path 是结果文件夹 --n_views 是colmap文件夹里相机的数量，是自己设置的，需要注意 -kk是采用kk格式的输入文件

##--source_path 是已生成的colmap格式数据文件夹 --model_path 是结果文件夹
#输入还需要采样的位姿 dexycb_data/20200813-subject-02/20200813_145341/54_frame/npz，里面有0 1 2...文件夹，每个文件夹代表一条reaching路径中采样的点的位姿。
python render_v4.py --source_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame --model_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145341/70_frame/FSGS_output --iteration 10000 --kk --video

python render_v4.py --source_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145653/36_frame --model_path /home/e/eez095/dexycb_data/20200813-subject-02/20200813_145653/36_frame/FSGS_output --iteration 10000 --kk --video

5步批处理
#单线程 使用sample_v4版本
python run_5_v2.py --BigDataset_path /home/e/eez095/dexycb_data/20200813-subject-02 --step3_complete /home/e/eez095/project/pytorch_6dof-graspnet/log/non_empty_paths.txt
6. Supervised learning
环境：
use:------------------
module purge
module load CUDA/11.3.1
module load GCCcore/11.2.0 Python/3.9.6 

cd project/policy_learning/
source policy/bin/activate

python ./script/policy_v15.py --mode train --model_path ./model/v15.pth --train_txt_path /home/e/eez095/project/policy_learning/dataset_file/data_0310_no_obj23_train.txt --text_txt_path /home/e/eez095/project/policy_learning/dataset_file/data_0310_no_obj23_test.txt


install：------------------
module purge
module load CUDA/11.3.1
module load GCCcore/11.2.0 Python/3.9.6
cd project/policy learning
virtualenv policy
source policy/bin/activate


pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
pip install open3d
