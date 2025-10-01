import os, sys, uuid, copy, mimetypes, hashlib
from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET
import pandas as pd
from USERS.usersettings import filePath, time


################################################################################################################

### nanを空文字に変換 ###
def nan_to_empty_string(value):
    if pd.isna(value):
        return ""
    return str(value)

### uuid要素をバージョン４で生成 ###
def create_uuid():
    return str(uuid.uuid4())

### id属性の値がnanの場合、デフォルト値を設定 ###
def setID(value, tag, prefix=""):
    if pd.isna(value) or value == "":
        return f"def{tag}{prefix}ID"
    return str(value)

## valueの数値をフォーマット
def formatter_num(format_string, number):
    if '.' in format_string:
        decimal_places = len(format_string.split('.')[1])  # 小数点以下の桁数
    else:
        decimal_places = 0
    
    # 小数点以下の桁数に基づいて数値をフォーマット
    if decimal_places == 0:
        formatted = "{:.0f}".format(int(number))  # 整数としてフォーマット
    elif decimal_places == 1:
        formatted = "{:.1f}".format(float(number))  # 小数点以下1桁
    elif decimal_places == 2:
        formatted = "{:.2f}".format(float(number))  # 小数点以下2桁
    elif decimal_places == 3:
        formatted = "{:.3f}".format(float(number))  # 小数点以下3桁
    elif decimal_places == 4:
        formatted = "{:.4f}".format(float(number))  # 小数点以下4桁
    else:
        formatted = number  # それ以外の場合
    return formatted

### instruction要素のidを基に、親要素のprogram要素のidを検索して返す ###
def find_programID_by_instructionID(root, instruction_id):
    for program_elem in root.findall(".//program"):
        for instruction_elem in program_elem.findall(".//instruction"):
            if instruction_elem is not None and instruction_elem.get('id') == instruction_id:
                return program_elem.get("id"), instruction_elem.find("./uuid").text
    return None

### insertion要素のコンテンツを作成 ###
def make_insertion(value, instance_element, others_path=None):
    if pd.isna(value) or value == "":
        return instance_element
    filename = str(value)
    if others_path is not None:
        file_path = others_path / filename
    else:
        file_path =  filePath().INPUT_OTHER_PATH + filename

    # formatの取得
    extension = os.path.splitext(filename)[1]
    mime_type=''
    hash_sha256 = ''
    mimetypes.init()
    try:
        mime_type = mimetypes.types_map[extension]
    except Exception as e:
        print("[INFO]insertion file's mime_type is not exist.: ", filename)
        mime_type = 'none'
    try:
        with open(file_path, 'rb') as f:
            hash_sha256 = hashlib.sha256()
            while chunk := f.read(8192):  # 8KBごとにファイルを読み込む
                hash_sha256.update(chunk) 
            hash_sha256 = hash_sha256.hexdigest()
        print("[INFO]insertion file is loaded.: ", file_path)
    except FileNotFoundError as e:
        print("[INFO]Skip hash value generation because the input file does not exist in the directory. ", filename)
    except Exception as e:
        print(e)
        exit(1)
    ## insertion要素を追加
    insertion_element = ET.SubElement(instance_element, "insertion")
    insertion_uri_element = ET.SubElement(insertion_element, "uri")
    insertion_uri_element.text = './'+ filename   # MaiMLと同じフォルダを設定
    insertion_hash_element = ET.SubElement(insertion_element, "hash")
    insertion_hash_element.text = str(hash_sha256)
    insertion_format_element = ET.SubElement(insertion_element, "format")
    insertion_format_element.text = mime_type
    return instance_element

### 再帰的にproperty/content要素を探索し、keyが一致する要素を返す
def find_general_elements_by_key(element, key):
    matched_elements = []
    if element.tag in ("property", "content") and element.get("key") == key:
        matched_elements.append(element)
    for child in element:
        matched_elements.extend(find_general_elements_by_key(child, key))
    return matched_elements


### エクセルの日付のフォーマットをMaiMLのフォーマットに変換 ###
def change_time_format(e_datetime):
    e_datetime = pd.to_datetime(e_datetime).tz_localize(time().TIME_ZONE)
    return e_datetime.strftime(time().TIME_FORMAT)[:22] + ':' + e_datetime.strftime('%z')[3:]

### document要素のdate要素用に現在の時刻をxs:dateTime形式にフォーマットして返す ###
def get_current_datetime():
    # 現在のローカル時刻を取得
    local_time = datetime.now().astimezone()
    return local_time.strftime(time().TIME_FORMAT)[:22] + ':' + local_time.strftime('%z')[3:]

################################################################################################################


### MaiMLファイルを読み込む ###
def read_maiml(maiml_file):
    namespaces = {}
    ## 名前空間を保持しておく関数 ##
    def get_namespaces(xml_str):
        # ルート要素から名前空間の定義を取得する
        import re
        namespaces = {}
        match = re.findall(r'xmlns:([^=]+)="([^"]+)"', xml_str)
        for prefix, uri in match:
            namespaces[prefix] = uri
        default_ns = re.search(r'xmlns="([^"]+)"', xml_str)
        if default_ns:
            namespaces[""] = default_ns.group(1)  # デフォルト名前空間
        return namespaces
    
    ## 名前空間を除去してタグを簡略化する関数 ##
    def strip_namespace(element):
        for elem in element.iter():
            elem.tag = elem.tag.split("}")[-1]  # 名前空間を削除
    
    # XMLを文字列で読み込む
    xml_str = ''
    with open(maiml_file, "r", encoding="utf-8") as f:
        xml_str = f.read()
        # 名前空間を保存
        namespaces = get_namespaces(xml_str)
        ## maimlタグの'xsi:type'属性を削除
        for key in ['xsi:type="maimlRootType"','xsi:type="protocolFileRootType"', "xsi:type='maimlRootType'", "xsi:type='protocolFileRootTyp'"]:
            xml_str = xml_str.replace(key, '')
        
    # XML文字列をElementTreeで読み込む
    tree = ET.ElementTree(ET.fromstring(xml_str))
    root = tree.getroot()
        
    # タグから名前空間プレフィックスを削除（名前空間を気にせずに処理するため/xmlns:xsiは残る）
    strip_namespace(root)
    return tree, root, namespaces

## Excelファイルを読み込む ##
def read_excel(excel_file):
    df = pd.read_excel(excel_file)
    return df

## MaiMLデータとExcelデータをmerge ##
# 1シート→1method要素、1log要素
# 1行→1results,1trace要素
def merge_data(root, xls, others_path=None):
    # 入力MaiMLデータに<data>要素と<eventLog>要素が存在する場合は削除
    data_elem = root.find("./data")
    if data_elem is not None:
        root.remove(data_elem)
    eventLog_elem = root.find("./eventLog")
    if eventLog_elem is not None:
        root.remove(eventLog_elem)
    
    ## <data>要素を追加(id属性,<uuid>要素に自動生成した値を設定)
    data_element = ET.Element("data")
    data_element.set("id", setID("","data"))
    data_uuid_element = ET.SubElement(data_element, "uuid")
    data_uuid_element.text = create_uuid()
    
    ## <eventLog>要素を追加(id属性,<uuid>要素に自動生成した値を設定)
    eventLog_element = ET.Element("eventLog")
    eventLog_element.set("id", setID("","eventLog"))
    eventLog_uuid_element = ET.SubElement(eventLog_element, "uuid")
    eventLog_uuid_element.text = create_uuid()
    
    ## XMLツリーからtemplate・instructionのid属性のリストをそれぞれ作成
    protocol = root.find("./protocol")
    templates = protocol.findall(".//materialTemplate") + protocol.findall(".//conditionTemplate") + protocol.findall(".//resultTemplate")
    template_ids = [template.get("id") for template in templates]
    instructions = protocol.findall(".//instruction")
    instruction_ids = [instruction.get("id") for instruction in instructions]
        
    ## <method>要素のid属性値とエクセルデータのシート名を照合し、<log>要素を追加
    methods = protocol.findall(".//method")
    method_ids = [method.get("id") for method in methods]
    sheet_num = 0
    for method_id in method_ids:
        df_method = pd.DataFrame()
        try:
            df_method = xls.parse(f"@{method_id}", header=None) # ヘッダー無し
        except Exception as e:
            print("[Error]Error while reading the sheet: ", e)
            exit(1)
        if not df_method.empty:
            sheet_num += 1
            ## <eventLog>要素に<log>要素を追加(id属性に自動生成した値、ref属性に<method>要素のid属性値を設定)
            log_element = ET.SubElement(eventLog_element, "log")
            log_element.set("id", setID("","log", sheet_num))
            log_element.set("ref", method_id)
            log_uuid_element = ET.SubElement(log_element, "uuid")
            log_uuid_element.text = create_uuid()
            ## sheetの値を取得し、<trace>,<event>要素を追加
            ## １行目：instruction,templateのID
            row1 = df_method.iloc[0]
            template_list = {}
            instruction_list = {}
            for col_num, col in row1.items():
                # 1行目の値がtemplateのid属性値の場合（複数列存在）
                if col in template_ids: 
                    if col in template_list.keys():
                        template_list[col].append(col_num)
                    else:
                        template_list[col] = [col_num]  # 新しいリストを作成
                # 1行目の値が<instruction>要素のid属性値の場合（1列のみ存在）
                if col in instruction_ids:
                    if col in instruction_list.keys():
                        ## エラー処理
                        print("[Error]Instruction ID is duplicated.")
                        exit(1)
                    else:
                        instruction_list[col] = col_num  # 新しいリストを作成
            ## ２行目：１行目がtemplateのID列にkeyの値もしくは'INSERTION'
            row2 = df_method.iloc[1]
            ## ３行目以降：１行目がtemplateのID列→<results>要素を作成／１行目が<instruction>のID列に日付→<event>要素のコンテンツに追加
            row3over = df_method.iloc[2:]
            for _rownum, row in row3over.iterrows():
                results_id = setID(row[0],"results")
                ## <results>要素を追加(id属性に１列目の値を設定)
                results_element = ET.SubElement(data_element, "results")
                results_element.set("id", results_id)
                results_uuid_element = ET.SubElement(results_element, "uuid")
                results_uuid_element.text = create_uuid()
                ## MaiMLデータの全てのtemplateを取得し、<results>要素にインスタンス（material/condition/result）として追加
                for template in templates:
                    # results要素にinstance要素を追加
                    template_id = template.get("id")
                    element_name = template.tag
                    instance_element = ''
                    if element_name == "materialTemplate": # materialTemplate->material
                        instance_element = ET.SubElement(results_element, "material")
                    elif element_name == "conditionTemplate": # conditionTemplate->condition
                        instance_element = ET.SubElement(results_element, "condition")
                    elif element_name == "resultTemplate": # resultTemplate->result
                        instance_element = ET.SubElement(results_element, "result")
                    instance_element.set("id", setID("",element_name[:-8]+'_'+template_id,_rownum))
                    instance_element.set("ref", template_id)
                    instance_uuid_element = ET.SubElement(instance_element, "uuid")
                    instance_uuid_element.text = create_uuid()
                    
                    # template直下のpropertyとcontentのみ取得
                    template_properties = list(template.findall("./property")) + list(template.findall("./content"))

                    if template_properties:
                        instance_properties = [copy.deepcopy(prop) for prop in template_properties]
                        
                        # 2行目の値が、汎用データコンテナのkey属性値の場合は<value>要素の値を上書き／"INSERTION"の場合は<insertion>要素を追加
                        if template_id in template_list.keys():
                            for template_col_num in template_list[template_id]:
                                # row2[template_col_num]がinstance_propertiesのkeyに存在する場合、3行目以降のその列の値で上書き
                                key = row2[template_col_num]
                                # "INSERTION"の場合、insertion要素を追加
                                if key == "INSERTION":
                                    instance_element = make_insertion(row[template_col_num], instance_element, others_path)
                                    continue
                                
                                for general_element in instance_properties:
                                    # key一致する要素を再起的に探す
                                    matched_elements = find_general_elements_by_key(general_element, key)
                                    for match in matched_elements:
                                        value_element = match.find("./value")
                                        if value_element is None:
                                            value_element = ET.SubElement(match, "value")
                                        value = nan_to_empty_string(row[template_col_num])
                                        if pd.notna(match.get("formatString")):
                                            value = formatter_num(match.get("formatString"), value)
                                        value_element.text = value
                        instance_element.extend(instance_properties)
                        
                ## <instruction>要素のid属性値から、<trace>,<event>要素を生成する
                for instruction_id, instruction_colnum in instruction_list.items():
                    program_id , instruction_uuid = find_programID_by_instructionID(root,instruction_id)
                    ## <trace>要素を追加(idに自動生成した値、refに<program>要素のid値を設定)
                    trace_element = ET.SubElement(log_element, "trace")
                    trace_element.set("id", setID("","trace", _rownum))
                    trace_element.set("ref", program_id) # <trace>要素のref属性値は<program>要素のid属性値
                    trace_uuid_element = ET.SubElement(trace_element, "uuid")
                    trace_uuid_element.text = create_uuid()
                    
                    ## <event>要素を追加(idに自動生成した値、refに<instruction>要素のid値を設定)
                    event_element = ET.SubElement(trace_element, "event")
                    event_element.set("id", setID("","event", _rownum))
                    event_element.set("ref", instruction_id) # <event>要素のref属性値は<instruction>要素のid属性値
                    event_uuid_element = ET.SubElement(event_element, "uuid")
                    event_uuid_element.text = create_uuid()
                    
                    ## ３行目以降の値（日付）を取得し、<event>要素に必要なコンテンツを追加
                    for col_num, col in row.items():
                        if col_num == instruction_colnum:
                            property_element1 = ET.SubElement(event_element, "property")
                            property_element1.set("xsi:type", "uuidType")
                            property_element1.set("key", "concept:instance")
                            value_element1 = ET.SubElement(property_element1, "value")
                            value_element1.text = instruction_uuid
                            property_element2 = ET.SubElement(event_element, "property")
                            property_element2.set("xsi:type", "stringType")
                            property_element2.set("key", "lifecycle:transition")
                            value_element2 = ET.SubElement(property_element2, "value")
                            value_element2.text = "complete"
                            property_element3 = ET.SubElement(event_element, "property")
                            property_element3.set("xsi:type", "dateTimeType")
                            property_element3.set("key", "time:timestamp")
                            property_element3.set("formatString", "YYYY-MM-DDThh:mm:ssTZD")
                            value_element3 = ET.SubElement(property_element3, "value")
                            value_element3.text = change_time_format(col)   # 日付のフォーマットを変換してから追加
                            ## resultsRef要素を追加
                            resultsRef_element = ET.SubElement(event_element, "resultsRef")
                            resultsRef_element.set("id", f"{instruction_id}_{event_element.get('id')}_resultref")
                            resultsRef_element.set("ref", results_id)
    
    root.append(data_element)
    root.append(eventLog_element)
    return root
                
    
## 生成したMaiMLデータをファイルに書き出す ##
def write_maiml(root, output_file, namespaces):
    try:
        # ルート要素にすでにある名前空間を取得（ElementTreeが残してしまった名前空間への対処）
        existing_ns = {k: v for k, v in ET.ElementTree(root).getroot().attrib.items() if k.startswith("xmlns")}
        
        ## 元の名前空間を復元
        for prefix, uri in namespaces.items():
            # 取得した名前空間をルート要素に設定（重複がある場合はスキップ）
            attr_name = f"xmlns:{prefix}" if prefix else "xmlns"
            if attr_name not in existing_ns:  # 名前空間がルート要素にすでに存在している場合は追加しない
                if attr_name == "xmlns:xsi":  ## xmlns:xsiは隠れて存在するので追加しない（応急処置）
                    continue
                else:
                    root.set(attr_name, uri)
        
        ## MaiMLデータの更新
        ## maimlタグにxsi:type属性を追加
        root.set("xsi:type", "maimlRootType")
        ## documentのuuid,date要素を更新
        root.find("./document").find("./uuid").text = create_uuid()
        root.find("./document").find("./date").text = get_current_datetime() # 現在時刻をフォーマットして設定

        ## ファイルに書き出す
        tree = ET.ElementTree(root)
        ET.indent(tree, space="    ", level=0)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        print('[Error]Error while writing to the file.',e)
        exit(1)

## main処理 ##
def main(maiml_input, excel_input, maiml_output, rootdir=None):
    ## MAiMLファイルの読み込み
    tree = '' 
    root = ''
    try:
        tree, root, namespaces = read_maiml(maiml_input)
        print("[INFO]MaiML file is loaded.: "+ maiml_input)
    except Exception as e:
        print("[Error]An error occurred while reading the input file.: "+ maiml_input)
        print(e)
        exit(1)
    
    ## Excelファイルの読み込み
    xls = ''
    try:
        xls = pd.ExcelFile(excel_input)
        print("[INFO]Excel file is loaded.: "+ excel_input)
    except Exception as e:
        print("[Error]An error occurred while reading the input file.: "+ excel_input)
        print(e)
        exit(1)
        
    ## MaiMLデータとエクセルデータをマージ
    root = merge_data(root, xls, rootdir)
    
    ## ファイルへ書き出し
    write_maiml(root, maiml_output, namespaces)



## python実行関数 ##
if __name__ == "__main__":
    if len(sys.argv) > 1: ## 引数ありで実行
        # 引数で指定したディレクトリ内のエクセルファイルを取得
        rootdir = Path( filePath().INPUT_DIR + sys.argv[1])
        if rootdir.exists() and rootdir.is_dir():
            inputMaimlpath = ''
            inputExfilepath = ''
            outputMaimlpath = ''
            maimlfilenames = []
            exfilenames = []
            for file in rootdir.rglob('*'):  # rglob('*') で再帰的にすべてのファイルを取得
                # 拡張子が.maimlのファイルを取得
                if file.suffix in ['.maiml', '.mai']:
                    if file.is_file():  # ファイルかどうかを確認
                        if isinstance(maimlfilenames, list): # すでにリストが存在する場合
                            maimlfilenames.append(file) # リストに追加
                        else:
                            maimlfilenames = [file]
                # 拡張子が.xlsxのファイルを取得
                elif file.suffix == '.xlsx':
                    if file.is_file():  # ファイルかどうかを確認
                        if isinstance(exfilenames, list): # すでにリストが存在する場合
                            exfilenames.append(file)
                        else:
                            exfilenames = [file]
                            
            valid_job = False  # フラグを用意
            # maimlファイルからmethod要素のid属性値を取得し、エクセルファイルのシート名と照合
            for maimlfile in maimlfilenames:    
                inputMaimlpath = rootdir / maimlfile
                tree, root, namespaces = read_maiml(inputMaimlpath)

                protocol = root.find("./protocol")
                methods = protocol.findall(".//method")
                method_ids = [method.get("id") for method in methods]

                for exfile in exfilenames:
                    exfilename = exfile
                    inputExfilepath = rootdir / exfilename
                    try:
                        xls = pd.ExcelFile(inputExfilepath)
                        sheet_names = xls.sheet_names
                        # method要素のid属性値とシート名を照合
                        for method_id in method_ids:
                            if f"@{method_id}" in sheet_names:
                                outputMaimlpath = rootdir / f"{os.path.splitext(os.path.basename(exfilename))[0]}_output.maiml"
                                valid_job = True
                                break
                    except Exception as e:
                        print("[Error]An error occurred while reading the input file.: "+ str(inputExfilepath))
                        print(e)

            if valid_job:
                try:
                    main(str(inputMaimlpath), str(inputExfilepath), str(outputMaimlpath), rootdir=rootdir)
                    print("[INFO]Successfully created the MaiML data file. ", outputMaimlpath)
                except Exception as e:
                    print("[Error]Error: ", e)
            else:
                print("[Error]No valid MaiML/Excel pair found. Skipping execution.")

    else: ## 引数なしで実行
        inputMaimlpath = filePath().INPUT_MaiML_PATH
        inputExfilepath = filePath().INPUT_EXCEL_PATH
        outputMaimlpath = filePath().OUTPUT_FILE_PATH
        try:
            main(inputMaimlpath, inputExfilepath, outputMaimlpath)
            print("[INFO]Successfully created the MaiML data file. "+ outputMaimlpath)
        except Exception as e:
            print("[Error]Error : ",e)
