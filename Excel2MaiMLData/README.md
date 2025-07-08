# Excel2MaiMLData
<br/>

# A: 概要
計測分析の手順や条件等の計画情報を記載したMaiMLファイル、その計画を基に実行した結果を記載したエクセルファイルを入力ファイルとし、
入力データをマージし、`maimlRootType` タイプの MaiML データファイルを作成するプログラム。

# B: 実行方法
## 入出力データ
### 入力データ
1. **MaiMLファイル**  
   入力するMaiMLのファイルパスは、実行引数の有無による。
   - 実行引数無しの場合、"/INPUT/maiml/"+"`USERS/usersettings.py`に記載した１つのMaiMLのファイル名"。
   - 実行引数有りの場合、引数で指定したディレクトリに存在する1つのMaiMLファイル。

2. **エクセルファイル**  
   入力するエクセルのファイルパスは、実行引数の有無による。
   - 実行引数無しの場合、"/INPUT/excel/"+"`USERS/usersettings.py`に記載した１つのエクセルのファイル名"。
   - 実行引数有りの場合、引数で指定したディレクトリに存在する1つのエクセルファイル。
   - 記載方法は、`settings/ExcelFormat.xlsx`を参照。

3. **外部ファイル**
   MaiMLファイルに<insertion>要素として挿入する外部ファイル。
   入力する外部ファイルのファイルパスは、実行引数の有無による。
   - 実行引数無しの場合、"/INPUT/others/"+"エクセルに記載した外部ファイル名"。
   - 実行引数無しの場合、"引数で指定したディレクトリ"+"/"+"エクセルに記載した外部ファイル名"。

### 出力データ
1. **入力データをマージしたMaiMLファイル**  
   出力するMaiMLファイルパスは、実行引数の有無による。
   - 実行引数無しの場合: "OUTPUT/" + "USERS/usersettings.py"に記載した_MaiML_FILENAME 。
   - 実行引数有りの場合: "引数で指定したディレクトリ"+"/"+"入力MaiMLファイル名"+ "_output.maiml"。

## 実行方法
### その1. 実行引数無しで実行
1. **入力ファイルを準備**
   - `USERS/usersettings.py` の入力ファイルのパス ("_INPUT_MaiML_PATH","_IN_EXCEL_FILENAME") を編集。
   - MaiMLファイル、エクセルファイル、挿入する外部ファイルをそれぞれ配置。
2. **コマンド実行**
   ```sh
   python excel2dataMaiML2.py
   ```
   または
   ```sh
   python excel2dataMaiML2.py
   ```

### その2. 実行引数にディレクトリを指定して実行
1. **入力ファイルを準備**
   - `/INPUT/XXXXX/` ディレクトリにMaiMLファイル、エクセルファイル、挿入する外部ファイルを配置。  
     ※ `XXXXX` は任意の名前。
2. **コマンド実行**
   ```sh
   python excel2dataMaiML2.py XXXXX
   ```

# C: python実行環境の構築
## Python 3.9以上
- 実行パスが通っていること

## 実行に必要なPythonパッケージ
- `settings/requirements.txt` に記載


# D: sampleファイルの実行
## ①`/INPUT/test/`ディレクトリに入力ファイルが存在していることを確認
- input.xlsx
- input.maiml
- Axoneme-56.008.tif
- test.txt
## ②コマンド実行
   ```sh
   python excel2protocolMaiML2.py test
   ```
## ③`/INPUT/test`ディレクトリに出力されたMaiMLファイルを確認
- input_output.maiml
