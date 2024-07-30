## Neo4j DB構築＋初期データ投入

#### 機能構成

技術要素としては下記の２機能を用いた構成である。
1. DBサーバ : Neo4j (Dockerコンテナ)
1. XMAILデータからCypherへの変換 : Python および xml.etree.ElementTree

#### スクリプト構成

まずDBサーバを起動し、DBクエリ動作が可能な状態となった後に、XMAILデータから変換したCypherクエリの形式でDBサーバへ投入する、というのが基本的な流れ。

- DBサーバ起動  : `docker-run-neo4j.sh`
- XMAILフォルダ内を全てDBへ投入 : `setup-XMAIL.sh`
  - 指定されたXMAILファイルをDBへ投入 : `app/Script/load-xmail.sh`
  - 指定されたXMAILファイルをCypherへ変換 : `app/Script/xml2cypher.py`

※ DBサーバ起動後は、サーバがクエリに対応可能な状態となるまで時間がかかるため、直後はDB投入のスクリプトは異常終了する可能性あり。可能ならDB投入前にDB稼働を確認しておくとよい。

#### スクリプト実行手順

```sh
cd kyutech/graph-db
sh ./docker-run-neo4j.sh

# 投入するXMAILファイルを事前に ./XMAIL 以下に置く
# DBサーバ稼働を事前にブラウザ等で確認
sh ./setup-XMAIL.sh

# あとから個別にXMAILファイルを追加する場合
sh ./app/Script/load-xmail.sh <XMAIL file>
```
