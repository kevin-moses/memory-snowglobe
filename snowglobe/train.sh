# conda
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
bash Anaconda3-2024.10-1-Linux-x86_64.sh  

# ssh
ssh -i firstkey.pem ubuntu@{ip}
# scp
scp -i firstkey.pem  photo_data_512.zip ubuntu@{ip}:gan3/photo_data_512.zip

# clone repo
git clone https://github.com/NVlabs/stylegan3.git
conda env create -f environment.yml -n gan3
pip install vision_aided_loss

# optional
conda install psutil
conda install tensorboard

# for real
# nohup python train.py --outdir=../training-runs --cfg=stylegan3-t --data=../photo_data_512.zip --gpus=8 --batch=32 --gamma=8 --snap=30 --resume=../training-runs/00016-stylegan3-t-photo_data_512-gpus8-batch32-gamma8/network-snapshot-000840.pkl  > output.log 2>&1 &

#vision aided
# nohup python train.py --outdir=../training-runs --cfg=stylegan3-t --data=../photo_data_512.zip --gpus=8 --batch=32 --gamma=8 --snap=30 --resume=../training-runs/00016-stylegan3-t-photo_data_512-gpus8-batch32-gamma8/network-snapshot-000840.pkl  > output.log 2>&1 &

nohup python train.py --outdir=../vision-training-runs --cfg=stylegan3-t --data=../../photo_data_512.zip --gpus=8 --batch=24 \
 --gamma=8 --snap=30 --mbstd-group=3 \
 --resume=../vision-training-runs/00016-stylegan3-t-photo_data_512-gpus8-batch24-gamma8-clip+dino+vgg+face_seg-cv_loss_multilevel_sigmoid_s+multilevel_sigmoid_s+sigmoid_s+sigmoid_s/network-snapshot-002885.pkl \
 --cv=input-clip+dino+vgg+face_seg-output-conv_multi_level+conv_multi_level+conv+conv --cv-loss=multilevel_sigmoid_s+multilevel_sigmoid_s+sigmoid_s+sigmoid_s \
 --aug=ada  --warmup=0 > output.log 2>&1 &

# watch
watch -n 1 nvidia-smi 

# get outputs
scp -i firstkey.pem ubuntu@104.171.203.34:gan3-a100/training-runs/00014-stylegan3-t-photo_data_512-gpus8-batch32-gamma8/fakes001520.png \
 /mnt/c/Users/kevinmoses/code/data/00014-output/fakes001520.png