## evaluate on 5-fold cross validation
max=4
for i in `seq 0 $max`
do
  NUM="${var}$i"
  CUDA_VISIBLE_DEVICES='3' python main.py   ./data/ --arch resnet18 -j 32  --nce-t 0.07 --lr 1e-4 --nce-m 0.5 --low-dim 128 -b 75 \
  --result exp/fundus_amd/AMD_miccai_lambda2 --seedstart  $NUM  --multiaug    --multitaskposrot --multitask  --evaluate --resume savemodels/fold$NUM-epoch-2000.pth.tar
done
python read_result.py


## evaluate DR-pretrained model on AMD
rm -rf savemodels/result.txt
max=4
for i in `seq 0 $max`
do
  NUM="${var}$i"
  CUDA_VISIBLE_DEVICES='2,3' python main.py   ./data/ --arch resnet18 -j 32  --nce-t 0.07 --lr 1e-4 --nce-m 0.5 --low-dim 128 -b 75 \
  --result exp/fundus_amd/AMD_miccai_lambda2 --seedstart  $NUM  --multiaug    --multitaskposrot --multitask  --evaluate --resume savemodels/DR-pretrain-model.pth.tar
done
python read_result.py
