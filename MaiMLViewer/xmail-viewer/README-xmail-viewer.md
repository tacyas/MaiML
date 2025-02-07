﻿## XMAILデータ照会ツール
### xmail-viewer
 
***
### Development Prerequisites
当アプリケーションの開発に必要な前提条件を以下に示す。
各ツールの設定ファイルは当リポジトリから取得してください。
#### 構成管理
https://desktop.github.com/
	`github`

※ 当プロジェクト一式をクローンし、開発を行ってください。
#### コードエディタ
https://code.visualstudio.com/
	`Visual Studio Code (VS Code)`
#### コードフォーマッタ
https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode
	`Prettier`
	※ VSCode上でソースファイルを開き、[Shift + Alt + f] でコードフォーマット可能。 
	
#### 静的コード解析
https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint
	`ES Lint`
#### コメント
https://marketplace.visualstudio.com/items?itemName=joelday.docthis
	`jsDoc3 + Document This (VS Code plugin)`
*** 
### アプリケーション構成
|#|Category|Technology|
|:-----:|:-----|:-----|
|1|Application Server|express|
|2|Technical Stacks|NodeJS|
|3|UI/UX|Bootstrap 4|
|4|View|hbs|
|5|Graph Visualization|~~Alchemy.js~~<br> Cytoscape.js|
|6|Data grid|DataTables.js|
|7|Container|Docker|
|8|Orchestration|docker-compose|

### アプリケーション概要
GraphDBに登録されているMaiMLデータを一覧で照会し、さらに一覧上で選択されたMaiMLに対するペトリネット図を生成する。

### アプリケーション起動方法
＜開発モード＞
１）前提条件として開発環境にnodejs及び、npmがインストールされていること
　　　　`\xmail-viewer> node -v`
　　　　`v10.5.0`
　　　　`\xmail-viewer> npm -v`
　　　　`6.1.0`

２）当リポジトリ(xmail-viewer)をクローン
３）package.jsonが存在するディレクトリにて`npm install`を実行

	※ クライアントセキュリティソフトウェアが有効になっている場合、npm installが失敗する場合があるので、その場合は一旦セキュリティソフトウェアを停止して実行し、後で必ずセキュリティソフトウェアを有効にしてください。
　　
４）同ディレクトリにおいて下記コマンドを実行
  　　　　`node ./bin/www`
５）Chromeブラウザから下記URLへアクセス
　　　　`http://localhost:3000`
６）MaiMLデータ一覧照会画面が表示される

＜プロダクションモード＞
　　　　`TBD`

### ディレクトリ構成
	./xmail-viewer
	    ├─bin
	    ├─common
	    ├─logs
	    ├─models
	    │   ├─python
	    │   └─tmp
	    ├─routes
	    └─views
	        ├─css
	        │  └─vendor
	        ├─img
	        ├─js
	        │  └─vendor-util
	        └─partials
	    ├─app.js
	    ├─package.json

## Docker
### Prerequisites
githubからソースをクローン
git clone [https://mntUsk@github.com/Micronet-Techno/kyutech.git](https://mntUsk@github.com/Micronet-Techno/kyutech.git)

	cd ~
	cd kyutech
	git clone https://mntUsk@github.com/Micronet-Techno/kyutech.git
	(password)
	cd kyutech
	sudo cp -r xmail-viewer/ /usr/kyutech/
	cd /user/kyutech

### pre-process
docker hubからnode image を取得（10.5.0で開発だが、とりあえずlatest）

	docker pull node
	docker images

#### Dockerfile

	cd /use/kyutech
	vi Dockerfile

		FROM node
		MAINTAINER mnt

		ADD xmail-viewer/bin /opt/app/xmail-viewer/bin
		ADD xmail-viewer/models /opt/app/xmail-viewer/models
		ADD xmail-viewer/routes /opt/app/xmail-viewer/routes
		ADD xmail-viewer/views /opt/app/xmail-viewer/views
		ADD xmail-viewer/app.js /opt/app/xmail-viewer/app.js
		ADD xmail-viewer/package.json /opt/app/xmail-viewer/package.json

		ENV PORT 3000
		ENV GRAPH_DB_IP 52.11.150.230

		WORKDIR /opt/app/xmail-viewer
		RUN npm i
		EXPOSE 3000

		CMD [ "node", "/opt/app/xmail-viewer/bin/www" ]

##### ※「ENV GRAPH_USER 」、「GRAPH_PWD」が環境変数に存在する場合はその認証情報を使用する。

#### Build container
	docker build -t xmail-viewer:0.0.4 .
	docker images

#### Docker run
	docker run -d --restart=always -v /usr/kyutech/logs:/opt/app/xmail-viewer/logs -p 3101:3000 xmail-viewer:0.0.4
	docker ps -a


	docker start (container id)
	
#### 	Validate application

[http://52.11.150.230:3101](http://52.11.150.230:3101)

#### Docker command
	docker images
	docker network ls
	docker ps -a
	docker stop (container id)

	docker rm $(sudo docker ps -qa)
	docker rmi $(sudo docker images -q)

	sudo docker network create kyutech

	ps -ef | grep node
	netstat -anp | grep LISTEN

### 機能一覧

|#|Feature|概要|
|:-----:|:-----|:-----|
|1|MaiMLデータ一覧照会|Graph DBに格納されているデータを一覧表示します。|
|2|MaiMLペトリネット図生成|Cytoscape.jsを使用し、MaiMLデータからペトリネット図を生成します。|
|3|MaiML構成ノード情報照会|ペトリネット図を構成するノートの情報を照会します。|
|4|MaiMLファイルアップロード(1件)|ローカルPC上のMaiMLファイルを一覧表示とペトリネット図データとしてGraph DBへ登録します。NIDは自動で採番され、同じファイルを複数回登録することができる。|
|5|MaiMLデータ削除(1件)|一覧上で選択された行（キー：NID）を対象にGraphDBに登録されているMaiMLデータを削除する。|
||||

#### ログ

|#|種類|概要|パス|
|:-----:|:-----|:-----|:-----|
|1|アクセスログ|expressのアクセスログを記録する|/logs/access.log|
|2|アプリケーションログ|アプリケーションログ(DEBUG/INFO/ERROR)|/logs/app.log|
||||

#### Development Memo
登録したMaiMLファイルをNID指定で登録されているデータをすべて削除

	match p=(a:XMAIL)
	-[:XML_Root]->(r)
	-[:XML_Child|XML_Data*1..]->(n)
	where id(a)=30862
	detach delete p;

ペトリネット図を直接表示

	http://localhost:3000/petronet/view?id=0
	http://localhost:3000/petronet/view?id=30862
	など

> Written with [StackEdit](https://stackedit.io/).
