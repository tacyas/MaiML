# Excel2DocandProtocolofMaiML

# A: Overview
This program takes an Excel file containing planning information for measurement analysis procedures and conditions as input and generates a MaiML data file of type `protocolFileRootType` based on the input data.

# B: Execution Method
## Input and Output Data
### Input Data
#### 1. **Excel File**  
   Refer to `INPUT/excel/ExcelDescription.xlsx`.  
   The input Excel file path depends on the presence of execution arguments.
   | Execution Condition | The input Excel file path |
   |---------|-------|
   | **No arguments** | The program runs for the single Excel file path specified in `USERS/usersettings.py` |
   | **With arguments** | The program runs for all Excel files in the specified directory |

### Output Data
   Outputs a MaiML file that converts input excel data into the MaiML data format.
   The output content for elements that are not mandatory in Excel and are not automatically set by the program varies　depending on the executed Python script.
#### 1. Output Specifications for Each Script
| Script | Handling of Unfilled Items in Excel |
|-------------|----------------|
| `excel2protocolMaiML.py` | Outputs only the tags (with no values) |
| `excel2protocolMaiML2.py` | Does not include the tags themselves|

#### 2. Output File Save Location
The location where the output MaiML file is saved is determined by the presence or absence of execution arguments.
| Execution Condition | Output Directory |
|---------|-------|
| **No arguments** | Saved as OUTPUT/output.maiml |
| **With arguments** | Saved in the specified directory with the input file name changed to .maiml extension |

##### **Example**
- Running 'python excel2protocolMaiML.py'
  → Saved as `OUTPUT/output.maiml`  

- Running `python excel2protocolMaiML2.py XXXXX`
  → Saved as `/INPUT/XXXXX/入力ファイル名.maiml`

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
### ① Verify that the input file exists in the `/INPUT/test/` directory.
- exampleX.xlsx

### ② Check that the namespace definitions have been added to `/USERS/usersettings.py`.
   ```sh
      'xmlns:BBBB="http://BBBB.corp/index.jp"'
      'xmlns:BBBBHPLC="http://BBBB.corp/ontology/hplc"'
      'xmlns:CDF="http://BBBB.corp/ontology/cdf"'
   ```

### ③ Execute the command:
   ```sh
      python excel2protocolMaiML2.py test
   ```

### ④ Verify the generated MaiML file in the /INPUT/test/ directory.
- exampleX.maiml
