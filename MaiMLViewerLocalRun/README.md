## MaiML型データ内のテンプレート及びインスタンスにおける<br>参照関係の可視化アプリケーション<!-- omit in toc -->

### 1. アプリケーション概要
MaiMLデータをGraphDBに登録し、そのデータをnodeJS WEBアプリケーション上でデータ一覧、ペトリネット図、汎用データコンテナ等の詳細情報を表示するアプリケーションである。

### 2. アプリケーション使用方法

#### 2.1. 起動
下記URLへブラウザでアクセスする事によりアプリケーションのトップ画面が表示される。

[http://localhost:3000](http://localhost:3000)

#### 2.2. MaiML一覧表示画面

起動後の初期画面。以下の操作が可能。
* MaiMLファイルから一覧に追加
プルダウンメニューより `Import` &rarr; `Upload File` &rarr; MaiMLファイルをdrop &rarr; `実行`
* MaiMLを選択してPetri-Net表示
表示したいMaiMLの`NID`ボタン押下 &rarr; Petri-Net要素情報画面へ遷移
* MaiMLを選択して一覧から削除
表示したいMaiMLの`DEL`ボタン押下

#### 2.3. Petri-Net要素情報画面

MaiMLに格納されているPetri-Netと各要素の詳細情報の表示画面。

##### 2.3.1. Petri-Net図(左カラム)
MaiML一覧表示画面で選択したMaiMLに属するPetri-Netの要素と、それらの要素と関連付けのある他MaiML（２代前後）に属する要素を含んだPetri-Netを同時に表示する。

* 各要素が属するMaiMLによりグループ分類表示
* Petri-Net の各要素を選択し、次項に示す編集操作が可能
* MaiMLグループをダブルクリックすると、そのMaiMLのPetri-Net要素情報画面へ遷移
（編集対象のMaiMLを切り替えることができる）

##### 2.3.2. ~~編集 +~~ 要素情報表示(中カラム) + insertion要素情報表示
* `Register PNML position`ボタン：</br>
    MaiML一覧表示画面で選択したMaiMLファイルのペトリネット図の各ノードの座標をサーバーに保存
* Node Details：</br>
選択したノードに含まれる情報を表示
* Insertion contents：</br>
選択したノードが持つinsertion要素の情報を表示
  
##### 2.3.3. Properties(右カラム)

左カラムで選択したノードに存在する属性情報を表示する。
各属性属性の下には別の複数の属性を持つことができる階層構造を構成する。

* `NID` : 本アプリケーション内で各属性情報に付与された個別番号
* `Parent NID` : その情報を持つ親を示す `NID`


### 3. アプリケーションの環境構築方法
SETUP_AND_RUN.md、もしくは、SETUP_AND_RUN_ForWindows.mdを参照してください。

