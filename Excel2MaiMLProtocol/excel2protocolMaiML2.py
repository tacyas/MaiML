import os, sys
from pathlib import Path
import pandas as pd
import xml.etree.ElementTree as ET
import uuid
from datetime import datetime
from USERS.usersettings import defaultNS, filePath


## エクセルの文字列をフォーマット
def clean_numeric(value):
    if isinstance(value, str):  
        value_num = value.strip("'\"")  # 先頭・末尾の ' や " を削除
        if value_num.replace(".", "", 1).isdigit():  # 数値なら変換
            return value_num
    return value 

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

## nanを空文字に変換
def nan_to_empty_string(value):
    if pd.isna(value):
        return ""
    return str(value)

## uuid要素をバージョン４で生成
def create_uuid():
    return str(uuid.uuid4())

## document要素のdate要素
def get_current_datetime():
    # 現在のローカル時刻を取得
    local_time = datetime.now().astimezone()
    # xs:dateTime形式にフォーマット
    formatted_time = local_time.strftime('%Y-%m-%dT%H:%M:%S') + f"{local_time.strftime('%z')[:3]}:{local_time.strftime('%z')[3:]}" 
    return formatted_time

## ID属性の値がnanの場合、デフォルト値を設定
def setID(value, tag, prefix=""):
    if pd.isna(value):
        return f"def{tag}{prefix}ID"
    return str(value)

class BaseElement:
    def add_element(self, parent, tag, row, prefix=""):
        try:
            if tag == "root":
                element = parent
            else:
                element = ET.SubElement(parent, tag, id=setID(row["#ID"], tag, prefix))
            # 共通部分
            #self.add_common_subelements(element, row)
        except KeyError:
            pass
        return element
    
    def add_common_subelements(self, element, row):
        try:
            ET.SubElement(element, "name").text = nan_to_empty_string(row["NAME"])
            ET.SubElement(element, "description").text = nan_to_empty_string(row["DESCRIPTION"])
        except KeyError:
            pass
        return element

## 単純要素
class SimElement(BaseElement):
    def add_element(self, parent, tag, row, prefix=""):
        element = super().add_element(parent, tag, row, prefix)
        return element

## グローバル要素
class GlobalElement(BaseElement):
    def add_element(self, parent, tag, row, prefix=""):
        # GlobalElement専用の追加処理
        element = super().add_element(parent, tag, row, prefix)
        uuid_value = create_uuid()
        try:
            uuid_value = uuid_value if str(row["UUID"]) == "nan" else nan_to_empty_string(row["UUID"])
        except KeyError:
            pass
        ET.SubElement(element, "uuid").text = uuid_value
        element = super().add_common_subelements(element, row)
        try:
            ET.SubElement(element, "annotation").text = nan_to_empty_string(row["ANNOTATION"])
        except KeyError:
            pass
        return element
    
## 汎用データコンテナ
class GenElement(BaseElement):
    def add_common_subelements(self, element, row, df):
        super().add_common_subelements(element, row)
        flag = 0
        for col in df.columns:
            if "VALUE" in col:
                if pd.isna(row[col]) and (row["#XSI:TYPE"] == "propertyListType" or flag >= 1):
                    pass
                else:
                    value = nan_to_empty_string(row["VALUE"])
                    if pd.notna(row["#FORMATSTRING"]):
                        value = formatter_num(row["#FORMATSTRING"], value)
                    ET.SubElement(element, "value").text = value
                    flag += 1
        return element

## creator要素のvendorRef/instrumentRef要素
def create_vendor_ref(creator, row, df, rownum):
    for col in df.columns:
        if "VENDORREF" in col:
            if pd.notna(row[col]):
                vendor_ref = ET.SubElement(creator, "vendorRef", id=f"def{col}{rownum}", ref=nan_to_empty_string(row[col]))
            else:
                print("The VENDORREF column is not listed in the CREATOR row.")
                exit(1)
        if "INSTRUMENTREF" in col and pd.notna(row[col]):
            vendor_ref = ET.SubElement(creator, "instrumentRef", id=f"def{col}{rownum}", ref=nan_to_empty_string(row[col]))

## instruction要素のtransitionRef要素
def create_transition_ref(instruction, row, df, rownum):
    for col in df.columns:
        if "TRANSITIONREF" in col:
            if pd.notna(row[col]):
                transition_ref = ET.SubElement(instruction, "transitionRef", id=f"def{col}{rownum}", ref=nan_to_empty_string(row[col]))
            else:
                print("The TRANSITIONREF column is not listed in the INSTRUCTION line.")
                exit(1)
            
## arc要素のsource/target属性
def create_arc(arc, row, df, rownum):
    for col in df.columns:
        if "SOURCE" in col and pd.notna(row[col]):
            arc.set("source", nan_to_empty_string(row[col]))
        if "TARGET" in col and pd.notna(row[col]):
            arc.set("target", nan_to_empty_string(row[col]))

## materialTemplate/conditionTemplate/resultTemplate要素のplaceRef/templateRef要素
def create_template_ref(template, row, df, rownum):
    for col in df.columns:
        if "PLACEREF" in col and pd.notna(row[col]):
            place_ref = ET.SubElement(template, "placeRef", id=f"defPLACEREF{nan_to_empty_string(row['#ID'])}{rownum}", ref=nan_to_empty_string(row[col]))
        if "TEMPLATEREF" in col and pd.notna(row[col]):
            template_ref = ET.SubElement(template, "templateRef", id=f"defTEMPLATEREF{nan_to_empty_string(row['#ID'])}{rownum}", ref=nan_to_empty_string(row[col]))

## materialTemplate/conditionTemplate/resultTemplate要素を順番に並べる
def sort_templates(parent):
    template_types = ["materialTemplate", "conditionTemplate", "resultTemplate"]
    
    elements = []
    for t_type in template_types:
        elements.extend(parent.findall(t_type))

    for element in elements:
        parent.remove(element)  # 一旦削除
    
    for element in elements:
        parent.append(element)  # 順番通りに追加


## DOCUMENTシートを処理
def process_document(xls, sheet_name):
    df = xls.parse(sheet_name)
    #df = df.map(clean_string)
    df = df.map(clean_numeric)
    
    document = ET.Element("document")
    gen_element = GlobalElement()

    for num, row in df.iterrows():
        if row["TAG"] == "DOCUMENT":
            document.set("id", setID(row["#ID"],"document"))
            gen_element.add_element(document, "root", row, num)
        elif row["TAG"] == "CREATOR":
            creator = gen_element.add_element(document, "creator", row, num)
            create_vendor_ref(creator, row, df, num)
        elif row["TAG"] == "VENDOR":
            gen_element.add_element(document, "vendor", row, num)
        elif row["TAG"] == "OWNER":
            gen_element.add_element(document, "owner", row, num)
        elif row["TAG"] == "INSTRUMENT":
            if pd.isna(row["#ID"]):
                pass
            else:
                gen_element.add_element(document, "instrument", row, num)
    # DATE
    ET.SubElement(document, "date").text = get_current_datetime()
    return document


## PROTOCOLシートを処理
def process_protocol(xls, sheet_name):
    #print("PROTOCOL")
    df = xls.parse(sheet_name)
    df = df.map(clean_numeric)

    protocol = ET.Element("protocol")
    sim_element = SimElement()
    gen_element = GlobalElement()
    for num, row in df.iterrows():
        if row["TAG"] == "PROTOCOL":
            protocol.set("id", setID(row["#ID"],"protocol"))
            gen_element.add_element(protocol, "root", row, num)
        elif row["TAG"] == "METHOD":
            method = gen_element.add_element(protocol, "method", row, num)
        elif row["TAG"] == "PNML":
            if pd.isna(row['PARENTID']):
                print("The PARENTID column is not listed in the PNML line.")
                exit(1)
            method4pnml = protocol.find(f".//method[@id='{row['PARENTID']}']")
            gen_element.add_element(method4pnml, "pnml", row, num)
        elif row["TAG"] == "PROGRAM":
            if pd.isna(row['PARENTID']):
                print("The PARENTID column is not listed in the PROGRAM line.")
                exit(1)
            method4program = protocol.find(f".//method[@id='{row['PARENTID']}']")
            gen_element.add_element(method4program, "program", row, num)
        elif row["TAG"] == "INSTRUCTION":
            if pd.isna(row['PARENTID']):
                print("The PARENTID column is not listed in the INSTRUCTION line.")
                exit(1)
            program = protocol.find(f".//program[@id='{row['PARENTID']}']")
            instruction = gen_element.add_element(program, "instruction", row, num)
            create_transition_ref(instruction, row, df, num)
            
    pnmls = protocol.findall(".//pnml")
    for pnml in pnmls if isinstance(pnmls, list) else [pnmls]:
        pnml_id = pnml.get("id")
        if f"@{pnml_id}" not in xls.sheet_names:
            break
        df_pnml = xls.parse(f"@{pnml_id}")
        df_pnml = df_pnml.map(clean_numeric)
        
        for num_PNML, row_PNML in df_pnml.iterrows():
            if row_PNML["TYPE"] == "PLACE":
                place = sim_element.add_element(pnml, "place", row_PNML, num_PNML)
            elif row_PNML["TYPE"] == "TRANSITION":
                transition = sim_element.add_element(pnml, "transition", row_PNML, num_PNML)
            elif row_PNML["TYPE"] == "ARC":
                arc = sim_element.add_element(pnml, "arc", row_PNML, num_PNML)
                create_arc(arc, row_PNML, df_pnml, num_PNML)
        
        ## pnmlのコンテンツを要素順に並べる
        arclist = pnml.findall(".//arc")
        placelist = pnml.findall(".//place")
        transitionlist = pnml.findall(".//transition")
        
        # 要素を削除して追加
        for place in placelist:
            pnml.remove(place)
            pnml.append(place)
        for transition in transitionlist:
            pnml.remove(transition)
            pnml.append(transition)
        for arc in arclist:
            pnml.remove(arc)
            pnml.append(arc)

    ## program/method/protocol要素にテンプレートを追加
    elements = protocol.findall(".//program") + protocol.findall(".//method") + [protocol]

    for element in elements:
        element_id = element.get("id")
        if f"@{element_id}" not in xls.sheet_names:
            continue
        df_element = xls.parse(f"@{element_id}")
        df_element = df_element.map(clean_numeric)
        
        for num_element, row_element in df_element.iterrows():
            if row_element["TYPE"] == "MATERIALTEMPLATE":
                materialTemplate = gen_element.add_element(element, "materialTemplate", row_element, num_element)
                create_template_ref(materialTemplate, row_element, df_element, num_element)
            elif row_element["TYPE"] == "CONDITIONTEMPLATE":
                conditionTemplate = gen_element.add_element(element, "conditionTemplate", row_element, num_element)
                create_template_ref(conditionTemplate, row_element, df_element, num_element)
            elif row_element["TYPE"] == "RESULTTEMPLATE":
                resultTemplate = gen_element.add_element(element, "resultTemplate", row_element, num_element)
                create_template_ref(resultTemplate, row_element, df_element, num_element)  
    
    # TEMPLATEシートの処理
    #print("TEMPLATE")
    df_template = xls.parse("TEMPLATE")
    #df_template = df_template.map(clean_string)
    df_template = df_template.map(clean_numeric)
    parentgenerallist = {}
    childgenerallist = {}
    gen_element = GenElement()
    
    for num_TEMPLATE, row_TEMPLATE in df_template.iterrows():
        template_id = ''
        general = ''
        try:
            template_id = str(row_TEMPLATE["TEMPLATEID"])  # IDを文字列に変換
            ## 汎用データコンテナを作成
            general = ET.Element(str(row_TEMPLATE["TYPE"]))
            # 必須属性
            general.set("key", str(row_TEMPLATE["#KEY"]))
            general.set("xsi:type", str(row_TEMPLATE["#XSI:TYPE"]))
        except KeyError as e:
            print("There is an error on the TEMPLATE sheet.", e)
            exit(1)
            
        # 必須でない属性
        attributes = {
            "units": "#UNITS",
            "formatstring": "#FORMATSTRING",
            "scaleFactor": "#SCALEFACTOR",
            "axis": "#AXIS",
            "size": "#SIZE"
        }
        for attr, col_name in attributes.items():
            if col_name in df_template.columns and not pd.isna(row_TEMPLATE[col_name]):
                general.set(attr, str(row_TEMPLATE[col_name]))  ## 特殊文字を削除
                
        # 子要素を追加
        gen_element.add_common_subelements(general, row_TEMPLATE, df_template)
        
        ## 汎用データコンテナのネスト対応
        if pd.isna(row_TEMPLATE["PARENTKEY"]):    # 親要素の場合parentgenerallist に追加
            parentgenerallist.setdefault(template_id, []).append(general)
        else:  # 子要素の場合childgenerallist に追加
            ET.SubElement(general, "parentkey").text = nan_to_empty_string(row_TEMPLATE["PARENTKEY"])  ## 一時的に親要素のkeyをparentkey要素として格納
            childgenerallist.setdefault(template_id, []).append(general)
    
    # XMLツリーからidが一致するタグを検索
    for template in protocol.findall(".//materialTemplate") + protocol.findall(".//conditionTemplate") + protocol.findall(".//resultTemplate"):
        template_id = template.get("id")
        parentgeneral = parentgenerallist.get(template_id, [])
        childgeneral = childgenerallist.get(template_id, [])
        
        ## 以降の無限ループ回避のため、入力データに間違いがないかチェック
        checkkeylist = []
        for parent in parentgeneral:
            parent_key = parent.get("key")
            checkkeylist.append(parent_key)
        checkchildkeylist = []
        for child in list(childgeneral):
            child_key = child.get("key")
            checkkeylist.append(child_key)
            child_parent_key_element = child.find(".//parentkey")
            checkchildkeylist.append(child_parent_key_element.text)
        ## checkchildkeylistのkeyがcheckkeylistに存在しない場合はエラー
        checkkeyset = set(checkkeylist)
        missing_keys = [key for key in checkchildkeylist if key not in checkkeyset]
        if missing_keys:
            print("The PARENTKEY column on the TEMPLATE sheet is incorrect. ", missing_keys)
            exit(1)
        
        for parent in parentgeneral:
            template.append(parent)
            parent_key = parent.get("key")
            
            for child in list(childgeneral):
                child_parent_key_element = child.find(".//parentkey")
                if child_parent_key_element is not None and child_parent_key_element.text == parent_key:
                    childgeneral.remove(child)
                    child.remove(child_parent_key_element)
                    parent.append(child)
        # 子要素がネストで存在する場合
        while childgeneral:
            for child in list(childgeneral):
                child_key_element = child.find(".//parentkey")
                if child_key_element is not None:
                    child_key = child_key_element.text
                    parent2 = parent.find(f".//*[@key='{child_key}']")
                    if parent2 is not None:
                        childgeneral.remove(child)
                        child.remove(child_key_element)  # <parentkey>タグを削除
                        parent2.append(child)  # 親要素に追加
    
        ## コンテンツを要素順に並べる
        placereflist = template.findall(".//placeRef")
        templatereflist = template.findall(".//templateRef")
        # 要素を削除して追加
        for placeref in placereflist:
            template.remove(placeref)
            template.append(placeref)
        for templateref in templatereflist:
            template.remove(templateref)
            template.append(templateref)

    ## program,method,protocolのtemplateコンテンツを要素順に並べる
    for program in protocol.findall(".//program"):
        sort_templates(program)
    for method in protocol.findall(".//method"):
        sort_templates(method)
    sort_templates(protocol)
    return protocol


def main(exfilepath, maimlpath):
    # Excelファイルの読み込み
    xls = ''
    try:
        xls = pd.ExcelFile(exfilepath)
        print("Excel file is loaded.: "+ exfilepath)
    except Exception as e:
        print("An error occurred while reading the input file.: "+ exfilepath)
        print(e)
        exit(1)
        
    # DOCUMENTシートを処理
    document_xml = process_document(xls, "DOCUMENT")

    # PROTOCOLシートを処理
    protocol_xml = process_protocol(xls, "PROTOCOL")

    # MAIML XMLを生成
    maiml_xml = ET.Element("maiml")
    maiml_attrs = defaultNS().MAIML_ATTR
    for maiml_attr in maiml_attrs:
        maiml_xml.set(maiml_attr.split("=")[0], maiml_attr.split("=")[1].replace('"', ""))
    maiml_xml.append(document_xml)
    maiml_xml.append(protocol_xml)

    # XMLを文字列に変換しファイル保存
    try:
        tree = ET.ElementTree(maiml_xml)
        ET.indent(tree, space="    ", level=0)
        tree.write(maimlpath, encoding="utf-8", xml_declaration=True)
    except Exception as e:
        print('Error while writing to the file.',e) 


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # 引数で指定したディレクトリ内のエクセルファイルを取得
        rootdir = Path( filePath().INPUT_DIR + sys.argv[1])
        if rootdir.exists() and rootdir.is_dir():
            for file in rootdir.rglob('*'):  # rglob('*') で再帰的にすべてのファイルを取得
                if file.is_file():  # ファイルかどうかを確認
                    # ファイル名と拡張子を分けて取得
                    file_extension = file.suffix  # 拡張子を取得
                    if file_extension == '.xlsx':
                        exfilename = file
                        inputExfilepath = rootdir / exfilename
                        outputMaimlpath = rootdir / f"{os.path.splitext(os.path.basename(exfilename))[0]}.maiml"
                        try:
                            main(str(inputExfilepath), str(outputMaimlpath))
                            print("Successfully created the MaiML data file. ", outputMaimlpath)
                        except Exception as e:
                            print('Error : ',e)
    else:
        inputExfilepath = filePath().INPUT_FILE_PATH
        outputMaimlpath = filePath().OUTPUT_FILE_PATH
        try:
            main(inputExfilepath, outputMaimlpath)
            print("Successfully created the MaiML data file. "+ outputMaimlpath)
        except Exception as e:
            print('Error : ',e)
