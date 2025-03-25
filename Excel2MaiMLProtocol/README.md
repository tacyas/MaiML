# Excel2DocandProtocolofMaiML

# A: 概要
計測分析の手順や条件等の計画情報を記載したエクセルファイルを入力ファイルとし、
入力データをもとに、`protocolFileRootType` タイプの MaiML データファイルを作成するプログラム。

# B: 実行方法
## 入出力データ
### 入力データ
1. **エクセルファイル**  
   `INPUT/excel/エクセル説明.xlsx` を参照。  
   入力するエクセルのファイルパスは、実行引数の有無による。
   - 実行引数無しの場合、`USERS/usersettings.py` に記載した１つのエクセルのファイルパスに対してプログラムを実行。
   - 実行引数有りの場合、引数で指定したディレクトリに存在する全てのエクセルファイルに対してそれぞれプログラムを実行。

### 出力データ
1. **入力データをMaiMLデータフォーマットへ変換したMaiMLファイル**  
   出力するMaiMLファイルパスは、実行引数の有無による。
   - 実行引数無しの場合: `OUTPUT/output.maiml`
   - 実行引数有りの場合: 引数で指定したディレクトリに、入力ファイル名の拡張子を `.maiml` に変換したファイル。

## 実行方法
### その1. 実行引数無しで実行
1. **入力ファイルを準備**
   - `USERS/usersettings.py` の入力ファイルのパス (`_IN_EXCEL_FILENAME`)、 `<maiml>` 要素の属性 (`_MAIML_ATTR`) を編集。
   - 指定した入力ファイルのパスにエクセルファイルを配置。
2. **コマンド実行**
   ```sh
   python excel2protocolMaiML.py
   ```
   または
   ```sh
   python excel2protocolMaiML2.py
   ```

### その2. 実行引数にディレクトリを指定して実行
1. **入力ファイルを準備**
   - `USERS/usersettings.py` の `<maiml>` 要素の属性 (`_MAIML_ATTR`) を編集。
   - `/INPUT/XXXXX/` ディレクトリにエクセルファイルを配置。  
     ※ `XXXXX` は任意の名前。
2. **コマンド実行**
   ```sh
   python excel2protocolMaiML2.py XXXXX
   ```

# C: python実行環境の構築
## Python 3.9以上
- 実行パスが通っていること

## 実行に必要なPythonパッケージ
- `requirements.txt` に記載


# D: sampleファイルの実行
## ①`/INPUT/test/`ディレクトリに入力ファイルが存在していることを確認
- exampleX.xlsx
## ②`/USERS/usersettings.py`に名前空間の定義が追加されていることを確認
   ```sh
      'xmlns:BBBB="http://BBBB.corp/index.jp"'
      'xmlns:BBBBHPLC="http://BBBB.corp/ontology/hplc"'
      'xmlns:CDF="http://BBBB.corp/ontology/cdf"'
   ```
## ③コマンド実行
   ```sh
   python excel2protocolMaiML2.py test
   ```
## ④`/INPUT/test`ディレクトリに出力されたMaiMLファイルを確認
- exampleX.maiml
