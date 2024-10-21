# [How to build 'MaiML to Excel']

## (a) Docker install
- Prerequisite: The Docker daemon (such as Docker Desktop or Rancher Desktop) is running.

## (b) Build Docker
1. Navigate to the dockerjupyterlab directory.
2. Docker compose build command  
    　`>docker compose build`
3. Docker compose run command  
    　`>docker compose up -d`

## (c) Use Jupyter Notebook
- Access the following URL in your browser:
    * URL：[http://localhost:8888/](http://localhost:8888/)

## (d) python run 'MaiML to Excel'
1. Click on the 'Notebook' icon for 'Python 3 (ipykernel)'.
2. Enter the following command and execute it: 
    　`run /WORK/CODE/maimltoxl.py`
    >If the message "[ERROR]: Arguments is incorrect." is displayed, it means the environment setup was successful.

<br><br>

# [How to run 'MaiML to Excel']

## (a) Executable file
　　`/WORK/CODE/maimltoxl.py`

## (b) Input and output data
    　The input data consists of the MaiML file, the values of the id attributes of the instance elements 
     (\<result>, \<material>, \<condition>), and the values of the key attributes in the general purpose data container 
     held by the instance elements.
     If the id attribute of the instance elements and the key attributes in the general purpose data are not specified, 
     all contents of the instance elements within the MaiML file will be included.
     The output data will be in an Excel file, with the id attribute values of the instance elements used as sheet names. 
     The contents of the general porpose data containers for those elements will be listed. 
     If a key attribute value is specified at runtime, only the contents of the general purpose data containers 
     with that key attribute value will be output.
     There are two ways to specify input data when executing the program: using a JSON file or command-line arguments.
     The input data should be updated in the /WORK/DATA/INPUT/ folder. The output data can be downloaded 
     from the /WORK/DATA/OUTPUT/ folder.

## (c) Execution Method and Input Data
    　The specification of input data is distinguished using command options.
    　For information on command options, refer to [3-1]. For using a JSON file, see [3-2]. 
    　For using command-line arguments, refer to [3-3].

### (c-1) Description of Command Options
|option|Specified data|description|required|
|:--|:--|:--|:--|
|-j|json|Specify when using a json file for input.|"-j" or "-m" is required.|
|-m|maiml|input File Path of MaiML data file|"-j" or "-m" is required.|
|-o|xl|output File Path of excel||
|-si|resultid|select 'instance' element ID||
|-sk|selectkey|select 'key' data of property/content/uncertainty data content ||
|another||||
|-t|test|tests run|Specify when running tests.|


### (c-2) Method for Using a JSON File
- Example Command <br>
　`run /WORK/CODE/maimltoxl.py -j`

- JSON File to Use <br>
  　`/WORK/DATA/INPUT/input.json` <br>

- Contents of the JSON File <br>
    The description of the input.json file is as follows in the table.

    |Param name|description|type|required|
    |:--|:--|:--|:--:|
    |maiml_file_name|File Name of input MaiML data|URI|⭕️|
    |xl_file_name|File Name of output excel data|URI|-|""|
    |resultId|select 'instance' element ID|List of string|-|
    |selectkey|select 'key' of property/content/uncertainty data content |List of string|-|

- Example of the input.json file <br>
    ex-1)
    ```
    {
        "maiml_file_name" : "test.maiml",
        "xl_file_name" : "test.xlsx",
        "resultId" : ["resultID-1","resultID-2"],
        "selectkey" : ["exm:SampleValue"]
    }
    ```
    ex-2)
    ```
    {
        "maiml_file_name" : "test.maiml",
        "xl_file_name" : "test.xlsx",
        "selectkey" : ["exm:SampleValue"]
    }
    ```

### (c-3) Method for Using Command-Line Arguments
- Example Command <br>
　`run /WORK/CODE/maimltoxl.py -m maimlfilename.maiml -sk exm:SampleValu1 exm:SampleValue2`　

- Description of each arguments: <br>

    |option to use|description|type|required|
    |:--|:--|:--|:--:|
    |-m "filename"|"filename" is File Name of input MaiML data|URI|⭕️|
    |-o "filename"|"filename" is File Name of output excel data|URI|-|
    |-si "list of ID"|'instance' element ID|List of string|-|
    |-sk "list of key"|key data of \<property>/\<content>/\<uncertainty> data content|List of string|-|
　　
<br><br>

# [Others]
- Directory structure
    ```
    MaiML2Excel/
        -docker-compose.yml
        -Dockerfile
        -CODE/
            -maimltoxl.py
            -namespace.py
            -staticClass.py
            -LOG/
                -log_config.json
                -INFO.log
                -DEBUG.log
        -DATA/
            -INPUT/
                -input.json
                -**inputmaimlfile.maiml
            -OUTPUT/
                -**outputexcelfile.xlsx
            -TMP/
    ``` 
