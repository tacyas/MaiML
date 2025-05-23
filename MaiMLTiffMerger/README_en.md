# MaiMLTiffMerger
## Overview
It is a web system that merges MaiML files containing information about measurement processes that output TIFF images with measurement result information.

---


## (a) How to Use the System
1. Refer to　MorphoSmanual.pdf、MaiMLTiffMerger説明.pdf

## (b) Verified Input and Output Data Conditions
### [INPUT DATA]
1. MaiML files with document and protocol layers.
    1. Contains a single \<instruction> element.
    2. Contains a single　\<resultTemplate> element, which is the output of the instruction.
2. TIFF files with metadata.
    1. Contains the datetime when the TIFF image was output.
3. Result data to be added to the input MaiML data.
    1. Data to be added to the contents of the \<material> and \<condition> elements used in the measurement.
    2. Data to be added to the contents of the \<result> element, excluding data that can be extracted from the metadata of the TIFF file.

### [OUTPUT DATA]
1. MaiML data that has been generated by adding the contents of the data layer and eventLog layer (measurement result data) to the input MaiML data (measurement process data).
    1. Contains a \<data> element that carries over the contents of the template elements (\<materialTemplate>, \<conditionTemplate>, \<resultTemplate>) to the instance elements (\<material>, \<condition>, \<result>). 
    2. The reference relationships held in the protocol layer are not automatically carried over to the data layer.
    3. Contains one \<event> element for each \<instruction> element.
    4. Contains the value of the 'DateTime' key from the metadata of the input TIFF file as the completion time in the \<eventLog> element.
    5. Contains the metadata from the input TIFF file (excluding section iv) as a general purpose data container in the \<result> element.
    6. Contains the URI and hash value of the input TIFF file as content in the \<insertion> element of the \<result> element.
2. The file that contains the MaiML data written out from item 1.
3. A ZIP file containing the MaiML file from item 2 and the input TIFF file.

## (c) How to Start the System
1. Start the Docker Compose service.
2. Start the Docker environment with the following command:
   docker compose up -d
3. Access localhost from a web browser.
   http://127.0.0.1:80/
