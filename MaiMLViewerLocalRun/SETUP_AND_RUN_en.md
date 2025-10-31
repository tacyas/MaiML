# MaiMLViewerLocalRun
# Building a Local Environment to Develop and Run MaiMLViewer Without Docker

## Components and Required Installations
#### A: xmail-viewer (Application Server)
    node.js, node modules (specified in package.json and package-lock.json)
#### B: graph-db (Database Server)
    openjdk 11, neo4j 4.4
#### C: Python scripts handling part of DB access
    python3, Python packages (neo4j==4.4, cryptography==3.3.2, lxml, signxml)

</br></br>

## Environment Setup Steps
### Preparation: Download all code from GitHub to your local environment
  - For example, use the directory "/*YOUR_DIRECTORY*/MaiMLViewerLocalRun/" as your local working directory.
***
### A: xmail-viewer (Application Server)
  #### A-1 Install Node.js
  - Download and install from the official site (https://nodejs.org/)
  - Both Node.js and npm will be installed.
  - If the executables for node and npm are not in PATH, add them manually.
  #### A-2 Configure proxy if necessary (e.g., corporate network environments)
  - Execute the following commands:
    ```sh
    > cd /YOUR_DIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
    > npm config set proxy <proxy_server>:<port_number>
    ```
  #### A-3 Install dependencies
  - Ensure both package.json and package-lock.json exist in "/*YOUR_DIRECTORY*/MaiMLViewerLocalRun/xmail-viewer/"
  - Execute the following commands to install the required modules:
    ```sh
    > cd /YOUR_DIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
    > npm install
    ```
       → The directory "/*YOUR_DIRECTORY*/MaiMLViewerLocalRun/xmail-viewer/node_modules/" will be created.
  #### A-4 Start Node.js
  - Execute the following command to launch the www file:
    ```sh
    > cd /YOUR_DIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
    > node ./bin/www
    ```
  #### A-5 Open a web browser and access "http://localhost:3000/"
  - Even if an error appears, the connection itself is fine.
  #### A-6 Stop Node.js
  - Press the following keys on your keyboard:
    ```sh
      ctrl+c
    ```
***
### B: graph-db (Database Server)
Install and configure the following according to your environment.
  #### B-1 Install JDK 11
  - Install openjdk 11.x.xx (https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-11)
  - Add two environment variables:
    ```
    JAVA_HOME=path_to_your_installation (e.g., /YOUR_DIRECTORY/openjdk@11/libexec/openjdk.jdk/Contents/Home)
    PATH=$JAVA_HOME/bin:$PATH
    ```
  #### B-2 Install neo4j 4.4
  - Download neo4j 4.4-community edition from the official site (https://neo4j.com/deployment-center/#enterprise)
  - Extract the downloaded neo4j-community-4.4.xx-unix.tar.gz and place it in a desired directory (e.g., /*YOUR_DIRECTORY*/neo4j/)
  #### B-3 Start neo4j
  - Execute the following commands:
    ```sh
    > cd /YOUR_DIRECTORY/neo4j/bin/
    > ./neo4j console   (or > ./neo4j start)
       Starting Neo4j.
       Started neo4j (pid:14213). It is available at http://localhost:7474
    ```
  #### B-4 Open a web browser and access "http://localhost:7474"
  - If the start screen appears, it's working correctly.
  #### B-5 Stop neo4j
  - Execute the following commands:
    ```sh
    > cd /YOUR_DIRECTORY/neo4j/bin/
    > ./neo4j stop
    ```
  #### B-6 Set environment variables
  - Add the following environment variables:
    ```
    NEO4J_HOME=/YOUR_DIRECTORY/neo4j
    PATH=$PATH:$NEO4J_HOME/bin
    ```
***
### C: Python Environment for DB Access Scripts
  #### C-1 Install Python (version 3 or higher) for your environment
  - Make sure to check "Add Python to PATH" during installation.
  #### C-2 Install required packages
  - Install the following Python packages: neo4j==4.4, cryptography==3.3.2, lxml, signxml
  - Example commands:
    ```sh
    > pip install neo4j==4.4
    > pip install cryptography==3.3.2
    > pip install lxml
    > pip install signxml
    ```
</br></br>

## Running the MaiMLViewer Application
### 1: Set required environment variables
```
MAIML_TMP_DIR=/YOUR_DIRECTORY/MaiMLViewerLocalRun/xmail-viewer/models/tmp
```
### 2: Configure and start neo4j
- Modify the neo4j.conf file  
  - File location:  
    /*YOUR_DIRECTORY*/neo4j/conf/neo4j.conf  
  - Edit as follows:
    ```
     dbms.security.auth_enabled=false
     dbms.connector.bolt.enabled=true
     dbms.connector.http.enabled=true
    ```
- Restart neo4j after editing:
  ```sh
  > neo4j restart
  ```
### 3: Start Node.js
- Execute the following commands:
  ```sh
  > cd /YOUR_DIRECTORY/MaiMLViewerLocalRun/xmail-viewer/
  > node /bin/www
  ```
  　→ The directory "/*YOUR_DIRECTORY*/MaiMLViewerLocalRun/xmail-viewer/logs" will be created.
### 4: Access the application in a web browser
- URL: "http://localhost:3000/"
- The MaiMLViewer list page should appear.

</br></br><br/>

## Summary
### 1. Required Installations
#### 1-1. node, npm, and node modules
#### 1-2. python3 and Python packages
#### 1-3. openjdk 11 and neo4j 4.4
<br/>

### 2. Required Configurations
#### 2-1. Modify neo4j.conf
#### 2-2. Set environment variables
```
 JAVA_HOME, NEO4J_HOME, MAIML_TMP_DIR
```
#### 2-3. Add executables to PATH
```
 node, npm, java, neo4j, python
```
<br/>

### 3. Application Execution Steps
#### 3-1. Start neo4j
#### 3-2. Run /MaiMLViewerLocalRun/xmail-viewer/bin/www with Node.js
#### 3-3. Access "http://localhost:3000/" via web browser
