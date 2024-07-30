## XMAIL編集アプリサポート用スクリプト

### XMAILからCypherクエリ文字列への変換ツール `xml2cypher.py`

#### 機能

入力XMAILファイルを Graph-DB へ登録するための Cypher クエリ文を出力する。

#### 実行方法

```bash
$ <path_to_py_file>/xml2cypher.py <input_file>
```
- 変換結果は stdout へ出力

#### 備考

引数で与えられた入力XMAILファイルのパスは Graph-DB 上に格納される。
これは次項の `xmail_export.py` に与えるパス名として利用する。
また、いったん入力されたXMAILファイルは Graph-DB との整合を保つため、消去やリネーム、上書き更新をしないよう注意が必要。

<br>

### XMAIL export スクリプト `xmail_export.py`

#### 機能

入力XMAILファイルに対して編集した情報を反映し、新規XMAILファイルを出力する。
XMAILデータ中には新規に自動生成した uuid を設定する。
また、XMLDsig に従ったXML署名を行い、検証可能とする。

##### 入力
- Graph-DB上から取得するXMAIL更新データ(XMAIL node id の数値によって指定)
- 更新元のXMAILファイル
- 出力XMAILへの署名用鍵ファイル

##### 出力
- 更新済みXMAILファイル

#### 実行環境構築

```bash
$ pip install neo4j
$ pip install lxml
$ pip install signxml
```

#### 実行方法

```bash
$ <path_to_py_file>/xmail_export.py --host $GRAPH_DB_IP --node-id <XMAIL node id> --output <output_file> <input_file>
```
##### コマンドライン・オプション
|option|default|description|
|:--|:--:|:--|
|--node-id| - |必須, 取得するXMAILデータの node id を整数値で指定する|
|--output|`None`|出力するXMAILファイル名|
|--host|localhost:7687|Neo4j接続URI, ポート番号は省略可|
|--user|なし|Neo4j接続ユーザ名|
|--password|なし|Neo4j接続パスワード|
|--key-file| - |XML署名の鍵ファイル|
|--key-passphrase| - |XML署名の鍵パスフレーズ|


#### ファイル構成

- `xmail_export.py` : XMAIL Export スクリプト本体
- `cypher_query.py` : Graph-DB クエリ発行ライブラリ
- `cypher_api.json` : クエリAPI定義ファイル(JSON形式)
- `example.key`     : XML-Signature 生成のための鍵ファイル


### 補足: XML署名について

#### XML署名に使用する鍵の作成

```bash
$ openssl genrsa -aes256 -out example.key
Generating RSA private key, 2048 bit long modulus
............................................................+++
.....................................................+++
e is 65537 (0x10001)
Enter pass phrase for example.key:
Verifying - Enter pass phrase for example.key:
$ 
```

(注) 鍵ファイル名と pass phrase はアプリ側で固定文字列として管理しているため下記に設定する。
- ファイル名 : `example.key`
- pass phrase : `secret`
- 暗号の種別やビット長は任意

#### 署名の検証方法

```bash
$ xmlsec1 --verify sample.xmail
OK
SignedInfo References (ok/all): 1/1
Manifests References (ok/all): 0/0
$ 
```