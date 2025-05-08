# [How to run 'MaiML to Excel']

## (a) Executable file
　　`./maimltoxl.py`

## (b) Input and output data
    　The input data consists of the MaiML file, the required value of the id attribute of the instance(<result>,
     <material> and <condition>) element, and the value of the key attribute in the general purpose data container 
     held by the instance element.
     If the id attribute of the instance element and the key attribute in the general purpose data are not specified, 
     all contents of that element within the MaiML file will be included.
      The output data will be in an Excel file, with the id attribute value of the instance element used as the sheet name. 
     A list of contents from the general purpose data container for that instance element will be output. 
     If a key attribute value is specified at runtime, only the contents of the general purpose data container 
     with that key attribute value will be output.
      There are two ways to specify input data when executing the program: using a JSON file or command-line arguments. 
     The input data should be placed in the ./DATA/INPUT/ folder, and the output data can be checked 
     in the ./DATA/OUTPUT/ folder.

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
|-si|resultid|select 'result' element ID||
|-sk|selectkey|select 'key' data of property/content/uncertainty data content ||
|another:|
|-t|test|tests run|Specify when running tests.|


### (c-2) Method for Using a JSON File
- Example Command<br>
　`python3 ./maimltoxl.py -j`

- JSON File to Use <br>
  　`./DATA/INPUT/input.json` <br>

- Contents of the JSON File <br>
    The description of the input.json file is as follows in the table.

    |Param name|description|type|required|
    |:--|:--|:--|:--:|
    |maiml_file_name|File Name of input MaiML data|URI|⭕️|
    |xl_file_name|File Name of output excel data|URI|-|""|
    |resultId|select 'result' element ID|List of string|-|
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
- Example Command<br>
　`python3 ./maimltoxl.py -m maimlfilename.maiml -sk exm:SampleValu1 exm:SampleValue2`　

- Description of each arguments: <br>

    |option to use|description|type|required|
    |:--|:--|:--|:--:|
    |-m "filename"|"filename" is File Name of input MaiML data|URI|⭕️|
    |-o "filename"|"filename" is File Name of output excel data|URI|-|
    |-si "list of ID"|\<result> element ID|List of string|-|
    |-sk "list of key"|key data of \<property>/\<content>/\<uncertainty> data content|List of string|-|
　　
<br><br>

# [Others]
- Directory structure
    ```
    RUN-python/
        -maimltoxl.py
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
- Python Packages Required for Execution
    ```
    sys
    os
    re
    json
    openpyxl
    lxml
    argparse
    ```


# [Options]
## Command to export template information to an Excel file:
　　`python maimltoxlwithtemplate.py -j`

## Two Excel files will be generated:
- One containing the instance data from the results element
- One containing the template data from the protocol element

## input.jsonの記述例
    ex-1) Specify the file name for instance data with xl_file_name, and for template data with xl_file_name_temp
    ```
    {
     "maiml_file_name" : "input.maiml",
     "xl_file_name" : "instances.xlsx",
     "xl_file_name_temp": "templates.xlsx"
    }
    ```
