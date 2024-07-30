## Cypher クエリI/F定義モジュール

#### 概要

Node.js環境からDBアクセスのためのCypherクエリ文を取得するI/Fを用意しています。
クエリ文は下記の要領で取得することができます。

1. I/F定義モジュール `cypher_api.js` の `get_cypher()` を用いてクエリ文の文字列を取得
1. `get_cypher()`に渡す引数は、I/F名とパラメータ（`query_sample.js` にあるコメントアウト部分を参照）
1. I/F名の一覧、および各I/Fの仕様については `cypher_api.js` 中のデータ定義部分コメントを参照下さい。
1. `get_cypher()` では引数チェックをしていないので、渡すパラメータの個数違い等のないようにご注意下さい。

#### クエリ文字列の取得サンプル
```
const cypher_api = require('./cypher_api.js');
query_str1 = cypher_api.get_cypher('get_xmail'));
query_str2 = cypher_api.get_cypher('get_PN', 1234));
```

#### ※備考 : I／F定義におけるパラメータ

Neo4j側のAPIにはパラメータ機能があり、`$`記号で始まるパラメータ名を含むCypher文字列と
パラメータをセットにしてAPIに渡すことが可能な仕組みです。
本来はその機能を用いた実装が理想的ですが、DB本体側とAPIドライバ側とのバージョン対応関係によっては
期待通りの動作をしないようでしたので、本モジュールの中で `$`記法のCypher文字列を
最終的なCypher文字列に変換するロジックを組み込みました。

#### ファイル構成

- `cypher_api.js` : I/F定義モジュール本体
- `query_sample.js` : I/F定義データのJSON変換ツール, I/F呼び出しサンプル
- `cypher_api.json` : JSON形式のI/F定義データ(Pythonからの利用を意図したもの)
- `cypher_test.py` : I/F定義テストツール
