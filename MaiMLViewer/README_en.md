## A visualization application for reference relationships within templates and instances in MaiML data.<!-- omit in toc -->

### 1. Application Overview
This application registers MaiML data in a GraphDB and allows users to query and edit the data list and Petri net diagrams on a Node.js web application. The results of the Petri net diagram edits can be exported and saved back as MaiML data in a file.

### 2. Repository Structure
Refer to the individual README_en.md files for usage instructions for each component.

|Repository|Technology|
|:-----|:-----|
|graph-db/|Neo4j, Cypher Query Language|
|xmail-viewer/|NodeJS|
|Documents/|Markdown|
|MaiML/|XML|
|docker-compose.yml|Docker|
|README.*| - |


### 3. Server Startup Procedure

This application is composed of multiple Docker containers.

|Repository|containers|Features|
|:--|:--|:--|
|xmail-viewer|xmail_viewer|Web Application Core|
|graph-db|graph_db|Graph DB using Neo4j|
|nginx|nginx|Web Server using Nginx|


All of these containers are managed collectively by Docker Compose, allowing for start/stop operations using commands such as the following:

- Create and Start Containers  
`docker-compose up -d`
- Stop Containers 
`docker-compose stop`
- Start Stopped Containers 
`docker-compose start`
- Restart Containers  
`docker-compose restart`
- Stop Containers and Remove Images 
`docker-compose down --rmi all`
- Delete All Data
`docker-compose down --rmi all --volumes`


### 4. How to Use the Application

#### 4.1. Starting the Application
Accessing the following URL in your browser will display the application’s main screen.

`http://＜Hostname or IP Address＞:3101`

※In the case of a Docker machine in a local environment

[http://localhost:3101](http://localhost:3101)

#### 4.2. MaiML List Display Screen

Initial screen after startup. The following operations are possible:
* Add to List from MaiML File
`Import`from the dropdown menu &rarr; `Upload File` &rarr; `drop the MaiML file` &rarr; `Execute` 
* Select MaiML to display the Petri net
Press the NID button of the MaiML you want to display → Transition to the Petri net element information screen
* Select MaiML to remove it from the list
Press the DEL button for the MaiML you want to display

#### 4.3. Petri Net Element Information Screen

Screen displaying the Petri net and detailed information of each element stored in the MaiML.

##### 4.3.1. Petri Net Diagram (Left Column)
Simultaneously displays all elements of the Petri net belonging to the selected MaiML, as well as elements from other MaiML files that are associated with those elements.

* Group classification display based on the MaiML to which each element belongs.
* The labels for the MaiML groups indicate the corresponding MaiML NID.
* Select and edit each element of the Petri net.
* Double-clicking a MaiML group will transition you to the Petri net element information screen for that MaiML.
(You can switch the MaiML being edited.)

##### 4.3.2. Element Information Display (Middle Column) + Insertion Element Information Display

* Register PNML Position Button: Saves the coordinates of each node in the Petri net diagram to the server.
* Node Details: Displays the information contained in the selected node.
* Insertion Contents: Displays the information of the insertion elements associated with the selected node.

##### 4.3.3. Properties(Right Column)

Display the attribute information of the selected node in the left column.
A hierarchical structure can be formed where each attribute can have multiple sub-attributes.

* `NID` : Individual numbers assigned to each attribute information.
* `Parent NID` : The `NID` indicating the parent that holds that information.
