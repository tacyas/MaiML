## MaiML型データ内のテンプレート及びインスタンスにおける<br>参照関係の可視化アプリケーション<!-- omit in toc -->

### 1. アプリケーション概要
MaiMLデータをGraphDBに登録し、そのデータをnodeJS WEBアプリケーション上でデータ一覧、ペトリネット図、汎用データコンテナ等の詳細情報を表示するアプリケーションである。


### 2. リポジトリ構成
各コンポーネントの利用方法は個別のREADME.mdを参照のこと。

|Repository|Technology|
|:-----|:-----|
|graph-db/|Neo4j, Cypher Query Language|
|xmail-viewer/|NodeJS|
|Documents/|Markdown|
|MaiML/|XML|
|docker-compose.yml|Docker|
|README.*| - |


### 3. サーバ起動手順

本アプリケーションは複数のDockerコンテナで構成されている。

|Repository|コンテナ|機能|
|:--|:--|:--|
|xmail-viewer|xmail_viewer|Webアプリケーション本体|
|graph-db|graph_db|Neo4jによるグラフDB|
|nginx|nginx|NginxによるWebサーバ|


これら全てのコンテナは docker-compose によって一括管理されており、下記のようなコマンドを用いて一括して開始/終了の操作が可能である。

- コンテナ作成＆起動  
`docker-compose up -d`
- コンテナ停止  
`docker-compose stop`
- 停止中コンテナの起動  
`docker-compose start`
- コンテナ再起動  
`docker-compose restart`
- コンテナ終了＆イメージ削除  
`docker-compose down --rmi all`
- データも全て削除
`docker-compose down --rmi all --volumes`


### 4. アプリケーション使用方法

#### 4.1. 起動
下記URLへブラウザでアクセスする事によりアプリケーションのトップ画面が表示される。

`http://＜ホスト名 or IPアドレス＞:3101`

※ローカル環境でのDocker machineの場合

[http://localhost:3101](http://localhost:3101)

#### 4.2. MaiML一覧表示画面

起動後の初期画面。以下の操作が可能。
* MaiMLファイルから一覧に追加
プルダウンメニューより `Import` &rarr; `Upload File` &rarr; MaiMLファイルをdrop &rarr; `実行`
* MaiMLを選択してPetri-Net表示
表示したいMaiMLの`NID`ボタン押下 &rarr; Petri-Net要素情報画面へ遷移
* MaiMLを選択して一覧から削除
表示したいMaiMLの`DEL`ボタン押下

#### 4.3. Petri-Net要素情報画面

MaiMLに格納されているPetri-Netと各要素の詳細情報の表示画面。

##### 4.3.1. Petri-Net図(左カラム)
選択したMaiMLに属するPetri-Netの全要素と、それらの要素と関連付けのある他MaiMLに属する要素を含んだPetri-Netを同時に表示する。

* 各要素が属するMaiMLによりグループ分類表示
* Petri-Net の各要素を選択し、次項に示す編集操作が可能
* MaiMLグループをダブルクリックすると、そのMaiMLのPetri-Net要素情報画面へ遷移
（編集対象のMaiMLを切り替えることができる）

##### 4.3.2. ~~編集 +~~ 要素情報表示(中カラム) + insertion要素情報表示
* `Register PNML position`ボタン：
  ペトリネット図の各ノードの座標をサーバーに保存
* Node Details：
選択したノードに含まれる情報を表示
* Insertion contents：
選択したノードが持つinsertion要素の情報を表示
  
##### 4.3.3. Properties(右カラム)

左カラムで選択したノードに存在する属性情報を表示する。
各属性属性の下には別の複数の属性を持つことができる階層構造を構成する。

* `NID` : 本アプリケーション内で各属性情報に付与された個別番号
* `Parent NID` : その情報を持つ親を示す `NID`



