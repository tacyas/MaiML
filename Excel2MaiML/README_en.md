# Excel2MaiML
## A：How to run 'Excel2MaiML'
### [Input and output data]
- INPUT DATA　　※Please refer to the [B: Details] below for conditions and other specifics
  1. A MaiML data file containing the contents of the \<document\> and \<protocol\> elements. <br/>
　　INPUT/maiml/input.maiml  or  INPUT/xxxxx/yyyyyy.maiml 
  1. An Excel data file containing measurement results. <br/>
　　INPUT/excel/input.xlsx  or  INPUT/xxxxx/zzzzzz.xlsx
- OUTPUT DATA
  1. A MaiML file with merged input data. <br/>
　　OUTPUT/output.maiml
 
### [Program Execution Instructions]
- Method 1.
  1. Prepare the Input Files: <br/>
　　Place the MaiML file in the /INPUT/maiml/ directory. <br/>
　　Place the Excel file in the /INPUT/excel/ directory. <br/>
　　Place the External files in the /INPUT/others/ directory. <br/>
  1. Run the Command: <br/>
　　python3 excel2maiml.py <br/>
- Method 2.
  1. Prepare the Input Files: <br/>
　　Place the MaiML file, Excel file and External files in the /INPUT/XXXXX/ directory. <br/>
　　　※'XXXXX' is a placeholder for any name. <br/>
  1. Run the Command: <br/>
　　python3 excel2maiml.py XXXXX <br/>
<br/>


## B:Details
### [Input MaiML Data]
  ・Guarantee of one \<program\> element <br/>

### [Input Excel Data]
　・The sheet name should be the \<method\> element's ID <br/>
　・Row 1 <br/>
　　・Columns 1:　’’ <br/>
　　・Columns 2 and beyond should contain the \<instruction\> element's ID or template's ID <br/>
　・Row 2 <br/>
　　・The column with the template's ID in row 1 <br/>
　　・Row 2 should contain the \<property\> element's key names from below the \<protocol\> element <br/>
　・Row 3 and onward contain the measurement data (multiple rows = multiple measurements) <br/>
　　・Column 1 contains the \<result\> element's ID  <br/>
　　　・The first row contains the \<instruction\> element's ID in the columns <br/>
　　　・Row 3 and onward contain the measurement dates <br/>
　　・The first row contains the template's ID in the columns <br/>
　　　・Row 3 and onward contain the values corresponding to the \<property\> element's keys <br/> 
<p align="center">
  <img src="https://github.com/MaiMLFileHandlingPrograms/Excel2MaiML/blob/main/setting/%E5%85%A5%E5%8A%9B%E3%82%A8%E3%82%AF%E3%82%BB%E3%83%AB%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E8%AA%AC%E6%98%8E.jpeg" />
</p>
<p align="center">The method for writing in Excel</p>

<br/>

### ［Generated MaiML data］
  ・If there are multiple measurement data, create multiple \<results\> elements.  <br/>
  　　（One row of data → One \<results\> element） <br/>
  ・For general data containers, only the \<property\> element is created. <br/>
  ・Copy the template from the input MaiML file as an instance. <br/>
  ・Update the value with Excel data only when the key of the general data container in the template matches the key in the Excel data. <br/>
  　　（If there is no match, the Excel data is ignored.） <br/>
  ・If 'INSERTION' exists in row 2 of the Excel file, create the <insertion> content based on the template's ID instance.  <br/>
  　1. If an external file exists in the INPUT directory: <br/>
  　　The \<insertion\> content: uri: ./+filename, hash value: hash value calculated from the file.  <br/>
  　1. If no external file exists in the INPUT directory: <br/>
　  　The \<insertion\> content: uri: ./+filename, hash value: empty.  <br/>
  ・Create one \<eventLog\> element. <br/>
  ・Create a \<trace\> element if measurement date data exists.  <br/>
　・If there are multiple measurement data, create multiple \<trace\> elements. <br/>
　・If the 'instructionID' exists in the Excel data and date data is available, create one \<event\> element. <br/>
　　　key=lifecycle:transition with the value "complete" only. <br/>

<br/>

## C:Setting Up the Python Execution Environment
### [Python Version]
  ・3.12.x <br/>
### [Python Packages]
  ・requirements.txt <br/>

<br/>

## D:Sample Data
### [MaiML File]
  ・INPUT/maiml/input.maiml <br/>
  　A MaiML file describing a measurement that takes one \<materialTemplate\>(\<material\>) element and one \<conditionTemplate\>(\<condition\>) element as input for a single operation, and outputs one \<resultTemplate\>(\<result\>) element. <br/>
### [Excel File]
  ・INPUT/excel/input.xlsx <br/>
  　An Excel file that records the results used or acquired during the measurement described in input.maiml, along with the input and output file names. <br/>
### [External File]
  ・INPUT/others/Axoneme-56.008.tif <br/>
  ・INPUT/others/test.txt <br/>
  　External files listed in the input.xlsx file, which are recorded as input/output files during the measurement, and included in the new MaiML file using the \<insertion\> element. <br/>
