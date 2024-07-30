<div style="text-align: center;">
ソフトウェア設計書
</div>

# MaiML型データ内のテンプレート及びインスタンスにおける参照関係の可視化アプリケーション <!-- omit in toc -->

<div style="text-align: right;">
2023.02.13 株式会社マイクロネットテクノ
</div>

---

## 1. 概要

本システムはウェブ・ブラウザ上で動作するウェブ・アプリケーションである。ユーザは任意のMaiML型データを入力してブラウザ上で情報を表示させたり、また編集操作することが可能である。主な機能を下記に示す。

- 複数のMaiML型データファイルを入力可能
- 任意のMaiML型データを選択して内部のペトリネット構造、および構成要素の参照関係をGUI表示
- 編集対象のMaiMLに属するノードと同一uuidとなるノードをもつMaiMLを同時に一つのグラフとして画面表示
- グラフ構成要素のペトリネット要素や、参照関係をもつテンプレート、インスタンスを任意に選択して詳細情報を表示
- ペトリネットに対してplaceやtransitionノードの追加編集
- ペトリネットのarc要素や、その他の参照関係を示すエッジ接続を任意に追加、削除
- 編集結果を新規のMaiML型データとしてファイル出力
- MaiMLファイル出力時の新規uuid自動付与
- MaiMLデータの改竄防止のためのXML署名機能


## 2. システム構成

本システムは下記のモジュールから構成されている。
1. GUI機能 : `Node.js` アプリケーション
2. 1の機能を補助する `Python` スクリプト
3. MaiML型データを管理するグラフDBシステム `Neo4j`
4. ウェブサーバ `Nginx`

これらのモジュールのサーバ上における実装は `Docker` を用いた3つの仮想化コンテナによって構成し、それらのコンテナは `docker-compose` を用いて一括運用管理が可能となっている。この仮想化システム導入により、サーバへのインストールから起動、運用管理に至るまでの手順簡略化を実現している。

それぞれのモジュール間の機能の関連を下図に示す。

```plantuml
'skinparam backgroundColor lightgray

node client {
    file "MaiML data" as MaiML
    component "Web browser" as browser
}
node server {
    package "container 'nginx'" as cn {
        component Nginx
    }
    package "container 'xmail_viewer'" as cx {
        component "Node.js" as node
        component "Python scripts" as py
    }
    package "container 'graph_db'" as gx {
        database "Neo4j" as db
    }
    storage "MaiML Storage" as st
}

MaiML --> browser
MaiML <-- browser
browser .. Nginx : HTTP REST API
Nginx .. node    : URL '/' (reverse proxy)
Nginx <-- st      : URL '/download/' \n MaiML export
node .. db
node -- py
node -left-> st : MaiML import
py .. db
py <---> st

```

## 3. MaiMLデータ編集機能仕様

[MaiML編集機能](MaiML-Edit.html)

## 4. システム内部のデータ構造と動作

### 4.1. MaiMLデータの仕様とグラフDBモデリング

[MaiMLデータの仕様とグラフDBモデリング](MaiML-DesignDocuments.html)

### 4.2. REST API 仕様

本アプリケーションのクライアント・インターフェースは RESTful API で実装している。
このAPI仕様についてURLパスと概略機能の一覧を下表に示す。

(*) 'NID' はGraph DB上におけるノードを一意的に対応付ける数値を意味する。

|HTTP Method|Path|Parameter|Description|
|:--:|:--|:--:|:--|
|GET|/||redirect to '/xmail-list'|
|GET|/xmail-list||MaiML一覧データ取得|
|POST|/xmail-upload||MaiMLデータアップロード|
|||filename|MaiMLファイル名|
|||xmail|MaiMLデータ|
|POST|/xmail-delete||MaiMLデータ削除|
|||nid|MaiML NID|
|GET|/petrinet/view||redirect to '/xmail-petrinet'|
|POST|/petrinet/xmail-petrinet||MaiMLペトリネット図データ取得(node 及び edge)|
|||nid|MaiML NID|
|POST|/node/||MaiMLに属する Petri-Net全要素の一括取得|
|||nid|MaiML NID|
|POST|/node/node||指定したPetri-Net 要素の取得|
|||nid|Petri-Net 要素NID|
|POST|/node/node-list||指定した複数の Petri-Net 要素の一括取得|
|||[nid, ...]|Petri-Net 要素NIDのリスト|
|POST|/node/node-material||Petri-Net 要素テンプレート取得|
|||node_id|Petri-Net 要素NID|
|POST|/node-edit/pnarc-check||arc作成可否チェック|
|||src_nid|Source NID|
|||dst_nid|Destination NID|
|POST|/node-edit/pnarc-create||arc作成|
|||src_nid|Source NID|
|||dst_nid|Destination NID|
|POST|/node-edit/pnarc-delete||arc削除|
|||src_nid|Source NID|
|||dst_nid|Destination NID|
|POST|/node-edit/node-creation||ノード作成|
|||nid|MaiML NID|
|||id|place / transition に付与するid|
|||type|Type (`place` or `transition`)|
|POST|/node-edit/export||MaiMLエクスポート|
|||nid|MaiML NID|
|||outfile|exported MaiML|
