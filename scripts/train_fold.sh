## our method trained on AMD,
max=4
for i in `seq 0 $max`
do
  NUM="${var}$i"
  CUDA_VISIBLE_DEVICES='3' python main.py   ./data/ --arch resnet18 -j 32  --nce-t 0.07 --lr 1e-4 --nce-m 0.5 --low-dim 128 -b 75 \
  --result exp/fundus_amd/AMD_miccai --seedstart  $NUM  --multiaug    --multitaskposrot --multitask
done


## our method trained on DR,
### modify main.py line 140 to import datasets.fundus_kaggle_dr as medicaldata
max=4
for i in `seq 0 $max`
do
  NUM="${var}$i"
  CUDA_VISIBLE_DEVICES='3' python main.py   ./data/ --arch resnet18 -j 32  --nce-t 0.07 --lr 1e-4 --nce-m 0.5 --low-dim 128 -b 128 \
  --result exp/fundus_dr/DR_miccai --seedstart  $NUM  --multiaug    --multitaskposrot --multitask
done