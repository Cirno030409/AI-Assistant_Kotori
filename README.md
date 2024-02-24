# AIアシスタント「ことり」
ChatGPTを使った，Windows用のAIアシスタント「ことり」です．現在試作段階中です．Windows上のほとんどの作業が口頭で行えることを目標にしています．起動中に「ことり」というウェイクワードとともに指示を行うことで，様々なPC上の操作を口頭で行うことができます．

## 現在の機能
・ことりが知らない情報は，ことりが自分でWebページを巡回して情報を収集します．  
・指定したWebページを，ブラウザで表示してくれます．(YoutubeやHuluとか）  
・指定したプログラムを起動してくれます．(「Chrome起動して」などというと起動してくれる）しかし，動作しないプログラムも確認しています．  
・口頭でPCの音量を上げたり下げたりできます．  
・口頭でPCをスリープ状態にできます．  

## 試しに使ってみる
実行には，Pythonの環境が整っている必要があります．
1. `pip install -r requirements.txt`を実行して，必要なライブラリをインストールします．
2. `run.bat`を実行します．


