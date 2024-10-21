## MaiML Data Query Tool
### xmail-viewer
 
***
### Development Prerequisites
The prerequisites for developing this application are listed below. 
Please obtain the configuration files for each tool from this repository.

#### Code Editor
https://code.visualstudio.com/ </br>
	`Visual Studio Code (VS Code)`
 
#### Code Formatter
https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode </br>
	`Prettier` </br>
	※ Open the source file in VSCode and format the code using [Shift + Alt + F]. 
	
#### Static Code Analysis
https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint </br>
	`ES Lint`

#### Comments
https://marketplace.visualstudio.com/items?itemName=joelday.docthis </br>
	`jsDoc3 + Document This (VS Code plugin)`
*** 

### Application Structure
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

### Application Overview
Query the MaiML data registered in GraphDB in a list format, and generate a Petri net diagram for the selected MaiML from the list."

### How to Start the Application
＜Development Mode＞
  1) As a prerequisite, Node.js and npm must be installed in the development environment. </br>
　　　　`\xmail-viewer> node -v` </br>
　　　　`v10.5.0` </br>
　　　　`\xmail-viewer> npm -v` </br>
　　　　`6.1.0` </br>
    
  2) Clone this repository (xmail-viewer).

  3) Run `npm install` in the directory where package.json is located.

	※ If client security software is enabled, npm install may fail.
     In that case, temporarily disable the security software while running the command, and be sure to re-enable it afterward.
     
  4) In the same directory, execute the following command: </br>
  　　　　`node ./bin/www`
  
  5) Access the following URL from the Chrome browser: </br>
　　　　`http://localhost:3000`
  
  6) The XMAIL data list query screen will be displayed. </br></br>

＜Production Mode＞</br>
　　　　`TBD`

### Directory Structure
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
Clone the source from GitHub. </br>
git clone [https://github.com/tacyas/MaiML.git](https://github.com/tacyas/MaiML.git) </br>

	cd ~
	cd kyutech
	git clone https://mntUsk@github.com/Micronet-Techno/kyutech.git
	(password)
	cd kyutech
	sudo cp -r xmail-viewer/ /usr/kyutech/
	cd /user/kyutech

### pre-process
Obtain the Node image from Docker Hub (development is done with version 10.5.0, but for now, use latest).

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

##### ※If the environment variables [GRAPH_USER] and [GRAPH_PWD] exist, their authentication information will be used.

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

### Feature List

|#|Feature|Overview|
|:-----:|:-----|:-----|
|1|Query MaiML Data List|Displays a list of data stored in the Graph DB.|
|2|Generate MaiML Petri Net Diagram|Using Alchemy.js, generate a Petri net diagram from the XMAIL data.|
|3|Query MaiML Structure Node Information|Queries the information of the nodes that make up the Petri net diagram.|
|4|Upload MaiML File (1 item)|The MaiML file on your local PC will be registered in the Graph DB as a list and Petri net diagram data. NIDs are automatically assigned, allowing the same file to be registered multiple times.|
|5|Delete MaiML File (1 item)|Delete the MaiML data registered in GraphDB for the selected row in the list (key: NID).|
||||

#### Log

|#|Type | Overview | Path |
|:-----:|:-----|:-----|:-----|
|1|Access Log|Record access logs for Express.|/logs/access.log|
|2|Application Log|Application Log (DEBUG/INFO/ERROR)|/logs/app.log|
||||

#### Development Memo
Delete all data registered with the specified NID for the uploaded MaiML file.

	match p=(a:XMAIL)
	-[:XML_Root]->(r)
	-[:XML_Child|XML_Data*1..]->(n)
	where id(a)=30862
	detach delete p;

Directly display the Petri net diagram.

	http://localhost:3000/petronet/view?id=0
	http://localhost:3000/petronet/view?id=30862
	etc.
