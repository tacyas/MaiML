## MaiML型データ内のテンプレート及びインスタンスにおける<br>参照関係の可視化アプリケーション<!-- omit in toc -->

<div align="right">国立九州工業大学プロジェクト</div>

### 1. アプリケーション概要
XMAILデータをGraphDBに登録し、そのデータをnodeJS WEBアプリケーション上でデータ一覧、ペトリネット図を照会・編集するアプリケーションである。ペトリネット図の編集結果は再びXMAILデータとしてファイルへ出力保存することができる。

### 2. 改訂履歴
|Author|Version|Last updated|Description|
|:-----:|:-----:|:-----:|:-----|
|Usk Tetsubayashi|1.0|2019/1/24|ドラフト|
|Usk Tetsubayashi|1.1|2021/2/8|ペトリネット編集, XMAILデータ出力|
|Koyasako|1.2|2022/2/10|MaiML対応,要素同士の関連表示機能|
|Koyasako|1.3|2023/2/13|Class層,Instance層ノード対応|

### 3. リポジトリ構成
各コンポーネントの利用方法は個別のREADME.mdを参照のこと。

|Repository|Technology|
|:-----|:-----|
|graph-db/|Neo4j, Cypher Query Language|
|xmail-viewer/|NodeJS|
|Documents/|Markdown|
|MaiML/|XML|
|docker-compose.yml|Docker|
|README.*| - |


### 4. サーバ起動手順

本アプリケーションは複数のDockerコンテナで構成されています。

|Repository|コンテナ|機能|
|:--|:--|:--|
|xmail-viewer|xmail_viewer|Webアプリケーション本体|
|graph-db|graph_db|Neo4jによるグラフDB|
|nginx|nginx|NginxによるWebサーバ|


これら全てのコンテナは docker-compose によって一括管理されており、下記のようなコマンドを用いて一括して開始/終了の操作が可能です。

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


### 5. アプリケーション使用方法

#### 5.1. 起動
下記URLへブラウザでアクセスする事によりアプリケーションのトップ画面が表示されます。

`http://＜ホスト名 or IPアドレス＞:3101`

※ローカル環境でのDocker machineの場合

[http://localhost:3101](http://localhost:3101)

#### 5.2. MaiML一覧表示画面

起動後の初期画面。以下の操作が可能。
* MaiMLファイルから一覧に追加
プルダウンメニューより `Import` &rarr; `Upload File` &rarr; MaiMLファイルをdrop &rarr; `実行`
* MaiMLを選択してPetri-Net表示
表示したいMaiMLの`NID`ボタン押下 &rarr; Petri-Net要素情報画面へ遷移
* MaiMLを選択して一覧から削除
表示したいMaiMLの`DEL`ボタン押下

#### 5.3. Petri-Net要素情報画面

MaiMLに格納されているPetri-Netと各要素の詳細情報の表示画面。

##### 5.3.1. Petri-Net図(左カラム)
選択したMaiMLに属するPetri-Netの全要素と、それらの要素と関連付けのある他MaiMLに属する要素を含んだPetri-Netを同時に表示する。

* 各要素が属するMaiMLによりグループ分類表示
* MaiMLグループのラベルは対応するMaiML NIDを示す
* Petri-Net の各要素を選択し、次項に示す編集操作が可能
* MaiMLグループをダブルクリックすると、そのMaiMLのPetri-Net要素情報画面へ遷移
（編集対象のMaiMLを切り替えることができる）

##### 5.3.2. 編集 + 要素情報表示(中カラム)
* ノード間の接続の削除：
左カラムで接続を選択して `Delete connection` 押下
* ノード間に接続を追加：
左カラムで place/transition を順に選択して `Create connection` 押下
* place/transition 追加：
`Add node` &rarr; `ID`文字列を入力, `Node type`選択 &rarr; `実行`
* 編集結果のMaiMLファイル出力：
`Export MaiML` &rarr; `Filename` を入力 &rarr; `実行`
* Node Details：
選択したノードに含まれる情報を表示

##### 5.3.3. Properties(右カラム)

左カラムで選択したノードに存在する属性情報を表示する。
各属性属性の下には別の複数の属性を持つことができる階層構造を構成する。

* `NID` : 各属性情報に付与された個別番号
* `Parent NID` : その情報を持つ親を示す `NID`


### 6. その他ツール・スクリプト等

- ~~MaiMLデータロード~~
`sh graph-db-loader.sh`
- ~~MaiMLデータ全削除~~
`sh graph-db-delete.sh`
- [MaiML編集アプリサポート用スクリプト](graph-db/app/Script/README.html) (XML署名についてはこちらに記載)

### 7. ドキュメント

- [ソフトウェア設計書](Documents/MaiML-App.html)


> Written with [StackEdit](https://stackedit.io/).
