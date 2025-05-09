! git clone https://github.com/kevin-moses/vision-aided-gan
%cd vision-aided-gan
!pip install vision_aided_loss ninja
%cd stylegan3

! python gen_images.py --outdir=out --trunc=1 --seeds=0-200 --network=../../drive/MyDrive/Colab\ Notebooks/network-snapshot-008657.pkl
