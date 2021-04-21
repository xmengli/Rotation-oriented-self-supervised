## IEEE TMI21: Rotation-oriented Collaborative Self-supervised Learning for Retinal Disease Diagnosis

Pytorch implementation 

## Paper
IEEE TMI21: [Rotation-oriented Collaborative Self-supervised Learning for Retinal Disease Diagnosis.]

## Installation

* Install Python 3.7.4, Pytorch 1.1.0, torchvision 0.3.0 and CUDA 8.0
* Or Check requirements.txt
* Clone this repo
```
git clone https://github.com/xmengli999/Rotation-oriented-self-supervised
cd Rotation-oriented-self-supervised
```

## Data Preparation
* Download [Ichallenge-AMD dataset](https://drive.google.com/file/d/1ti0ozvMHCnq-PCX_CVc-Da98uJNmla8T/view?usp=sharing), 
[file_index](https://drive.google.com/file/d/1ts-Y8ePh_K_ijmBK8v3OfMIOhKMw-PSj/view?usp=sharing) <br/>
* Put them under `./data/`
* The folder should be 

`./data/Training400/resized_image_320/XXX.jpg` 

`./data/Training400/random_list.txt`


## Evaluate 
* Download [our models](https://pan.baidu.com/s/1NJdgbi7d3MiC7PATY6wKjA), password: h7z6, and put it under `./savemodels/`
* cd `scripts`
* Run scripts in `eval_fold.sh` to start the evaluation process
* 5-fold cross-validation results (Table I in the paper): 

| AUC    | Accuracy   | Precision    |
| ---------- | :-----------:  | :-----------: |
| 75.64%    | 87.09%   | 83.96%     |


* Download [our models](https://pan.baidu.com/s/10H09TiDgy5LgkHiYkaTp3A), password: 2juk, and put it under `./savemodels/`
* train on DR, test on AMD (Table II in the paper)  -- this step requires Pytorch 1.6.0:

| AUC    | Accuracy   | Precision    |
| ---------- | :-----------:  | :-----------: |
| 78.11%    | 87.85%   | 85.58%     |

## Train 
* cd `scripts`
* Check scripts in `train_fold.sh` to start the training process

## Note
* Contact: Xiaomeng Li (eexmli@ust.hk)
