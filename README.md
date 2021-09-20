# AIC project

## 環境構築
### install
```bash
$ git clone https://github.com/kosukess/AIC.git
$ cd AIC
$ sh docker/create_container.sh

# open docker container

$ sh environment/trt_pose_hand_env.sh
```
  
### dockerコンテナの起動(2回目以降)
```bash
$ sh docker/open.sh
```
  
### jupyterlabの起動
windows側でgoogle chromeを立ち上げ, 192.168.55.1:8888を開くことで, jupyterlabに入れる.  
passwordはnvidia
  

## ディレクトリ, ファイルについて
### jupyter notebookについて
- live_hand_pose.ipynb: 手のポーズ推定を行う
- gesture_data_collection_pose: ジェスチャーのデータを集める
- gesture_classification_live_demo: 手のクラス分類を行う