# Excel2DocandProtocolofMaiML

# A: Overview
This program takes an Excel file containing planning information for measurement analysis procedures and conditions as input and generates a MaiML data file of type `protocolFileRootType` based on the input data.

# B: Execution Method
## Input and Output Data
### Input Data
1. **Excel File**  
   Refer to `INPUT/excel/ExcelDescription.xlsx`.  
   The input Excel file path depends on the presence of execution arguments.
   - Without execution arguments, the program runs for the single Excel file path specified in `USERS/usersettings.py`.
   - With execution arguments, the program runs for all Excel files in the specified directory.

### Output Data
1. **MaiML file converted from input data**  
   The output MaiML file path depends on the presence of execution arguments.
   - Without execution arguments: `OUTPUT/output.maiml`
   - With execution arguments: The specified directory will contain files where the input filename's extension is changed to `.maiml`.

## Execution Method
### Case 1: Execution Without Arguments
1. **Prepare Input Files**
   - Edit the input file path (`_IN_EXCEL_FILENAME`) and `<maiml>` element attributes (`_MAIML_ATTR`) in `USERS/usersettings.py`.
   - Place the Excel file in the specified input file path.
2. **Run Command**
   ```sh
   python excel2protocolMaiML.py
   ```
   or
   ```sh
   python excel2protocolMaiML2.py
   ```

### Case 2: Execution With a Directory Argument
1. **Prepare Input Files**
   - Edit the `<maiml>` element attributes (`_MAIML_ATTR`) in `USERS/usersettings.py`.
   - Place Excel files in the `/INPUT/XXXXX/` directory.  
     ※ `XXXXX` is an arbitrary name.
2. **Run Command**
   ```sh
   python excel2protocolMaiML2.py XXXXX
   ```

# C: Setting Up the Python Execution Environment
## Python 3.9 or Higher
- Ensure the execution path is set.

## Required Python Packages
- Listed in `requirements.txt`


# D: Running the Sample File
## ① Verify that the input file exists in the `/INPUT/test/` directory.
- exampleX.xlsx

## ② Check that the namespace definitions have been added to `/USERS/usersettings.py`.
   ```sh
      'xmlns:BBBB="http://BBBB.corp/index.jp"'
      'xmlns:BBBBHPLC="http://BBBB.corp/ontology/hplc"'
      'xmlns:CDF="http://BBBB.corp/ontology/cdf"'
   ```

## ③ Execute the command:
   ```sh
      python excel2protocolMaiML2.py test
   ```

## ④ Verify the generated MaiML file in the /INPUT/test/ directory.
- exampleX.maiml
