## Set up Neo4j DB and insert initial data.

#### Functional Structure

The technical elements consist of the following two functionalities:
1. DB server : Neo4j (Docker container)
1. Conversion from MaiML data to Cypher: Python and xml.etree.ElementTree

#### Script Structure

First, start the DB server to ensure it is operational for queries. After that, insert the data into the DB server in the form of Cypher queries converted from the MaiML data. This is the basic workflow.

- Start the DB server  : `docker-run-neo4j.sh`
- Insert all files from the XMAIL folder into the DB. : `setup-XMAIL.sh`
  - Insert the specified MaiML file into the DB. : `app/Script/load-xmail.sh`
  - Convert the specified MaiML file to Cypher. : `app/Script/xml2cypher.py`

※ After starting the DB server, it may take some time for the server to be ready to handle queries. Therefore, the DB insertion script may terminate abnormally immediately afterward. It is advisable to check the DB's operational status before attempting to insert data.

#### Script Execution Steps

```sh
cd kyutech/graph-db
sh ./docker-run-neo4j.sh

# Place the MaiML file to be inserted in the ./XMAIL directory in advance.
# Check the DB server's operational status in advance using a browser or similar tool.
sh ./setup-XMAIL.sh

# If you want to add individual MaiML files later:
sh ./app/Script/load-xmail.sh <MaiML file>
```
