# AIアシスタント「ことり」
ChatGPTを使った，Windows用のAIアシスタント「ことり」です．現在試作段階中です．Windows上のほとんどの作業が口頭で行えることを目標にしています．起動中に「ことり」というウェイクワード（「ことり，〇〇して」など）とともに指示を行うことで，様々なPC上の操作をことりにやってもらったり，様々なことを調べてもらったりできます．

## 現在の機能
・質問してことりが知らない情報は，ことりが自分でWebページを巡回して情報を収集し，要約した情報をしゃべって教えてくれます．    
・指定したWebページを，ブラウザで表示してくれます．(「Youtube開いて」とか「Huluみたい」とか「Youtubeで〇〇検索して」も動作確認済み）  
・指定したプログラムを起動してくれます．(「Chrome起動して」などというと起動してくれる）しかし，動作しないプログラムも確認しています．  
・口頭でPCの音量を上げたり下げたりできます．（例：「音量を上げて」）  
・口頭でPCをスリープ状態にできます．（例：「スリープにして」）  
・口頭でメディアの再生・一時停止を切り替えられます（例：「再生止めて」「一時停止して」）．  
・緊急地震速報が来たら，音声で教えてくれる（ただし今は奈良県のみだけ対応）

現在試作段階であるため，うまく動かない機能があることがあります（てかあります）．

## 試しに使ってみる
実行には，Pythonの環境が整っている必要があります．
1. `pip install -r requirements.txt`をターミナル上で実行して，必要なライブラリをインストールします．
2. `run.bat`を実行します．

## 注意
・お金が発生することになるので，何百回も死ぬほど質問するとかはやめておいてください．  
・プログラム内にいろんなサービスのAPIキーがありますが，悪用しないでください．  
・このGitは，信用できるあなたにだけ公開しています．リンクを，Publicに公開しないでください． 

## 今後の展望
・ウェイクワードの認識の精度を向上させたい．  
・音声認識をGoogle Cloudを用いて行っているので，Windows内でローカルに音声認識を行うようにしたい．  
・PC内のファイルツリーの構造を理解させて，ファイルの移動やコピーといった操作を口頭で行えるようにしたい．  
・ユーザーがPC上で現在行っている作業を理解するような仕組みをつくりたい．

