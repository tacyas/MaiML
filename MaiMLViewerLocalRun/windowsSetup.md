# MaiMLViewerLocalRun
# ローカル環境でdockerを使わずにMaiMLViewerを開発＆実行する環境の構築( windows編 )

## 構成とインストールが必要なもの
#### A: xmail-viewer(アプリケーションサーバー)
    node.js, node modules(package.json,package-lock.jsonで指定), npm
#### B: graph-db(DBサーバー)
    openjdk 11, neo4j 4.4
#### C: DBアクセスの一部を担うpythonスクリプト
    python3, python Packages(neo4j==4.4,cryptography==3.3.2,lxml,signxml)

</br>
</br>

## 環境構築手順
### 準備: 
#### GitHubからコード一式をローカル環境にダウンロードし解凍する
  - 例として、ローカル環境のフォルダを"\\*ANATANODIRECTORY*\MaiMLViewerLocalRun\\"とする
#### コマンドプロンプトの起動方法
  - windowsの検索窓に「cmd」と入力し、コマンドプロンプトを選択する
    
***
### A: xmail-viewer(アプリケーションサーバー)の構築
  #### A-1 nodeをインストール
  - 公式サイト(https://nodejs.org/) から、Windowsインストーラ形式(.msi)をダウンロード＆インストールする
  - nodeとnpmがインストールされる
  - コマンドプロンプト画面を開き、下記コマンドを実行し、バージョンが表示されればインストール成功
    ```sh
    > node --version
      v22.14.0
    > npm --version
      10.9.2
    ```
 
  #### A-2 必要に応じて（企業内ネットワーク等でプロキシサーバ経由でインターネットにアクセスしている場合等）、プロキシの設定を行う
  - コマンドプロンプト画面を開き、下記コマンドを実行
    ```sh
    > cd \ANATANODIRECTORY\MaiMLViewerLocalRun\xmail-viewer\
    > npm config set proxy <プロキシサーバー>:<ポート番号>
    > npm config set https-proxy <プロキシサーバー>:<ポート番号>
    	例）
    	npm config set proxy http://proxy.example.com:8080
    	npm config set https-proxy http://proxy.example.com:8080
    ```
  #### A-3 関連モジュールをインストール
  - "\\*ANATANODIRECTORY*\\MaiMLViewerLocalRun\\xmail-viewer\\"ディレクトリに、package.json、
    package-lock.jsonの２つのファイルが存在する
  - コマンドプロンプト画面を開き、下記コマンドを実行し、package.json、package-lock.jsonで指定したモジュールをインストールする
    ```sh
    > cd \ANATANODIRECTORY\MaiMLViewerLocalRun\xmail-viewer\
    > npm install
    ```
    　   →"\\*ANATANODIRECTORY*\\MaiMLViewerLocalRun\\xmail-viewer\\node_modules\\"ディレクトリが作成される
  #### A-4 nodeを起動
  - コマンドプロンプト画面を開き、下記コマンドを実行し、nodeでwwwファイルを起動
    ```sh
    > cd \ANATANODIRECTORY\MaiMLViewerLocalRun\xmail-viewer\
    > node bin/www
    ```
  #### A-5 webブラウザで "http://localhost:3000/" にアクセス
  - 接続できていればエラーになっていてもOK
  #### A-6 nodeを停止
  - コマンドプロンプト画面を表示し、キーボードで下記を押下
    ```sh
      ctl+c
    ```
***
### B: graph-db(DBサーバー) の構築
下記をそれぞれ自分の環境に合わせてインストール、実行する
  #### B-1 JDK 11をインストール
  - サイト( https://learn.microsoft.com/ja-jp/java/openjdk/download#openjdk-11 )から、Windowsインストーラ形式(.msi)をダウンロードする
  - セットアップウィザードの「カスタムセットアップ」の画面で「Set JAVA_HOME valiable」が「✕ インストールしない」になっている所を「すべてインストール」に変更してインストールする

  #### B-2 neo4j 4.4をインストール
  - 公式サイト(https://neo4j.com/deployment-center/#enterprise) からneo4j 4.4-community版をダウンロードする
  - ダウンロードしたneo4j-community-4.4.xx-windows.zipを解凍し、任意のディレクトリ（例えば、\\*ANATANODIRECTORY*\\neo4j\\）におく

  #### B-3 neo4jを起動
  - コマンドプロンプト画面を開き、下記コマンドを実行する
    ```sh
    > \ANATANODIRECTORY\neo4j\bin\neo4j console　(もしくは　> \ANATANODIRECTORY\neo4j\bin\neo4j start)
	   Starting Neo4j.
	   Started neo4j (pid:14213). It is available at http://localhost:7474
    ```
  #### B-4　webブラウザで "http://localhost:7474" にアクセス
  - start画面が出たらOK
  #### B-5 neo4jを停止
  - コマンドプロンプト画面を表示し、キーボードで下記を押下
    ```sh
      ctl+c
    ```
 
***
### C: DBにアクセスする一部を担うpythonスクリプトの実行環境
  #### C-1 自分の環境に合わせてpython(3以上)をインストール
  - 「Add Python to PATH」にチェックを入れてインストール
  #### C-2 下記のパッケージをインストール
  - インストールするパッケージ一覧 <br/>
    neo4j==4.4、cryptography==3.3.2、lxml、signxml
  - コマンドプロンプト画面を開き、下記コマンドを実行する
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
- コマンドプロンプト画面を開き、下記コマンドを実行する
  ```sh
  > set MAIML_TMP_DIR=\ANATANODIRECTORY\MaiMLViewerLocalRun\xmail-viewer\models\tmp
  ````
### 2: neo4jの設定&起動
- neo4j.confの設定を変更する
  - neo4j.confの場所： <br/>
    \\*ANATANODIRECTORY*\\neo4j\\conf\\neo4j.conf
  - 修正内容：
    ```
     dbms.security.auth_enabled=false
     dbms.connector.bolt.enabled=true
     dbms.connector.http.enabled=true
    ```
    もし、下記のように行の先頭に"#"が存在している場合は、"#"を消す
    ```
     #dbms.security.auth_enabled=false
    ```
    
- 修正後neo4jを起動
  - コマンドプロンプト画面を開き、下記コマンドを実行する 
    ```sh
    > \ANATANODIRECTORY\neo4j\bin\neo4j console　(もしくは　> \ANATANODIRECTORY\neo4j\bin\neo4j start)
    ```
### 3: nodeの起動
- 新たなコマンドプロンプト画面を開き、下記コマンドを実行する
  ```sh
  > cd \ANATANODIRECTORY\MaiMLViewerLocalRun\xmail-viewer\
  > node bin\www
  ```
  　　→"\\*ANATANODIRECTORY*\\MaiMLViewerLocalRun\\xmail-viewer\\logs"が作成される
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
#### 2-2. 環境変数（MAIML_TMP_DIR）を設定

<br/>

### 3. アプリケーション実行方法
#### 3-1. コマンドプロンプト画面で、neo4jを起動
#### 3-2. 新たなコマンドプロンプト画面を開き、nodeで \\MaiMLViewerLocalRun\\xmail-viewer\\bin\\www を起動
#### 3-3. webブラウザで "http://localhost:3000/" にアクセス

</br>
</br>

## 実行PATHが通っていない時の対処法
### nodeとnpmの実行ファイル
  コマンドプロンプト画面から下記のコマンドを実行し、PATHを通す <br/>
  1. nodeのPATH（インストールフォルダが"C:\\Program Files\\nodejs\\"の場合）を通す
  ```sh
    > set path=%path%;C:\Program Files\nodejs\
  ```
  2. npmのPATH（インストールフォルダが"C:\\Users\\anata\\AppData\\Roaming\\npm"の場合）を通す
  ```sh
    > set path=%path%;C:\Users\anata\AppData\Roaming\npm
  ```
### openjdk 11
  コマンドプロンプト画面から下記のコマンドを実行し、PATHを通す <br/>
  1. 環境変数「JAVA_HOME」を追加（インストールフォルダが"C:\\Program Files\\openjdk@11\\libexec\\openjdk.jdk\\Contents\\Home\\"の場合）する
  ```sh
    > set JAVA_HOME=C:\Program Files\openjdk@11\libexec\openjdk.jdk\Contents\Home\
  ```
  2. 実行PATHを追加する
  ```sh
    > set path=%JAVA_HOME%\bin;%path%
  ```
### neo4j（PATHを通し、実行時のコマンドを簡略化する場合）
  コマンドプロンプト画面から下記のコマンドを実行し、PATHを通す <br/>
  1. 環境変数「NEO4J_HOME」を追加（インストールフォルダが"\\ANATANODIRECTORY\\neo4j"の場合）する
  ```sh
    > set NEO4J_HOME=\ANATANODIRECTORY\neo4j
  ```
  2. 実行PATHを追加する
  ```sh
    > set path=%path%;%NEO4J_HOME%\bin
  ```
  3. PATHを通すと、neo4jの実行コマンドは下記となる
  ```sh
    > neo4j console　(もしくは　> neo4j start)
  ```
