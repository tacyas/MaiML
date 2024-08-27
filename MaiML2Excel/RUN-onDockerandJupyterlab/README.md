# [How to build 'MaiML to Excel']

## (a) Docker install
- 前提：Docker Desktop、Rancher Desktop 等のDocker Deamonが起動している

## (b) Build Docker
1. dockerjupyterlabディレクトリに移動
2. Docker compose build command  
    　`>docker compose build`
3. Docker compose run command  
    　`>docker compose up -d`

## (c) Use Jupyter Notebook
- ブラウザで下記URLにアクセスする
    * URL：[http://localhost:8888/](http://localhost:8888/)

## (d) python run 'MaiML to Excel'
1. "Notebook" の　"Python 3(ipykernel)"アイコンをクリック
2. 下記コマンドを入力し、実行してみる  
    　`run /WORK/CODE/maimltoxl.py`
    >"[ERROR]: Arguments is incorrect." のメッセージが出力されたら、実行環境の構築に成功している。

<br><br>

# [How to run 'MaiML to Excel']

## (a) 実行ファイル
　　`/WORK/CODE/maimltoxl.py`

## (b) 入出力データ
    　入力データは、MaiMLファイル、instance要素（<result>、<material>、<condition>）のid属性の値、instance要素が持つ汎用データコンテナの
     key属性の値である。
     instance要素のid属性、instance要素が持つ汎用データのkey属性の指定がない場合は、MaiMLファイル内のinstance要素のコンテンツ全てが対象となる。
     出力データは、エクセルファイルである。instance要素のid属性の値をシート名とした、その要素の汎用データコンテナのコンテンツ一覧が出力される。
     実行時にkey属性の値を指定した場合は、そのkey属性の値を持つ汎用データコンテナのコンテンツのみが出力される。
     プログラム実行時に入力データを指定する方法は２通りあり、jsonファイルを使用する方法とコマンド引数を使用する方法である。入力データは、
     「/WORK/DATA/INPUT/」フォルダにアップデートする。出力データは、「/WORK/DATA/OUTPUT/」フォルダからダウンロード可能である。

## (c) 実行方法と入力データ
    　入力データの指定は、コマンドオプションを使用し区別される。
    　コマンドオプションについては[3-1]、JSONファイルを使用する方法については[3-2]、コマンド引数を使用する方法については[3-3]を参照。

### (c-1) コマンドオプションの説明
|option|Specified data|description|required|
|:--|:--|:--|:--|
|-j|json|Specify when using a json file for input.|"-j" or "-m" is required.|
|-m|maiml|input File Path of MaiML data file|"-j" or "-m" is required.|
|-o|xl|output File Path of excel||
|-si|resultid|select 'instance' element ID||
|-sk|selectkey|select 'key' data of property/content/uncertainty data content ||
|another||||
|-t|test|tests run|Specify when running tests.|


### (c-2) JSONファイルを使用する方法
- コマンド例<br>
　`run /WORK/CODE/maimltoxl.py -j`

- 使用するJSONファイル <br>
  　`/WORK/DATA/INPUT/input.json` <br>

- JSONファイルの記述内容 <br>
    input.jsonの記述定義は表の通り。

    |Param name|description|type|required|
    |:--|:--|:--|:--:|
    |maiml_file_name|File Name of input MaiML data|URI|⭕️|
    |xl_file_name|File Name of output excel data|URI|-|""|
    |resultId|select 'instance' element ID|List of string|-|
    |selectkey|select 'key' of property/content/uncertainty data content |List of string|-|

- input.jsonの記述例 <br>
    ex-1)
    ```
    {
        "maiml_file_name" : "test.maiml",
        "xl_file_name" : "test.xlsx",
        "resultId" : ["resultID-1","resultID-2"],
        "selectkey" : ["exm:SampleValue"]
    }
    ```
    ex-2)
    ```
    {
        "maiml_file_name" : "test.maiml",
        "xl_file_name" : "test.xlsx",
        "selectkey" : ["exm:SampleValue"]
    }
    ```

### (c-3) コマンド引数を使用する方法
- コマンド例<br>
　`run /WORK/CODE/maimltoxl.py -m maimlfilename.maiml -sk exm:SampleValu1 exm:SampleValue2`　

- Description of each arguments: <br>

    |option to use|description|type|required|
    |:--|:--|:--|:--:|
    |-m "filename"|"filename" is File Name of input MaiML data|URI|⭕️|
    |-o "filename"|"filename" is File Name of output excel data|URI|-|
    |-si "list of ID"|'instance' element ID|List of string|-|
    |-sk "list of key"|key data of \<property>/\<content>/\<uncertainty> data content|List of string|-|
　　
<br><br>

# [その他]
- ディレクトリ構成
    ```
    MaiML2Excel/
        -docker-compose.yml
        -Dockerfile
        -CODE/
            -maimltoxl.py
            -namespace.py
            -staticClass.py
            -LOG/
                -log_config.json
                -INFO.log
                -DEBUG.log
        -DATA/
            -INPUT/
                -input.json
                -**inputmaimlfile.maiml
            -OUTPUT/
                -**outputexcelfile.xlsx
            -TMP/
    ``` 
