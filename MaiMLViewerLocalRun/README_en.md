## A visualization application for reference relationships within templates and instances in MaiML data.<!-- omit in toc -->

### 1. Application Overview
This application registers MaiML data in a GraphDB and allows users to query and edit the data list and Petri net diagrams on a Node.js web application. The results of the Petri net diagram edits can be exported and saved back as MaiML data in a file.

### 2. How to Use the Application

#### 2.1. Starting the Application
Accessing the following URL in your browser will display the application’s main screen.

[http://localhost:3000](http://localhost:3000)

#### 2.2. MaiML List Display Screen

Initial screen after startup. The following operations are possible:
* Add to List from MaiML File
`Import`from the dropdown menu &rarr; `Upload File` &rarr; `drop the MaiML file` &rarr; `Execute` 
* Select MaiML to display the Petri net
Press the NID button of the MaiML you want to display → Transition to the Petri net element information screen
* Select MaiML to remove it from the list
Press the DEL button for the MaiML you want to display

#### 2.3. Petri Net Element Information Screen

Screen displaying the Petri net and detailed information of each element stored in the MaiML.

##### 2.3.1. Petri Net Diagram (Left Column)
Simultaneously displays all Petri Net elements belonging to the selected MaiML file, along with elements from related MaiML files (up to two generations before and after) that are associated with those elements.

- Elements are grouped visually based on the MaiML file they belong to.
- Users can select individual Petri Net elements to perform editing operations.
- Double-clicking a MaiML group transitions to the Petri Net element detail view for that MaiML, allowing the editing target to be switched.

##### 2.3.2. Element Information Display (Middle Column) + Insertion Element Information Display

* Register PNML Position Button: </br>
  Saves the coordinates of each node in the Petri Net diagram for the MaiML file selected in the MaiML list Display Screen to the server.
* Node Details: </br>
  Displays the information contained in the selected node.
* Insertion Contents: </br>
  Displays the information of the insertion elements associated with the selected node.

##### 2.3.3. Properties(Right Column)

Display the attribute information of the selected node in the left column.
A hierarchical structure can be formed where each attribute can have multiple sub-attributes.

* `NID` : Individual numbers assigned to each attribute information.
* `Parent NID` : The `NID` indicating the parent that holds that information.

### 3. How to Set Up the Application Environment
Please refer to SETUP_AND_RUN_en.md.
