# MaiMLViewerLocalRun
# ローカル環境でdockerを使わずにMaiMLViewerを開発＆実行する環境の構築

## 構成とインストールが必要なもの
#### A: xmail-viewer(アプリケーションサーバー)
    node.js, node modules(package.json,package-lock.jsonで指定)
#### B: graph-db(DBサーバー)
    openjdk 11, neo4j 4.4
#### C: DBアクセスの一部を担うpythonスクリプト
    python3, python Packages(neo4j==4.4,cryptography==3.3.2,lxml,signxml)

</br>
</br>

## 環境構築手順
### 準備: GitHubからコード一式をローカル環境にダウンロード
  - 例として、ローカル環境のディレクトリを"/*ANATANODIRECTORY*/MaiMLViewerLocalRun/"とする
***
### A: xmail-viewer(アプリケーションサーバー)
  #### A-1 nodeをインストール
  - 公式サイト(https://nodejs.org/) からダウンロードしてインストールする
  - nodeとnpmがインストールされる
  - nodeとnpmの実行ファイルにPATHが通っていなければそれぞれPATHを通す
  #### A-2 必要に応じて（企業内ネットワーク等でプロキシサーバ経由でインターネットにアクセスしている場合等）、プロキシの設定を行う
  - 下記コマンドを実行
    ```sh
    > cd /ANATANODIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
    > npm config set proxy <プロキシサーバー>:<ポート番号>
    ```
  #### A-3 関連モジュールをインストール
  - "/*ANATANODIRECTORY*/MaiMLViewerLocalRun/xmail-viewer/"ディレクトリに、package.json、
    package-lock.jsonの２つのファイルが存在する
  - 下記コマンドを実行し、package.json、package-lock.jsonで指定したモジュールをインストールする
    ```sh
    > cd /ANATANODIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
    > npm install
    ```
    　   →"/*ANATANODIRECTORY*/MaiMLViewerLocalRun/xmail-viewer/node_modules/"ディレクトリが作成される
  #### A-4 nodeを起動
  - 下記コマンドを実行し、nodeでwwwファイルを起動
    ```sh
    > cd /ANATANODIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
    > node ./bin/www
    ```
  #### A-5 webブラウザで "http://localhost:3000/" にアクセス
  - 接続できていればエラーになっていてもOK
  #### A-6 nodeを停止
  - キーボードで下記を押下
    ```sh
      ctl+c
    ```
***
### B: graph-db(DBサーバー) 
下記をそれぞれ自分の環境に合わせてインストール、実行する
  #### B-1 JDK 11をインストール
  - それぞれの環境に合わせて、openjdk11.x.xxをインストール( https://learn.microsoft.com/ja-jp/java/openjdk/download#openjdk-11 )し、２つの環境変数を追加する
    ```
    JAVA_HOME=インストールしたディレクトリ（例：/ANATANODIRECTORY/openjdk@11/libexec/openjdk.jdk/Contents/Home）
    PATH=$JAVA_HOME/bin:$PATH
    ```
  #### B-2 neo4j 4.4をインストール
  - 公式サイト(https://neo4j.com/deployment-center/#enterprise) からneo4j 4.4-community版をダウンロードする
  - ダウンロードしたneo4j-community-4.4.xx-unix.tar.gzを解凍し、
    任意のディレクトリ（例えば、/*ANATANODIRECTORY*/neo4j/）におく
  #### B-3 neo4jを起動
  - 下記コマンドを実行する
    ```sh
    > cd /ANATANODIRECTORY/neo4j/bin/
    > ./neo4j console　(もしくは　> ./neo4j start)
	   Starting Neo4j.
	   Started neo4j (pid:14213). It is available at http://localhost:7474
    ```
  #### B-4　webブラウザで "http://localhost:7474" にアクセス
  - start画面が出たらOK
  #### B-5 neo4jを停止
  - 下記コマンドを実行する
    ```sh
    > cd /ANATANODIRECTORY/neo4j/bin/
    > ./neo4j stop
    ```
  #### B-6 環境変数を設定
  - 環境変数を追加する
    ```
    NEO4J_HOME=/ANATANODIRECTORY/neo4j
    PATH=$PATH:$NEO4J_HOME/bin
    ```
 
***
### C: DBにアクセスする一部を担うpythonスクリプトの実行環境
  #### C-1 自分の環境に合わせてpython(3以上)をインストール
  - 「Add Python to PATH」にチェックを入れてインストール
  #### C-2 下記のパッケージをインストール
  - neo4j==4.4、cryptography==3.3.2、lxml、signxml
  - コマンド例
    ```sh
    > pip install neo4j==4.4
    > pip install  cryptography==3.3.2
    > pip install lxml
    > pip install signxml
    ```
</br>
</br>

## MaiMLViewer アプリケーションを実行する
### 1: アプリケーション実行時に必要な環境変数を設定する
```
MAIML_TMP_DIR=/ANATANODIRECTORY/MaiMLViewerLocalRun/xmail-viewer/models/tmp
````
### 2: neo4jの設定&起動
- neo4j.confの設定を変更する
  - neo4j.confの場所： <br/>
    /*ANATANODIRECTORY*/neo4j/conf/neo4j.conf
  - 修正内容：
    ```
     dbms.security.auth_enabled=false
     dbms.connector.bolt.enabled=true
     dbms.connector.http.enabled=true
    ```
- 修正後neo4jを再起動
  ```sh
  > neo4j restart
  ```
### 3: nodeの起動
- 下記コマンドを実行する
  ```sh
  > cd /ANATANODIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
  > node /bin/www
  ```
  　　→"/*ANATANODIRECTORY*/MaiMLViewerLocalRun/xmail-viewer/logs"が作成される
### 4: webブラウザでアプリケーションにアクセス
- URL："http://localhost:3000/" にアクセスする
- MaiMLViewerのリスト画面が表示される

</br>
</br>
<br/>

## まとめ
### 1. インストールするもの
#### 1-1. node, npm, nodeのモジュール
#### 1-2. python3, pythonのパッケージ
#### 1-3. openjdk 11, neo4j4.4
<br/>

### 2. 設定するもの
#### 2-1. neo4j.confを修正
#### 2-2. 環境変数を設定
```
 JAVA_HOME, NEO4J_HOME, MAIML_TMP_DIR
```
#### 2-3. 実行ファイルにpathを通す
```
 node, npm, java, neo4j, python
```
<br/>

### 3. アプリケーション実行方法
#### 3-1. neo4jを起動
#### 3-2. nodeで /MaiMLViewerLocalRun/xmail-viewer/bin/www を実行
#### 3-3. webブラウザで "http://localhost:3000/" にアクセス



