import os,copy,re

import xml.etree.ElementTree as ET
import glob, xmltodict, chardet

import uuid as UUID
from datetime import datetime as DT
from zoneinfo import ZoneInfo

from .staticClass import maimlelement, staticVal, settings
from .namespace import defaultNS


## XML読み込み（自動エンコーディング判定）####################################
def load_xml_with_auto_encoding(path, namespaces=None):
    with open(path, "rb") as f:
        raw = f.read()

    # chardetで推定
    result = chardet.detect(raw)
    enc = result["encoding"] or "utf-8"
    print(f"[INFO] Detected encoding: {enc} ({path})")

    try:
        text = raw.decode(enc)
    except UnicodeDecodeError:
        # 推定失敗時はUTF-8で再挑戦
        text = raw.decode("utf-8", errors="replace")
        print("[WARN] Fallback to UTF-8 with replacement")

    # XML → dict変換
    data_dic = xmltodict.parse(text, process_namespaces=True, namespaces=namespaces)
    return data_dic


## FILE DIR PATH #################################################
class filepath:
    cur_file = __file__  #このファイルのパス
    codedir = os.path.dirname(cur_file) + '/'


################################################
##   logic of maiml data format
################################################
class UpdateMaiML():
    ## templateコンテンツのpropertyのvalue要素がなければ作成する
    ## call from 'copytemplate()'
    def create_property_value(self,property_list):
        if not isinstance(property_list, list):
            property_list = [property_list]
        for property_dict in property_list:
            property_dict.setdefault(maimlelement.value, "")
            if maimlelement.property in property_dict:
                property_dict[maimlelement.property] = self.create_property_value(property_dict[maimlelement.property])
        return property_list


    ## templateからdata用インスタンスを作る
    ## call from 'createFullMaimlDict()'
    def copytemplate(self, templatelist):
        instancelist = []
        instanceIDList = []
        for template_dict in templatelist:
            #  要素の順番はこの時点では保証しない
            instancedict = template_dict.copy()
            # 2.templateRefが存在した場合、インスタンス層の対応なし（削除する）
            instancedict.pop(maimlelement.templateRef, None)
            del instancedict[maimlelement.placeRef]
            instance_id = template_dict[maimlelement.idd]+'_instance'
            instanceIDList.append(instance_id)
            instance_attribute = {
                maimlelement.idd:instance_id,
                maimlelement.refd:template_dict[maimlelement.idd]
                }
            instance_elements = {
                maimlelement.uuid:str(UUID.uuid4()),
                }
            instancedict.update(
                **instance_attribute, 
                **instance_elements
                )
            # templateが持つpropertyにvalue要素がなければ空のvalue要素を作る
            if maimlelement.property in instancedict.keys():
                property_list = instancedict[maimlelement.property]
                self = UpdateMaiML()
                instancedict[maimlelement.property] = self.create_property_value(property_list)
                
            instancelist.append(instancedict)
        return instancelist, instanceIDList

    
    ### dict(document + protocol --> + data + eventLog)
    def createFullMaimlDict(self,maiml_dict):
        full_dict = copy.deepcopy(maiml_dict)
        ## 必須の修正部分：document要素のUUID等を更新
        full_dict[maimlelement.maiml][maimlelement.document][maimlelement.uuid] = str(UUID.uuid4())

        ## デフォルトMaiMLファイルからdata要素とeventLog要素のDictを作成
        data_dic = []
        defo_filepath = filepath.codedir + staticVal.default_data_filepath
        #with open(defo_filepath, 'r', encoding='utf-8') as inF:
            #data_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=defaultNS.namespaces)
        data_dic = load_xml_with_auto_encoding(defo_filepath, namespaces=defaultNS.namespaces)
        ## data要素を作成( Template-->instance )
        full_dict[maimlelement.maiml][maimlelement.data] = copy.deepcopy(data_dic[maimlelement.maiml][maimlelement.data])
        ## 要素と属性値の追加と編集
        protocol_dict = maiml_dict[maimlelement.maiml][maimlelement.protocol]
        new_data_dict = full_dict[maimlelement.maiml][maimlelement.data]
        ## グローバル要素にUUIDを追加
        new_data_dict[maimlelement.uuid] = str(UUID.uuid4())
        new_data_dict[maimlelement.results][maimlelement.uuid] = str(UUID.uuid4())

        material_list = []
        condition_list = []
        result_list = []
        updateMaiml = UpdateMaiML()
        ## 1. results=1とし、すべての結果データを１つのresultsのコンテンツとする
        if maimlelement.materialTemplate in protocol_dict.keys():
            ptc_materialTemplate_list = protocol_dict[maimlelement.materialTemplate] if isinstance(protocol_dict[maimlelement.materialTemplate], list) else [protocol_dict[maimlelement.materialTemplate]]
            mlist, mIDlist = updateMaiml.copytemplate(ptc_materialTemplate_list)
            material_list += mlist
        if maimlelement.conditionTemplate in protocol_dict.keys():
            ptc_conditionTemplate_list = protocol_dict[maimlelement.conditionTemplate] if isinstance(protocol_dict[maimlelement.conditionTemplate], list) else [protocol_dict[maimlelement.conditionTemplate]]
            clist, cIDList = updateMaiml.copytemplate(ptc_conditionTemplate_list)
            condition_list += clist
        if maimlelement.resultTemplate in protocol_dict.keys():
            ptc_resultTemplate_list = protocol_dict[maimlelement.resultTemplate] if isinstance(protocol_dict[maimlelement.resultTemplate], list) else [protocol_dict[maimlelement.resultTemplate]]
            rlist, rIDlist = updateMaiml.copytemplate(ptc_resultTemplate_list)
            result_list += rlist
        method_list = protocol_dict[maimlelement.method] if isinstance(protocol_dict[maimlelement.method], list) else [protocol_dict[maimlelement.method]]
        for method_dict in method_list:
            if maimlelement.materialTemplate in method_dict.keys():
                m_materialTemplate_list = method_dict[maimlelement.materialTemplate] if isinstance(method_dict[maimlelement.materialTemplate], list) else [method_dict[maimlelement.materialTemplate]] 
                mmlist, mmIDlist = updateMaiml.copytemplate(m_materialTemplate_list)
                material_list += mmlist
            if maimlelement.conditionTemplate in method_dict.keys():
                m_conditionTemplate_list = method_dict[maimlelement.conditionTemplate] if isinstance(method_dict[maimlelement.conditionTemplate], list) else [method_dict[maimlelement.conditionTemplate]]
                mclist, mcIDlist = updateMaiml.copytemplate(m_conditionTemplate_list)
                condition_list += mclist
            if maimlelement.resultTemplate in method_dict.keys():
                m_resultTemplate_list = method_dict[maimlelement.resultTemplate] if isinstance(method_dict[maimlelement.resultTemplate], list) else [method_dict[maimlelement.resultTemplate]]
                mrlist, meIDlist = updateMaiml.copytemplate(m_resultTemplate_list)
                result_list += mrlist
            program_list = method_dict[maimlelement.program] if isinstance(method_dict[maimlelement.program], list) else [method_dict[maimlelement.program]]
            for program_dict in program_list:
                if maimlelement.materialTemplate in program_dict.keys():
                    p_materialTemplate_list = program_dict[maimlelement.materialTemplate] if isinstance(program_dict[maimlelement.materialTemplate], list) else [program_dict[maimlelement.materialTemplate]]
                    pmlist, pmIDlist = updateMaiml.copytemplate(p_materialTemplate_list)
                    material_list += pmlist
                if maimlelement.conditionTemplate in program_dict.keys():
                    p_conditionTemplate_list = program_dict[maimlelement.conditionTemplate] if isinstance(program_dict[maimlelement.conditionTemplate], list) else [program_dict[maimlelement.conditionTemplate]]
                    pclist, pcIDlist = updateMaiml.copytemplate(p_conditionTemplate_list)
                    condition_list += pclist
                if maimlelement.resultTemplate in protocol_dict[maimlelement.method][maimlelement.program].keys():
                    p_resultTemplate_list = program_dict[maimlelement.resultTemplate] if isinstance(program_dict[maimlelement.resultTemplate], list) else [program_dict[maimlelement.resultTemplate]]
                    prlist, prIDlist = updateMaiml.copytemplate(p_resultTemplate_list)
                    result_list += prlist
        new_data_dict[maimlelement.results].update({maimlelement.material:material_list})
        new_data_dict[maimlelement.results].update({maimlelement.condition:condition_list})
        new_data_dict[maimlelement.results].update({maimlelement.result:result_list})
        
        ## eventLog要素を作成
        #print('create eventLog contents=====================================================')
        full_dict[maimlelement.maiml][maimlelement.eventlog] = copy.deepcopy(data_dic[maimlelement.maiml][maimlelement.eventlog])
        full_dict[maimlelement.maiml][maimlelement.eventlog][maimlelement.uuid] = str(UUID.uuid4())

        ## 要素と属性値の追加と編集
        def_log_dict = full_dict[maimlelement.maiml][maimlelement.eventlog][maimlelement.log]
        def_trace_dict = full_dict[maimlelement.maiml][maimlelement.eventlog][maimlelement.log][maimlelement.trace]
        #def_event_dict = full_dict[maimlelement.maiml][maimlelement.eventlog][maimlelement.log][maimlelement.trace][maimlelement.event]
        def_property_list = full_dict[maimlelement.maiml][maimlelement.eventlog][maimlelement.log][maimlelement.trace][maimlelement.event][maimlelement.property]

        log_list = []
        # log.@ref <-- method.@id
        method_list = protocol_dict[maimlelement.method] if isinstance(protocol_dict[maimlelement.method], list) else [protocol_dict[maimlelement.method]]
        for method_dict in method_list:
            new_log_dict = copy.deepcopy(def_log_dict)
            new_log_dict[maimlelement.uuid] = str(UUID.uuid4())
            new_log_dict[maimlelement.idd] = method_dict[maimlelement.idd]+'_log'
            new_log_dict[maimlelement.refd] = method_dict[maimlelement.idd]
            # trace.@ref <-- program.@id
            program_list = method_dict[maimlelement.program] if isinstance(method_dict[maimlelement.program], list) else [method_dict[maimlelement.program]]
            trace_list = []
            for program_dict in program_list:
                new_trace_dict = copy.deepcopy(def_trace_dict)
                new_trace_dict[maimlelement.uuid] = str(UUID.uuid4())
                new_trace_dict[maimlelement.idd] = program_dict[maimlelement.idd]+'_trace'
                new_trace_dict[maimlelement.refd] = program_dict[maimlelement.idd]
                # event.@ref <-- instruction.@id  event.property.value <-- instruction.uuid
                event_list = []
                instruction_list = program_dict[maimlelement.instruction] if isinstance(program_dict[maimlelement.instruction], list) else [program_dict[maimlelement.instruction]]
                for instruction_dict in instruction_list:
                    event_dict = new_trace_dict[maimlelement.event].copy()
                    event_dict[maimlelement.uuid] = str(UUID.uuid4())
                    event_dict[maimlelement.idd] = instruction_dict[maimlelement.idd]+'_event'
                    event_dict[maimlelement.refd] = instruction_dict[maimlelement.idd]
                    
                    property_list = copy.deepcopy(def_property_list)
                    new_property_list = []
                    new_property_dict = {}
                    for property_dict in property_list:
                        new_property_dict = property_dict.copy()
                        if new_property_dict[maimlelement.keyd] == maimlelement.conceptinstance :
                            new_property_dict[maimlelement.value] = instruction_dict[maimlelement.uuid]
                        else:
                            pass
                        new_property_list.append(new_property_dict)
                    event_dict.update({maimlelement.property:new_property_list})
                    event_list.append(event_dict)
                    
                new_trace_dict.update({maimlelement.event:event_list})
                trace_list.append(new_trace_dict)
                
            new_log_dict.update({maimlelement.trace:trace_list})
            log_list.append(new_log_dict)
        full_dict[maimlelement.maiml][maimlelement.eventlog].update({maimlelement.log:log_list})
        return full_dict

        
################################################
##   Read & Write MaiML file class
################################################
class ReadWriteMaiML:
    ''' Global contents    nomal=(True:グローバル要素/False:特定グローバル要素) '''
    def writeGlobalContents(self, mydic, parentET, nomal=True):
        #print('writeGlobalContents')
        uuid = maimlelement.uuid
        global_uuid = ET.SubElement(parentET, uuid)    # =1
        global_uuid.text = mydic[uuid]
        '''
        if nomal:  ## uuid ver4
            global_uuid.text = str(UUID.uuid4())
        else:  ## uuid ver3
            if uuid in mydic.keys():
                global_uuid.text = mydic[uuid]
            else:
                print('uuid ver3')
                #########################################
        '''
        childUri = maimlelement.childUri     ## >=0
        if childUri in mydic.keys():
            if isinstance(mydic[childUri], list):
                childUri_list = mydic[childUri]
            else:
                childUri_list =[mydic[childUri]]
            for childUri_dic in childUri_list:
                global_childUri_Elem = ET.SubElement(parentET, childUri)
                global_childUri_Elem.text = childUri_dic
        childHash = maimlelement.childHash     ## >=0
        if childHash in mydic.keys():
            if isinstance(mydic[childHash], list):
                childHash_list = mydic[childHash]
            else:
                childHash_list =[mydic[childHash]]
            for childHash_dic in childHash_list:
                global_childHash_Elem = ET.SubElement(parentET, childHash)
                global_childHash_Elem.text = childHash_dic
        childUuid = maimlelement.childUuid     ##  >=0
        if childUuid in mydic.keys():
            if isinstance(mydic[childUuid], list):
                childUuid_list = mydic[childUuid]
            else:
                childUuid_list =[mydic[childUuid]]
            for childUuid_dic in childUuid_list:
                global_childUuid_Elem = ET.SubElement(parentET, childUuid)
                global_childUuid_Elem.text = childUuid_dic

        ################################
        ## EncryptedData(@xmlns':'http://www.w3.org/2001/04/xmlenc#)   0/1
        ################################

        insertion = maimlelement.insertion  ## >=0
        if insertion in mydic.keys():
            if isinstance(mydic[insertion], list):
                insertion_list = mydic[insertion]
            else:
                insertion_list =[mydic[insertion]]
            for insertion_dic in insertion_list:
                global_isnertion_Elem = ET.SubElement(parentET, insertion)
                insertion_uri = maimlelement.uri  ## =1
                insertion_uri_Elem = ET.SubElement(global_isnertion_Elem, insertion_uri)
                insertion_uri_Elem.text = insertion_dic[insertion_uri]
                insertion_hash = maimlelement.hash  ## =1
                insertion_hash_Elem = ET.SubElement(global_isnertion_Elem, insertion_hash)
                insertion_hash_Elem.text = insertion_dic[insertion_hash]
                '''if '@method' in insertion_dic[insertion_hash].keys():
                    insertion_hash_Elem.set('method', insertion_dic[insertion_hash]['@method'])
                    insertion_hash_Elem.text = insertion_dic[insertion_hash]['#text']
                else:
                    insertion_hash_Elem.text = insertion_dic[insertion_hash]
                '''
                insertion_uuid = maimlelement.uuid   ## 0/1
                if insertion_uuid in insertion_dic.keys():
                    insertion_uuid_Elem = ET.SubElement(global_isnertion_Elem, insertion_uuid)
                    insertion_uuid_Elem.text = insertion_dic[insertion_uuid]
                insertion_format = maimlelement.format   # 0/1
                if insertion_format in insertion_dic.keys():
                    insertion_format_Elem = ET.SubElement(global_isnertion_Elem, insertion_format)
                    insertion_format_Elem.text = insertion_dic[insertion_format]
        name = maimlelement.name        
        if name in mydic.keys():   # 0/1
            p_name_dic = mydic[name]
            p_name_Elem = ET.SubElement(parentET, name)
            p_name_Elem.text = p_name_dic
        description = maimlelement.description
        if description in mydic.keys():   # 0/1
            p_description_dic = mydic[description]
            p_description_Elem = ET.SubElement(parentET, description)
            p_description_Elem.text = p_description_dic
        annotation = maimlelement.annotation
        if annotation in mydic.keys():    # 0/1
            p_annotation_dic = mydic[annotation]
            p_annotation_Elem = ET.SubElement(parentET, annotation)
            p_annotation_Elem.text = p_annotation_dic
        
        ###################################################################################
        ## 汎用データコンテナ
        generalTagList = [maimlelement.property, maimlelement.content, maimlelement.uncertainty]
        ## property, content    >=0
        for generalTag in generalTagList:
            if generalTag in mydic.keys():
                if isinstance(mydic[generalTag], list):
                    property_list = mydic[generalTag]
                else:
                    property_list = [mydic[generalTag]]
                for property_nest in property_list:
                    try:
                        self.writeGenericdataContainer(property_nest, parentET, generalTag)
                    except Exception as e:
                        print('Error in writeGenericdataContainer.',e)
                        raise e
        ################################################################################### 
        

    ''' 汎用データコンテナのネスト構造に対応 '''
    def writeGenericdataContainer(self, mydic, parentET, mytag):
        #print('writeGenericdataContainer')
        # set attrib
        #print(mydic[maimlelement.typed])
        my_Elem = ET.SubElement(parentET, mytag, attrib={maimlelement.type:mydic[maimlelement.typed], maimlelement.key:mydic[maimlelement.keyd]})    # =1
        # set values  
        if maimlelement.formatStringd in mydic.keys() and mydic[maimlelement.formatStringd] != '':    # 0/1
            my_Elem.set(maimlelement.formatString, mydic[maimlelement.formatStringd])
        if maimlelement.unitsd in mydic.keys() and mydic[maimlelement.unitsd] != '':    # 0/1
            my_Elem.set(maimlelement.units, mydic[maimlelement.unitsd])
        if maimlelement.scaleFactord in mydic.keys() and mydic[maimlelement.scaleFactord] != '':    # 0/1
            my_Elem.set(maimlelement.scaleFactor, mydic[maimlelement.scaleFactord])
        ## content, uncertaintyが持つ属性
        if maimlelement.axisd in mydic.keys() and mydic[maimlelement.axisd] != '':    # 0/1
            my_Elem.set(maimlelement.axis, mydic[maimlelement.axisd])
        if maimlelement.sized in mydic.keys() and mydic[maimlelement.sized] != '':    # 0/1
            my_Elem.set(maimlelement.size, mydic[maimlelement.sized])
        if maimlelement.idd in mydic.keys() and mydic[maimlelement.idd] != '':    # 0/1
            my_Elem.set(maimlelement.id, mydic[maimlelement.idd])
        if maimlelement.refd in mydic.keys() and mydic[maimlelement.refd] != '':    # 0/1
            my_Elem.set(maimlelement.ref, mydic[maimlelement.refd])

        childUri = maimlelement.childUri   # >=0
        if childUri in mydic.keys():
            if isinstance(mydic[childUri], list):
                childUri_list = mydic[childUri]
            else:
                childUri_list = [mydic[childUri]]
            for childUri_dic in childUri_list:
                childUri_Elem = ET.SubElement(my_Elem, childUri)
                childUri_Elem.text = childUri_dic
        childHash = maimlelement.childHash   # >=0
        if childHash in mydic.keys():
            if isinstance(mydic[childHash], list):
                childHash_list = mydic[childHash]
            else:
                childHash_list = [mydic[childHash]]
            for childHash_dic in childHash_list:
                childHash_Elem = ET.SubElement(my_Elem, childHash)
                childHash_Elem.text = childHash_dic
        childUuid = maimlelement.childUuid   # >=0
        if childUuid in mydic.keys():
            if isinstance(mydic[childUuid], list):
                childUuid_list = mydic[childUuid]
            else:
                childUuid_list = [mydic[childUuid]]
            for childUuid_dic in childUuid_list:
                childUuid_Elem = ET.SubElement(my_Elem, childUuid)
                childUuid_Elem.text = childUuid_dic

        ##  EncryptedData  ## 0/1
        #print('Templates内のEncryptedDataの実装を忘れない')
        description = maimlelement.description
        if description in mydic.keys():    # 0/1
            my_Elem.set(description,mydic[description])
        value = maimlelement.value  ## >=0
        if value in mydic.keys():    #  >=0
            if isinstance(mydic[value], list):
                valueList = mydic[value]
            else:
                valueList = [mydic[value]]
            for value_dic in valueList:
                value_Elem = ET.SubElement(my_Elem, value)
                value_Elem.text = value_dic
        ##  property, content, uncertainty  >=0
        if maimlelement.property in mydic.keys():
            mytag = maimlelement.property
            if isinstance(mydic[mytag], list):
                for sinmydic in mydic[mytag]:
                    self.writeGenericdataContainer(sinmydic, my_Elem, mytag)
            else:
                a_mydic = mydic[mytag]
                a_mydic_ET = ET.SubElement(my_Elem, mytag, attrib={maimlelement.type:a_mydic[maimlelement.typed], maimlelement.key:a_mydic[maimlelement.keyd]})    # =1
                if maimlelement.formatStringd in a_mydic.keys():    # 0/1
                    a_mydic_ET.set(maimlelement.formatString, a_mydic[maimlelement.formatStringd])
                if maimlelement.unitsd in a_mydic.keys():    # 0/1
                    a_mydic_ET.set(maimlelement.units, a_mydic[maimlelement.unitsd])
                if maimlelement.scaleFactord in a_mydic.keys():    # 0/1
                    a_mydic_ET.set(maimlelement.scaleFactor, a_mydic[maimlelement.scaleFactor])
                childUri = maimlelement.childUri   # >=0
                if childUri in a_mydic.keys():
                    if isinstance(a_mydic[childUri], list):
                        a_childUri_list = a_mydic[childUri]
                    else:
                        a_childUri_list = [a_mydic[childUri]]
                    for a_childUri_dic in a_childUri_list:
                        a_childUri_Elem = ET.SubElement(a_mydic_ET, childUri)
                        a_childUri_Elem.text = a_childUri_dic
                childHash = maimlelement.childHash   # >=0
                if childHash in a_mydic.keys():
                    if isinstance(a_mydic[childHash], list):
                         a_childHash_list = a_mydic[childHash]
                    else:
                        a_childHash_list = [a_mydic[childHash]]
                    for a_childHash_dic in a_childHash_list:
                        a_childHash_Elem = ET.SubElement(a_mydic_ET, childHash)
                        a_childHash_Elem.text = a_childHash_dic
                childUuid = maimlelement.childUuid   # >=0
                if childUuid in a_mydic.keys():
                    if isinstance(a_mydic[childUuid], list):
                        a_childUuid_list = a_mydic[childUuid]
                    else:
                        a_childUuid_list = [a_mydic[childUuid]]
                    for a_childUuid_dic in a_childUuid_list:
                        a_childUuid_Elem = ET.SubElement(a_mydic_ET, childUuid)
                        a_childUuid_Elem.text = a_childUuid_dic
                ################# ##############
                ##  EncryptedData  0/1
                ###############################
                if maimlelement.description in a_mydic.keys():    # 0/1
                    a_mydic_ET.set(maimlelement.description, a_mydic[maimlelement.description])
                ##  value  >=0
                if maimlelement.value in a_mydic.keys():    #  >=0
                    if isinstance(a_mydic[maimlelement.value], list):
                        valueList = a_mydic[maimlelement.value]
                    else:
                        valueList = [a_mydic[maimlelement.value]]
                    for value_dic in valueList:
                        value_Elem = ET.SubElement(a_mydic_ET, maimlelement.value)
                        value_Elem.text = value_dic
                        #print(value_dic)
                if maimlelement.property in a_mydic.keys():
                    mytag = maimlelement.property
                elif maimlelement.content in a_mydic.keys():
                    mytag = maimlelement.content    
                elif maimlelement.uncertainty in a_mydic.keys():
                    mytag = maimlelement.uncertainty
                if mytag != '':
                    if isinstance(a_mydic[mytag], list):
                        for sinmydic in a_mydic[mytag]:
                            self.writeGenericdataContainer(sinmydic, a_mydic_ET, mytag)
                    else:
                        sinmydic = a_mydic[mytag]
                        self.writeGenericdataContainer(sinmydic, a_mydic_ET, mytag)
        if maimlelement.content in mydic.keys():
            mytag = maimlelement.content
            if isinstance(mydic[mytag], list):
                for sinmydic in mydic[mytag]:
                    self.writeGenericdataContainer(sinmydic, my_Elem, mytag)
            else:
                b_mydic = mydic[mytag]
                b_mydic_ET = ET.SubElement(my_Elem, mytag, attrib={maimlelement.type:b_mydic[maimlelement.typed], maimlelement.key:b_mydic[maimlelement.keyd]})    # =1
                if maimlelement.formatStringd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.formatString, b_mydic[maimlelement.formatStringd])
                if maimlelement.unitsd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.units, b_mydic[maimlelement.unitsd])
                if maimlelement.scaleFactord in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.scaleFactor, b_mydic[maimlelement.scaleFactord])
                ## content, uncertaintyが持つ属性
                if maimlelement.axisd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.axis, b_mydic[maimlelement.axisd])
                if maimlelement.sized in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.size, b_mydic[maimlelement.sized])
                if maimlelement.idd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.id, b_mydic[maimlelement.idd])
                if maimlelement.refd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.ref, b_mydic[maimlelement.refd])

                childUri = maimlelement.childUri   # >=0
                if childUri in b_mydic.keys():
                    if isinstance(b_mydic[childUri], list):
                        b_childUri_list = b_mydic[childUri]
                    else:
                        b_childUri_list = [b_mydic[childUri]]
                    for b_childUri_dic in b_childUri_list:
                        b_childUri_Elem = ET.SubElement(b_mydic_ET, childUri)
                        b_childUri_Elem.text = b_childUri_dic
                childHash = maimlelement.childHash   # >=0
                if childHash in b_mydic.keys():
                    if isinstance(b_mydic[childHash], list):
                         b_childHash_list = b_mydic[childHash]
                    else:
                        b_childHash_list = [b_mydic[childHash]]
                    for b_childHash_dic in b_childHash_list:
                        b_childHash_Elem = ET.SubElement(b_mydic_ET, childHash)
                        b_childHash_Elem.text = b_childHash_dic
                childUuid = maimlelement.childUuid   # >=0
                if childUuid in b_mydic.keys():
                    if isinstance(b_mydic[childUuid], list):
                        b_childUuid_list = b_mydic[childUuid]
                    else:
                        b_childUuid_list = [b_mydic[childUuid]]
                    for b_childUuid_dic in b_childUuid_list:
                        b_childUuid_Elem = ET.SubElement(b_mydic_ET, childUuid)
                        b_childUuid_Elem.text = b_childUuid_dic
                #####################################
                ##  EncryptedData  0/1
                #####################################
                if maimlelement.description in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.description, b_mydic[maimlelement.description])
                ##  value  >=0
                if maimlelement.value in b_mydic.keys():    #  >=0
                    if isinstance(b_mydic[maimlelement.value], list):
                        valueList = b_mydic[maimlelement.value]
                    else:
                        valueList = [b_mydic[maimlelement.value]]
                    for value_dic in valueList:
                        value_Elem = ET.SubElement(b_mydic_ET, maimlelement.value)
                        value_Elem.text = value_dic
                ##  property, content, uncertainty  >=0
                mytag = ''
                if maimlelement.property in b_mydic.keys():
                    mytag = maimlelement.property
                elif maimlelement.content in b_mydic.keys():
                    mytag = maimlelement.content
                elif maimlelement.uncertainty in b_mydic.keys():
                    mytag = maimlelement.uncertainty
                if mytag != '':
                    if isinstance(b_mydic[mytag], list):
                        for sinmydic in b_mydic[mytag]:
                            self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)
                    else:
                        sinmydic = b_mydic[mytag]
                        self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)
        if maimlelement.uncertainty in mydic.keys():
            mytag = maimlelement.uncertainty
            if isinstance(mydic[maimlelement.uncertainty], list):
                for sinmydic in mydic[maimlelement.uncertainty]:
                    self.writeGenericdataContainer(sinmydic, my_Elem, mytag)
            else:
                b_mydic = mydic[maimlelement.uncertainty]
                b_mydic_ET = ET.SubElement(my_Elem, mytag, attrib={maimlelement.type:b_mydic[maimlelement.typed], maimlelement.key:b_mydic[maimlelement.keyd]})    # =1
                if maimlelement.formatStringd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.formatString, b_mydic[maimlelement.formatStringd])
                if maimlelement.unitsd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.units, b_mydic[maimlelement.unitsd])
                if maimlelement.scaleFactord in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.scaleFactor, b_mydic[maimlelement.scaleFactord])
                ## content, uncertaintyが持つ属性
                if maimlelement.axisd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.axis, b_mydic[maimlelement.axis])
                if maimlelement.sized in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.size, b_mydic[maimlelement.sized])
                if maimlelement.idd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.id, b_mydic[maimlelement.idd])
                if maimlelement.refd in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.ref, b_mydic[maimlelement.refd])
                childUri = maimlelement.childUri   # >=0
                if childUri in b_mydic.keys():
                    if isinstance(b_mydic[childUri], list):
                        b_childUri_list = b_mydic[childUri]
                    else:
                        b_childUri_list = [b_mydic[childUri]]
                    for b_childUri_dic in b_childUri_list:
                        b_childUri_Elem = ET.SubElement(b_mydic_ET, childUri)
                        b_childUri_Elem.text = b_childUri_dic
                childHash = maimlelement.childHash   # >=0
                if childHash in b_mydic.keys():
                    if isinstance(b_mydic[childHash], list):
                         b_childHash_list = b_mydic[childHash]
                    else:
                        b_childHash_list = [b_mydic[childHash]]
                    for b_childHash_dic in b_childHash_list:
                        b_childHash_Elem = ET.SubElement(b_mydic_ET, childHash)
                        b_childHash_Elem.text = b_childHash_dic
                childUuid = maimlelement.childUuid   # >=0
                if childUuid in b_mydic.keys():
                    if isinstance(b_mydic[childUuid], list):
                        b_childUuid_list = b_mydic[childUuid]
                    else:
                        b_childUuid_list = [b_mydic[childUuid]]
                    for b_childUuid_dic in b_childUuid_list:
                        b_childUuid_Elem = ET.SubElement(b_mydic_ET, childUuid)
                        b_childUuid_Elem.text = b_childUuid_dic
                #####################################
                ##  EncryptedData  0/1
                #####################################
                if maimlelement.description in b_mydic.keys():    # 0/1
                    b_mydic_ET.set(maimlelement.description, b_mydic[maimlelement.description])
                ##  value  >=0
                if maimlelement.value in b_mydic.keys():    #  >=0
                    if isinstance(b_mydic[maimlelement.value], list):
                        valueList = b_mydic[maimlelement.value]
                    else:
                        valueList = [b_mydic[maimlelement.value]]
                    for value_dic in valueList:
                        value_Elem = ET.SubElement(b_mydic_ET, maimlelement.value)
                        value_Elem.text = value_dic
                ##  property, content, uncertainty    >=0
                mytag = ''
                if maimlelement.property in b_mydic.keys():
                    mytag = maimlelement.property
                elif maimlelement.content in b_mydic.keys():
                    mytag = maimlelement.content
                elif maimlelement.uncertainty in b_mydic.keys():
                    mytag = maimlelement.uncertainty
                if mytag != '':
                    if isinstance(b_mydic[mytag], list):
                        for sinmydic in b_mydic[mytag]:
                            self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)
                    else:
                        sinmydic = b_mydic[mytag]
                        self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)
            
                


    ''' TEMPLATESの作成 '''
    def writeTemplates(self, mydic, parentET):
        #print('writeTemplates')
        ## global contents
        self.writeGlobalContents(mydic, parentET)
        ## placeRef      >=1  参照要素
        if isinstance(mydic[maimlelement.placeRef], list):
            p_placeRef_list = mydic[maimlelement.placeRef]
        else:
            p_placeRef_list = [mydic[maimlelement.placeRef]]
        for p_placeRef_dic in p_placeRef_list:
            p_placeRef_Elem = ET.SubElement(parentET, maimlelement.placeRef, attrib={maimlelement.id:p_placeRef_dic[maimlelement.idd], maimlelement.ref:p_placeRef_dic[maimlelement.refd]})
            if maimlelement.name in p_placeRef_dic.keys():   # 0/1
                p_placeRef_name_dic = p_placeRef_dic[maimlelement.name]
                p_placeRef_name_Elem = ET.SubElement(p_placeRef_Elem, maimlelement.name)
                p_placeRef_name_Elem.text = p_placeRef_name_dic
            if maimlelement.description in p_placeRef_dic.keys():   # 0/1
                p_placeRef_description_dic = p_placeRef_dic[maimlelement.description]
                p_placeRef_description_Elem = ET.SubElement(p_placeRef_Elem, maimlelement.description)
                p_placeRef_description_Elem.text = p_placeRef_description_dic
        ## templateRef      >=0
        if maimlelement.templateRef in mydic.keys():
            if isinstance(mydic[maimlelement.templateRef], list):
                p_templateRef_list = mydic[maimlelement.templateRef]
            else:
                p_templateRef_list = [mydic[maimlelement.templateRef]]
            for p_templateRef_dic in p_templateRef_list:
                p_templateRef_Elem = ET.SubElement(parentET, maimlelement.templateRef, attrib={maimlelement.id:p_templateRef_dic[maimlelement.idd], maimlelement.ref:p_templateRef_dic[maimlelement.refd]})
                if maimlelement.name in p_templateRef_dic.keys():   # 0/1
                    p_templateRef_name_dic = p_templateRef_dic[maimlelement.name]
                    p_templateRef_name_Elem = ET.SubElement(p_templateRef_Elem, maimlelement.name)
                    p_templateRef_name_Elem.text = p_templateRef_name_dic
                if maimlelement.description in p_templateRef_dic.keys():   # 0/1
                    p_templateRef_description_dic = p_templateRef_dic[maimlelement.description]
                    p_templateRef_description_Elem = ET.SubElement(p_templateRef_Elem, maimlelement.description)
                    p_templateRef_description_Elem.text = p_templateRef_description_dic

    ''' INSTANCEの作成 '''
    def writeInstanceData(self, results_dic, results_Elem, mytag):
        #print('writeInstanceData:',mytag)
        if mytag in results_dic.keys():
            if isinstance(results_dic[mytag], list):
                mytag_list = results_dic[mytag]
            else:
                mytag_list = [results_dic[mytag]]
            for mytag_dic in mytag_list:
                mytag_Elem = ET.SubElement(results_Elem, mytag, attrib={maimlelement.id:mytag_dic[maimlelement.idd], maimlelement.ref:mytag_dic[maimlelement.refd]})
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in mytag_dic:
                    if rens.search(key):
                        mytag_Elem.set(key[1:],mytag_dic[key])
                ###########################################
                #global contents
                try:
                    self.writeGlobalContents(mytag_dic, mytag_Elem)
                except Exception as e:
                    print('Error in writeGlobalContents.',e)
                    raise e
                instanceRef = maimlelement.instanceRef    # >=0  参照要素
                if instanceRef in mytag_dic.keys():
                    if isinstance(mytag_dic[instanceRef], list):
                        mytag_instanceRef_list = mytag_dic[instanceRef]
                    else:
                        mytag_instanceRef_list = [mytag_dic[instanceRef]]
                    for mytag_instanceRef_dic in mytag_instanceRef_list:
                        mytag_instanceRef_Elem = ET.SubElement(mytag_Elem, instanceRef, attrib={maimlelement.id:mytag_instanceRef_dic[maimlelement.idd],maimlelement.ref:mytag_instanceRef_dic[maimlelement.refd]})
                        ###########################################
                        # namespace
                        rens = re.compile("@xmlns:.*")
                        for key in mytag_instanceRef_dic:
                            if rens.search(key):
                                mytag_instanceRef_Elem.set(key[1:],mytag_instanceRef_dic[key])
                        ###########################################
                        isinstanceRef_name = maimlelement.name   # 0/1
                        if isinstanceRef_name in mytag_instanceRef_dic.keys():
                            mytag_instanceRef_name_Elem = ET.SubElement(mytag_instanceRef_Elem, isinstanceRef_name)
                            mytag_instanceRef_name_Elem.text = mytag_instanceRef_dic[isinstanceRef_name]
                        isinstanceRef_description = maimlelement.description   # 0/1
                        if isinstanceRef_description in mytag_instanceRef_dic.keys():
                            mytag_instanceRef_description_Elem = ET.SubElement(mytag_instanceRef_Elem, isinstanceRef_description)
                            mytag_instanceRef_description_Elem.text = mytag_instanceRef_dic[isinstanceRef_description]


    ''' chain要素のネスト構造に対応 '''  ## 未テスト
    def writeChainContents(self, mydic, parentET):
        ## global contents 特定グローバル要素
        self.writeGlobalContents(mydic, parentET)
        chain_hash = maimlelement.hash   ## =1
        chain_hash_Elem = ET.SubElement(parentET, chain_hash)
        chain_hash_Elem.text = mydic[chain_hash]
        chain = maimlelement.chain  ## >=0
        if chain in mydic.keys():
            if isinstance(mydic[chain], list):
                chain_chain_list = mydic[chain]
            else:
                chain_chain_list = [mydic[chain]]
            for chain_chain_dic in chain_chain_list:
                child_chain_Elem = ET.SubElement(parentET, chain)
                if maimlelement.idd in chain_chain_dic.keys():
                    child_chain_Elem.set(maimlelement.id,chain_chain_dic[maimlelement.idd])
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in chain_chain_dic:
                    if rens.search(key):
                        child_chain_Elem.set(key[1:],chain_chain_dic[key])
                ###########################################
                self.writeChainContents(chain_chain_dic, child_chain_Elem)


    ''' parent要素のネスト構造に対応 '''  ## 未テスト
    def writeParentContents(self, mydic, parentET):
        ## global contents 特定グローバル要素
        self.writeGlobalContents(mydic, parentET)
        parentT_hash = maimlelement.hash   ## =1
        parentT_hash_Elem = ET.SubElement(parentET, parentT_hash)
        parentT_hash_Elem.text = mydic[parentT_hash]
        parentT = maimlelement.parent  ## >=0
        if parentT in mydic.keys():
            if isinstance(mydic[parentT], list):
                parent_parent_list = mydic[parentT]
            else:
                parent_parent_list = [mydic[parentT]]
            for parent_parent_dic in parent_parent_list:
                child_parent_Elem = ET.SubElement(parentET, parentT)
                if maimlelement.idd in parent_parent_dic.keys():
                    child_parent_Elem.set(maimlelement.id,parent_parent_dic[maimlelement.idd])
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in parent_parent_dic:
                    if rens.search(key):
                        child_parent_Elem.set(key[1:],parent_parent_dic[key])
                ###########################################
                self.writeParentContents(parent_parent_dic, child_parent_Elem)
    

    ''' 参照要素型 '''
    def writeReferenceContents(self, mydic, parentET, mytag):
        #print('writeReferenceContents')
        mytag_Elem = ET.SubElement(parentET, mytag, attrib={maimlelement.id:mydic[maimlelement.idd], maimlelement.ref:mydic[maimlelement.refd]})
        mytag_name = maimlelement.name
        if mytag_name in mydic.keys():
            resultsRef_name_Elem = ET.SubElement(mytag_Elem, mytag_name)
            resultsRef_name_Elem.text = mydic[mytag_name]
        mytag_description = maimlelement.description
        if mytag_description in mydic.keys():
            resultsRef_description_Elem = ET.SubElement(mytag_Elem, mytag_description)
            resultsRef_description_Elem.text = mydic[mytag_description]

    ''' 複数ファイル読み込み '''
    def readFiles(self):
        maimlfiles = glob.glob('./Files/input_data/*')
        fileNum = len(maimlfiles)
        index = 0
        # Read from maiml
        for i in range(fileNum):
            maiml = maimlfiles[index]
            index += 1
            #with open(maiml, 'r', encoding='utf-8') as inF:
            #    maiml_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=defaultNS.namespaces)
            maiml_dic = load_xml_with_auto_encoding(maiml, namespaces=defaultNS.namespaces)
            return maiml_dic

    ''' １ファイル読み込み '''
    def readFile(self, filepath):
        if filepath is None:
            maimlfile = '/test/input_data/SEMDataSample.maiml'
        else:
            maimlfile = filepath
        #with open(maimlfile, 'r', encoding='utf-8') as inF:
        #    maiml_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=defaultNS.namespaces)
        maiml_dic = load_xml_with_auto_encoding(maimlfile, namespaces=defaultNS.namespaces)
        return maiml_dic


    ''' Document Contents の作成 '''
    def createdocumentcontents(self,document_dic, document_Elem):
        #print('create <document> contents')
        ## Signature    0/1  署名のためのコンテンツ：未実装
        ## global contents 特定グローバル要素
        self.writeGlobalContents(document_dic, document_Elem)

        creator = 'creator'   ##>=1  特定グローバル要素
        if isinstance(document_dic[creator], list):
            creator_list = document_dic[creator]
        else:
            creator_list =[document_dic[creator]]
        for creator_dic in creator_list:
            creator_Elem = ET.SubElement(document_Elem, creator, attrib={'id':creator_dic['@id']})
            ###########################################
            # namespace
            rens = re.compile("@xmlns:.*")
            for key in creator_dic:
                if rens.search(key):
                    creator_Elem.set(key[1:],creator_dic[key])
            ###########################################
            ## global contents 特定グローバル要素
            self.writeGlobalContents(creator_dic, creator_Elem, False)
            vendorRef = 'vendorRef'  ## >=1 参照要素
            if isinstance(creator_dic[vendorRef], list):
                vendorRef_list = creator_dic[vendorRef]
            else:
                vendorRef_list = [creator_dic[vendorRef]]
            for vendorRef_dic in vendorRef_list:
                vendorRef_Elem = ET.SubElement(creator_Elem, vendorRef, attrib={'id':vendorRef_dic['@id'], 'ref':vendorRef_dic['@ref']})
                name = 'name'   ## 0/1
                if name in vendorRef_dic.keys():
                    vendorRef_name_Elem = ET.SubElement(vendorRef_Elem, name)
                    vendorRef_name_Elem.text = vendorRef_dic[name]
                description = 'description'   ## 0/1
                if description in vendorRef_dic.keys():
                    vendorRef_description_Elem = ET.SubElement(vendorRef_Elem, description)
                    vendorRef_description_Elem.text = vendorRef_dic[description]
                
            instrumentRef = 'instrumentRef'    ## >=0　参照要素
            if instrumentRef in creator_dic.keys():
                if isinstance(creator_dic[instrumentRef], list):
                    instrumentRef_list = creator_dic[instrumentRef]
                else:
                    instrumentRef_list = [creator_dic[instrumentRef]]
                for instrumentRef_dic in instrumentRef_list:
                    instrumentRef_Elem = ET.SubElement(creator_Elem, instrumentRef, attrib={'id':instrumentRef_dic['@id'], 'ref':instrumentRef_dic['@ref']})
                    name = 'name'   ## 0/1
                    if name in instrumentRef_dic.keys():
                        vendorRef_name_Elem = ET.SubElement(instrumentRef_Elem, name)
                        vendorRef_name_Elem.text = instrumentRef_dic[name]
                    description = 'description'   ## 0/1
                    if description in instrumentRef_dic.keys():
                        vendorRef_description_Elem = ET.SubElement(instrumentRef_Elem, description)
                        vendorRef_description_Elem.text = instrumentRef_dic[description]

        vendor = 'vendor'    ## >=1　　特定グローバル要素
        if isinstance(document_dic[vendor], list):
            vendor_list = document_dic[vendor]
        else:
            vendor_list =[document_dic[vendor]]
        for vendor_dic in vendor_list:
            vendor_Elem = ET.SubElement(document_Elem, vendor, attrib={'id':vendor_dic['@id']})
            ###########################################
            # namespace
            rens = re.compile("@xmlns:.*")
            for key in vendor_dic:
                if rens.search(key):
                    vendor_Elem.set(key[1:],vendor_dic[key])
            ###########################################
            ## global contents 特定グローバル要素
            self.writeGlobalContents(vendor_dic, vendor_Elem, False)

        owner = 'owner'    ## >=1　　特定グローバル要素
        if isinstance(document_dic[owner], list):
            owner_list = document_dic[owner]
        else:
            owner_list =[document_dic[owner]]
        for owner_dic in owner_list:
            owner_Elem = ET.SubElement(document_Elem, owner, attrib={'id':owner_dic['@id']})
            ###########################################
            # namespace
            rens = re.compile("@xmlns:.*")
            for key in owner_dic:
                if rens.search(key):
                    owner_Elem.set(key[1:],owner_dic[key])
            ###########################################
            ## global contents 特定グローバル要素
            self.writeGlobalContents(owner_dic, owner_Elem, False)

        instrument = 'instrument'   ##  >=0　　特定グローバル要素
        if instrument in document_dic.keys():
            if isinstance(document_dic[instrument], list):
                instrument_list = document_dic[instrument]
            else:
                instrument_list =[document_dic[instrument]]
            for instrument_dic in instrument_list:
                instrument_Elem = ET.SubElement(document_Elem, instrument, attrib={'id':instrument_dic['@id']})
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in instrument_dic:
                    if rens.search(key):
                        instrument_Elem.set(key[1:],instrument_dic[key])
                ###########################################
                ## global contents 特定グローバル要素
                self.writeGlobalContents(instrument_dic, instrument_Elem, False)

        date = 'date'    ## =1   xs:dateTime（2018-11-10T22:12:59+09:00）
        date_Elem = ET.SubElement(document_Elem, date)
        
        tz = ZoneInfo(key=settings.TIME_ZONE)
        nowtimestamp = DT.now(tz)
        create_date = nowtimestamp.strftime('%Y-%m-%dT%H:%M:%S') + nowtimestamp.strftime('%z')[:3] + ':' + nowtimestamp.strftime('%z')[3:]
        date_Elem.text = create_date

        chain = 'chain'   ## >=0    グローバル要素(?)
        if chain in document_dic.keys():
            if isinstance(document_dic[chain], list):
                chain_list = document_dic[chain]
            else:
                chain_list =[document_dic[chain]]
            for chain_dic in chain_list:
                chain_Elem = ET.SubElement(document_Elem, chain)
                if '@id' in chain_dic.keys():
                    chain_Elem.set('id', chain_dic['@id'])
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in chain_dic:
                    if rens.search(key):
                        chain_Elem.set(key[1:],chain_dic[key])
                ###########################################
                if '@key' in chain_dic.keys():
                    chain_Elem.set('key', chain_dic['@key'])
                ## nest
                self.writeChainContents(chain_dic, chain_Elem)

        parent = 'parent'   ## >=0    グローバル要素(?)
        if parent in document_dic.keys():
            if isinstance(document_dic[parent], list):
                parent_list = document_dic[parent]
            else:
                parent_list =[document_dic[parent]]
            for parent_dic in parent_list:
                parent_Elem = ET.SubElement(document_Elem, parent)
                if '@id' in parent_dic.keys():
                    parent_Elem.set('id', parent_dic['@id'])
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in parent_dic:
                    if rens.search(key):
                        parent_Elem.set(key[1:],parent_dic[key])
                ###########################################
                if '@key' in parent_dic.keys():
                    parent_Elem.set('key', parent_dic['@key'])
                ## nest
                self.writeParentContents(parent_dic, parent_Elem)


    ''' Protocol Contents の作成 '''
    def createprotocolcontents(self, protocol_dic, protocol_Elem):
        #print('create <protocol> contents')
        ## global contents
        self.writeGlobalContents(protocol_dic, protocol_Elem)
        
        #method = 'method'  ##contents   # >=1
        if isinstance(protocol_dic[maimlelement.method], list):
            method_list = protocol_dic[maimlelement.method]
        else:
            method_list = [protocol_dic[maimlelement.method]]
        for method_dic in method_list:
            #print(dict(method_dic))
            method_Elem = ET.SubElement(protocol_Elem, maimlelement.method, attrib={'id':method_dic['@id']})    # =1
            ###########################################
            # namespace
            rens = re.compile("@xmlns:.*")
            for key in method_dic:
                if rens.search(key):
                    method_Elem.set(key[1:],method_dic[key])
            ###########################################
            ## global contents
            self.writeGlobalContents(method_dic, method_Elem)
            
            #pnml = 'pnml'  ##  >=1
            if isinstance(method_dic[maimlelement.pnml], list):
                pnml_list = method_dic[maimlelement.pnml]
            else:
                pnml_list = [method_dic[maimlelement.pnml]]
            for pnml_dic in pnml_list:    # >=1
                pnml_Elem = ET.SubElement(method_Elem, maimlelement.pnml, attrib={'id':pnml_dic['@id']})   # =1
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in pnml_dic:
                    if rens.search(key):
                        pnml_Elem.set(key[1:],pnml_dic[key])
                ###########################################
                ## global contents
                self.writeGlobalContents(pnml_dic, pnml_Elem)

                #place = 'place'    # >=1
                if isinstance(pnml_dic[maimlelement.place], list):
                    place_list = pnml_dic[maimlelement.place]
                else:
                    place_list = [pnml_dic[maimlelement.place]]
                for place_dic in place_list:    # >=1
                    place_Elem = ET.SubElement(pnml_Elem, maimlelement.place, attrib={'id':place_dic['@id']})
                    #place_Elem.text = place_dic['#text']
                    #place_name = 'name'
                    if maimlelement.name in place_dic.keys():   # 0/1
                        place_name_dic = place_dic[maimlelement.name]
                        place_name_Elem = ET.SubElement(place_Elem, maimlelement.name)
                        place_name_Elem.text = place_name_dic
                    #place_description = 'description'
                    if maimlelement.description in place_dic.keys():   # 0/1
                        place_description_dic = place_dic[maimlelement.description]
                        place_description_Elem = ET.SubElement(place_Elem, maimlelement.description)
                        place_description_Elem.text = place_description_dic
                #transition = 'transition'    # >=1
                if isinstance(pnml_dic[maimlelement.transition], list):
                    transition_list = pnml_dic[maimlelement.transition]
                else:
                    transition_list = [pnml_dic[maimlelement.transition]]
                for transition_dic in transition_list:    # >=1
                    transition_Elem = ET.SubElement(pnml_Elem, maimlelement.transition, attrib={'id':transition_dic['@id']})
                    #transition_Elem.text = transition_dic[#text]
                    #transition_name = 'name'
                    if maimlelement.name in transition_dic.keys():   # 0/1
                        transition_name_dic = transition_dic[maimlelement.name]
                        transition_name_Elem = ET.SubElement(transition_Elem, maimlelement.name)
                        transition_name_Elem.text = transition_name_dic
                    #transition_description = 'description'
                    if maimlelement.description in transition_dic.keys():   # 0/1
                        transition_description_dic = transition_dic[maimlelement.description]
                        transition_description_Elem = ET.SubElement(transition_Elem, maimlelement.description)
                        transition_description_Elem.text = transition_description_dic
                #arc = 'arc'    # >=1
                if isinstance(pnml_dic[maimlelement.arc], list):
                    arc_list = pnml_dic[maimlelement.arc]
                else:
                    arc_list = [pnml_dic[maimlelement.arc]]
                for arc_dic in arc_list:    # >=1
                    arc_Elem = ET.SubElement(pnml_Elem, maimlelement.arc, attrib={'id':arc_dic['@id'], 'source':arc_dic['@source'], 'target':arc_dic['@target']})
                    #arc_name = 'name'
                    if maimlelement.name in arc_dic.keys():   # 0/1
                        arc_name_dic = arc_dic[maimlelement.name]
                        arc_name_Elem = ET.SubElement(arc_Elem, maimlelement.name)
                        arc_name_Elem.text = arc_name_dic
                    #arc_description = 'description'
                    if maimlelement.description in arc_dic.keys():   # 0/1
                        arc_description_dic = arc_dic[maimlelement.description]
                        arc_description_Elem = ET.SubElement(arc_Elem, maimlelement.description)
                        arc_description_Elem.text = arc_description_dic
            program = 'program'   ## contents   >=1
            if isinstance(method_dic[program], list):
                program_list = method_dic[program]
            else:
                program_list = [method_dic[program]]
            for program_dic in program_list:
                program_Elem = ET.SubElement(method_Elem, program, attrib={'id':program_dic['@id']})
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in program_dic:
                    if rens.search(key):
                        program_Elem.set(key[1:],program_dic[key])
                ###########################################
                ## global contents
                self.writeGlobalContents(program_dic, program_Elem)

                instruction = 'instruction'    #  >=1
                if isinstance(program_dic[instruction], list):
                    instruction_list = program_dic[instruction]
                else:
                    instruction_list = [program_dic[instruction]]
                for instruction_dic in instruction_list:
                    instruction_Elem = ET.SubElement(program_Elem, instruction, attrib={'id':instruction_dic['@id']})
                    ###########################################
                    # namespace
                    rens = re.compile("@xmlns:.*")
                    for key in instruction_dic:
                        if rens.search(key):
                            instruction_Elem.set(key[1:],instruction_dic[key])
                    ###########################################
                    ## global contents
                    self.writeGlobalContents(instruction_dic, instruction_Elem)
                    transitionRef = 'transitionRef'    ##  >=1 参照要素
                    if isinstance(instruction_dic[transitionRef], list):
                        transitionRef_list = instruction_dic[transitionRef]
                    else:
                        transitionRef_list = [instruction_dic[transitionRef]]
                    for transitionRef_dic in transitionRef_list:
                        transitionRef_Elem = ET.SubElement(instruction_Elem, transitionRef, attrib={'id':transitionRef_dic['@id'], 'ref':transitionRef_dic['@ref']})
                        transitionRef_name = 'name'
                        if transitionRef_name in transitionRef_dic.keys():   # 0/1
                            transitionRef_name_dic = transitionRef_dic[transitionRef_name]
                            transitionRef_name_Elem = ET.SubElement(transitionRef_Elem, transitionRef_name)
                            transitionRef_name_Elem.text = transitionRef_name_dic
                        transitionRef_description = 'description'
                        if transitionRef_description in transitionRef_dic.keys():   # 0/1
                            transitionRef_description_dic = transitionRef_dic[transitionRef_description]
                            transitionRef_description_Elem = ET.SubElement(transitionRef_Elem, transitionRef_description)
                            transitionRef_description_Elem.text = transitionRef_description_dic

                ## program -- TEMPLATES
                ## program -- materialTemplate  >=0
                materialTemplate = 'materialTemplate' 
                if materialTemplate in program_dic.keys():
                    if isinstance(program_dic[materialTemplate], list):
                       p_materialTemplate_list = program_dic[materialTemplate]
                    else:
                        p_materialTemplate_list = [program_dic[materialTemplate]]
                    for p_materialTemplate_dic in p_materialTemplate_list:
                        p_materialTemplate_Elem = ET.SubElement(program_Elem, materialTemplate, attrib={'id':p_materialTemplate_dic['@id']})
                        ###########################################
                        # namespace
                        rens = re.compile("@xmlns:.*")
                        for key in p_materialTemplate_dic:
                            if rens.search(key):
                                p_materialTemplate_Elem.set(key[1:],p_materialTemplate_dic[key])
                        ###########################################
                        # templates contents
                        self.writeTemplates(p_materialTemplate_dic, p_materialTemplate_Elem)
                ## program -- conditionTemplate  >=0
                conditionTemplate = 'conditionTemplate'
                if conditionTemplate in program_dic.keys():
                    if isinstance(program_dic[conditionTemplate], list):
                        p_conditionTemplate_list = program_dic[conditionTemplate]
                    else:
                        p_conditionTemplate_list = [program_dic[conditionTemplate]]
                    for p_conditionTemplate_dic in p_conditionTemplate_list:
                        p_conditionTemplate_Elem = ET.SubElement(program_Elem, conditionTemplate, attrib={'id':p_conditionTemplate_dic['@id']})
                        ###########################################
                        # namespace
                        rens = re.compile("@xmlns:.*")
                        for key in p_conditionTemplate_dic:
                            if rens.search(key):
                                p_conditionTemplate_Elem.set(key[1:],p_conditionTemplate_dic[key])
                        ###########################################
                        # templates contents
                        self.writeTemplates(p_conditionTemplate_dic, p_conditionTemplate_Elem)
                ## program -- resultTemplate  >=0
                resultTemplate = 'resultTemplate'
                if resultTemplate in program_dic.keys():
                    if isinstance(program_dic[resultTemplate], list):
                        p_resultTemplate_list = program_dic[resultTemplate]
                    else:
                        p_resultTemplate_list = [program_dic[resultTemplate]]
                    for p_resultTemplate_dic in p_resultTemplate_list:
                        p_resultTemplate_Elem = ET.SubElement(program_Elem, resultTemplate, attrib={'id':p_resultTemplate_dic['@id']})
                        ###########################################
                        # namespace
                        rens = re.compile("@xmlns:.*")
                        for key in p_resultTemplate_dic:
                            if rens.search(key):
                                p_resultTemplate_Elem.set(key[1:],p_resultTemplate_dic[key])
                        ###########################################
                        # templates contents
                        self.writeTemplates(p_resultTemplate_dic, p_resultTemplate_Elem)

            ## method -- TEMPLATES
            ## method -- materialTemplate  >=0
            materialTemplate = 'materialTemplate'
            if materialTemplate in method_dic.keys():
                if isinstance(program_dic[materialTemplate], list):
                    m_materialTemplate_list = method_dic[materialTemplate]
                else:
                    m_materialTemplate_list = [method_dic[materialTemplate]]
                for m_materialTemplate_dic in m_materialTemplate_list:
                    m_materialTemplate_Elem = ET.SubElement(method_Elem, materialTemplate, attrib={'id':m_materialTemplate_dic['@id']})
                    ###########################################
                    # namespace
                    rens = re.compile("@xmlns:.*")
                    for key in m_materialTemplate_dic:
                        if rens.search(key):
                            m_materialTemplate_Elem.set(key[1:],m_materialTemplate_dic[key])
                    ###########################################
                    # templates contents
                    self.writeTemplates(m_materialTemplate_dic, m_materialTemplate_Elem)
            ## method -- conditionTemplate  >=0
            conditionTemplate = 'conditionTemplate'
            if conditionTemplate in method_dic:
                if isinstance(program_dic[conditionTemplate], list):
                    m_conditionTemplate_list = method_dic[conditionTemplate]
                else:
                    m_conditionTemplate_list = [method_dic[conditionTemplate]]
                for m_conditionTemplate_dic in m_conditionTemplate_list:
                    m_conditionTemplate_Elem = ET.SubElement(method_Elem, conditionTemplate, attrib={'id':m_conditionTemplate_dic['@id']})
                    ###########################################
                    # namespace
                    rens = re.compile("@xmlns:.*")
                    for key in m_conditionTemplate_dic:
                        if rens.search(key):
                            m_conditionTemplate_Elem.set(key[1:],m_conditionTemplate_dic[key])
                    ###########################################
                    # templates contents
                    self.writeTemplates(m_conditionTemplate_dic, m_conditionTemplate_Elem)
            ## method -- resultTemplate  >=0
            resultTemplate = 'resultTemplate'
            if resultTemplate in method_dic:
                if isinstance(program_dic[resultTemplate], list):
                    m_resultTemplate_list = method_dic[resultTemplate]
                else:
                    m_resultTemplate_list = [method_dic[resultTemplate]]
                for m_resultTemplate_dic in m_resultTemplate_list:
                    m_resultTemplate_Elem = ET.SubElement(method_Elem, resultTemplate, attrib={'id':m_resultTemplate_dic['@id']})
                    ###########################################
                    # namespace
                    rens = re.compile("@xmlns:.*")
                    for key in m_resultTemplate_dic:
                        if rens.search(key):
                            m_resultTemplate_Elem.set(key[1:],m_resultTemplate_dic[key])
                    ###########################################
                    # templates contents
                    self.writeTemplates(m_resultTemplate_dic, m_resultTemplate_Elem)

        ## protocol -- TEMPLATES
        materialTemplate = 'materialTemplate'   ## >=0
        if materialTemplate in protocol_dic.keys():
            if isinstance(protocol_dic[materialTemplate], list):
                materialTemplate_list = protocol_dic[materialTemplate]
            else:
                materialTemplate_list = [protocol_dic[materialTemplate]]
            for materialTemplate_dic in materialTemplate_list:
                materialTemplate_Elem = ET.SubElement(protocol_Elem, materialTemplate, attrib={'id':materialTemplate_dic['@id']})
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in materialTemplate_dic:
                    if rens.search(key):
                        materialTemplate_Elem.set(key[1:],materialTemplate_dic[key])
                ###########################################
                # templates contents
                self.writeTemplates(materialTemplate_dic, materialTemplate_Elem)
        conditionTemplate = 'conditionTemplate'  ## >=0
        if conditionTemplate in protocol_dic:
            if isinstance(protocol_dic[conditionTemplate], list):
                conditionTemplate_list = protocol_dic[conditionTemplate]
            else:
                conditionTemplate_list = [protocol_dic[conditionTemplate]]
            for conditionTemplate_dic in conditionTemplate_list:
                conditionTemplate_Elem = ET.SubElement(protocol_Elem, conditionTemplate, attrib={'id':conditionTemplate_dic['@id']})
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in conditionTemplate_dic:
                    if rens.search(key):
                        conditionTemplate_Elem.set(key[1:],conditionTemplate_dic[key])
                ###########################################
                # templates contents
                self.writeTemplates(conditionTemplate_dic, conditionTemplate_Elem)
        resultTemplate = 'resultTemplate'  ##  >=0
        if resultTemplate in protocol_dic:
            if isinstance(protocol_dic[resultTemplate], list):
                resultTemplate_list = protocol_dic[resultTemplate]
            else:
                resultTemplate_list = [protocol_dic[resultTemplate]]
            for resultTemplate_dic in resultTemplate_list:
                resultTemplate_Elem = ET.SubElement(protocol_Elem, resultTemplate, attrib={'id':resultTemplate_dic['@id']})
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in resultTemplate_dic:
                    if rens.search(key):
                        resultTemplate_Elem.set(key[1:],resultTemplate_dic[key])
                ###########################################
                # templates contents
                self.writeTemplates(resultTemplate_dic, resultTemplate_Elem)


    ''' Data Contents の作成 '''
    def createdatacontents(self, data_dic, data_Elem):
        #print('create <data> contents')
        # global contents
        self.writeGlobalContents(data_dic, data_Elem)
        
        results = maimlelement.results   ## >=1
        if isinstance(data_dic[results], list):
            results_list = data_dic[results]
        else:
            results_list = [data_dic[results]]
        for results_dic in results_list:
            results_Elem = ET.SubElement(data_Elem, results, attrib={'id':results_dic['@id']})
            ###########################################
            # namespace
            rens = re.compile("@xmlns:.*")
            for key in results_dic:
                if rens.search(key):
                    results_Elem.set(key[1:],results_dic[key])
            ###########################################
            # global contents
            self.writeGlobalContents(results_dic, results_Elem)
            material = maimlelement.material     ## >=0
            ## instance contents
            self.writeInstanceData(results_dic, results_Elem, material)

            condition = maimlelement.condition     ## >=0
            ## instance contents
            self.writeInstanceData(results_dic, results_Elem, condition)

            result = maimlelement.result     ## >=0
            ## instance contents
            self.writeInstanceData(results_dic, results_Elem, result)


    ''' EventLog Contents の作成 '''
    def createeventlogcontents(self, eventlog_dic, eventlog_Elem):
        #print('create <eventLog> contents')
        # global contents
        self.writeGlobalContents(eventlog_dic, eventlog_Elem)
        log = 'log'   ##  >=1  参照付グローバル
        if isinstance(eventlog_dic[log], list):
            log_list = eventlog_dic[log]
        else:
            log_list = [eventlog_dic[log]]
        for log_dic in log_list:
            log_Elem = ET.SubElement(eventlog_Elem, log, attrib={'id':log_dic['@id'], 'ref':log_dic['@ref']})
            # global contents
            self.writeGlobalContents(log_dic, log_Elem)
            trace = 'trace'   ## >=1  参照付グローバル
            if isinstance(log_dic[trace], list):
                trace_list = log_dic[trace]
            else:
                trace_list = [log_dic[trace]]
            for trace_dic in trace_list:
                trace_Elem = ET.SubElement(log_Elem, trace, attrib={'id':trace_dic['@id'], 'ref':trace_dic['@ref']})
                # global contents
                self.writeGlobalContents(trace_dic, trace_Elem)
                event = 'event'   # >=1  参照付グローバル
                if isinstance(trace_dic[event], list):
                    event_list = trace_dic[event]
                else:
                    event_list = [trace_dic[event]]
                for event_dic in event_list:
                    event_Elem = ET.SubElement(trace_Elem, event, attrib={'id':event_dic['@id'], 'ref':event_dic['@ref']})
                    # global contents
                    self.writeGlobalContents(event_dic, event_Elem)
                    resultsRef = 'resultsRef'    # >=0  参照要素
                    if resultsRef in event_dic.keys():
                        if isinstance(event_dic[resultsRef], list):
                            resultsRef_list = event_dic[resultsRef]
                        else:
                            resultsRef_list = [event_dic[resultsRef]]
                        for resultsRef_dic in resultsRef_list:
                            # reference contents
                            self.writeReferenceContents(resultsRef_dic, event_Elem, resultsRef)
                    event_creatorRef = 'creatorRef'    # >=0  参照要素
                    if event_creatorRef in event_dic.keys():
                        if isinstance(event_dic[event_creatorRef], list):
                            event_creatorRef_list = event_dic[event_creatorRef]
                        else:
                            event_creatorRef_list = [event_dic[event_creatorRef]]
                        for event_creatorRef_dic in event_creatorRef_list:
                            # reference contents
                            self.writeReferenceContents(event_creatorRef_dic, event_Elem, event_creatorRef)
                    event_ownerRef = 'ownerRef'    # >=0  参照要素
                    if event_ownerRef in event_dic.keys():
                        if isinstance(event_dic[event_ownerRef], list):
                            event_ownerRef_list = event_dic[event_ownerRef]
                        else:
                            event_ownerRef_list = [event_dic[event_ownerRef]]
                        for event_ownerRef_dic in event_ownerRef_list:
                            # reference contents
                            self.writeReferenceContents(event_ownerRef_dic, event_Elem, event_ownerRef)
                trace_creatorRef = 'creatorRef'    # >=0  参照要素
                if trace_creatorRef in trace_dic.keys():
                    if isinstance(trace_dic[trace_creatorRef], list):
                        trace_creatorRef_list = trace_dic[trace_creatorRef]
                    else:
                        trace_creatorRef_list = [trace_dic[trace_creatorRef]]
                    for trace_creatorRef_dic in trace_creatorRef_list:
                        # reference contents
                        self.writeReferenceContents(trace_creatorRef_dic, trace_Elem, trace_creatorRef)
                trace_ownerRef = 'ownerRef'    # >=0  参照要素
                if trace_ownerRef in trace_dic.keys():
                    if isinstance(trace_dic[trace_ownerRef], list):
                        trace_ownerRef_list = trace_dic[trace_ownerRef]
                    else:
                        trace_ownerRef_list = [trace_dic[trace_ownerRef]]
                    for trace_ownerRef_dic in trace_ownerRef_list:
                        # reference contents
                        self.writeReferenceContents(trace_ownerRef_dic, trace_Elem, trace_ownerRef)
            log_creatorRef = 'creatorRef'    # >=0  参照要素
            if log_creatorRef in log_dic.keys():
                if isinstance(log_dic[log_creatorRef], list):
                    log_creatorRef_list = log_dic[log_creatorRef]
                else:
                    log_creatorRef_list = [log_dic[log_creatorRef]]
                for log_creatorRef_dic in log_creatorRef_list:
                    # reference contents
                    self.writeReferenceContents(log_creatorRef_dic, log_Elem, log_creatorRef)
            log_ownerRef = 'ownerRef'    # >=0  参照要素
            if log_ownerRef in log_dic.keys():
                if isinstance(log_dic[log_ownerRef], list):
                    log_ownerRef_list = log_dic[log_ownerRef]
                else:
                    log_ownerRef_list = [log_dic[log_ownerRef]]
                for log_ownerRef_dic in log_ownerRef_list:
                    # reference contents
                    self.writeReferenceContents(log_ownerRef_dic, log_Elem, log_ownerRef)

    ''' xmlを整形 '''
    def pretty_print(self, current, parent=None, index=-1, depth=0):
        for i, node in enumerate(current):
            self.pretty_print(node, current, i, depth + 1)
        if parent is not None:
            if index == 0:
                parent.text = '\n' + ('\t' * depth)
            else:
                parent[index - 1].tail = '\n' + ('\t' * depth)
            if index == len(parent) - 1:
                current.tail = '\n' + ('\t' * (depth - 1))
        

    ''' dict型オブジェクトから新たなmaimlファイルを作成'''
    def writecontents(self, maiml_dic, filepath):
        ## maiml root contents
        #maiml = 'maiml'
        ''' maimlの属性値を入れる '''
        maimlroot = ET.Element(maimlelement.maiml, attrib={'version':'1.0', 'features':'nested-attributes', 
                                         })
        if '@xmlns' in maiml_dic[maimlelement.maiml].keys():
            if isinstance(maiml_dic[maimlelement.maiml]['@xmlns'], list):
                maiml_ns_dic_list = maiml_dic[maimlelement.maiml]['@xmlns']
            else:
                maiml_ns_dic_list = [maiml_dic[maimlelement.maiml]['@xmlns']]
            for maiml_ns_dic in maiml_ns_dic_list:
                for key in maiml_ns_dic.keys():
                    setkey = 'xmlns'
                    if key == '':
                        pass
                    else:
                        setkey = setkey + ':' + key
                    maimlroot.set(setkey, maiml_ns_dic[key])
        
        ## document contents
        #document = 'document'
        document_dic = maiml_dic[maimlelement.maiml][maimlelement.document]
        document_Elem = ET.SubElement(maimlroot, maimlelement.document, attrib={'id':document_dic['@id']})
        ###########################################
        # namespace
        rens = re.compile("@xmlns:.*")
        for key in document_dic:
            if rens.search(key):
                document_Elem.set(key[1:],document_dic[key])
        ###########################################
        self.createdocumentcontents(document_dic, document_Elem)
        #print('writed <document> contents!')
        ## document_uuid = str(UUID.uuid4())
        ## protocol contents
        #protocol = 'protocol'
        protocol_dic = maiml_dic[maimlelement.maiml][maimlelement.protocol]
        protocol_Elem = ET.SubElement(maimlroot, maimlelement.protocol, attrib={'id':protocol_dic['@id']})
        ###########################################
        # namespace
        rens = re.compile("@xmlns:.*")
        for key in protocol_dic:
            if rens.search(key):
                protocol_Elem.set(key[1:],protocol_dic[key])
        ###########################################
        self.createprotocolcontents(protocol_dic, protocol_Elem)
        #print('writed <protocol> contents!')
        
        ## data & eventLog contents
        #data = 'data'
        #eventLog = 'eventLog'
        if maimlelement.data in maiml_dic[maimlelement.maiml].keys() and maimlelement.eventlog in maiml_dic[maimlelement.maiml].keys():
            ## data contents
            maimlroot.set('xsi:type','maimlRootType')
            data_dic = maiml_dic[maimlelement.maiml][maimlelement.data]
            data_Elem = ET.SubElement(maimlroot, maimlelement.data, attrib={'id':data_dic['@id']})
            ###########################################
            # namespace
            rens = re.compile("@xmlns:.*")
            for key in data_dic:
                if rens.search(key):
                    data_Elem.set(key[1:],data_dic[key])
            ###########################################
            self.createdatacontents(data_dic, data_Elem)
            #print('writed <data> contents!')

            ## eventlog contents
            #concept = 'concept'
            #lifecycle = 'lifecycle'
            #timeAttrib = 'time'
            eventlog_dic = maiml_dic[maimlelement.maiml][maimlelement.eventlog]
            eventlog_Elem = ET.SubElement(maimlroot, maimlelement.eventlog, attrib={'id':eventlog_dic['@id']})
            if '@xmlns' in eventlog_dic.keys():
                if isinstance(eventlog_dic['@xmlns'], list):
                    eventLog_ns_dic_list = eventlog_dic['@xmlns']
                else:
                    eventLog_ns_dic_list = [eventlog_dic['@xmlns']]
                for eventLog_ns_dic in eventLog_ns_dic_list:
                    if maimlelement.concept in eventLog_ns_dic.keys():
                        eventlog_Elem.set('xmlns:'+maimlelement.concept, eventLog_ns_dic[maimlelement.concept])
                    if maimlelement.lifecycle in eventLog_ns_dic.keys():
                        eventlog_Elem.set('xmlns:'+maimlelement.lifecycle, eventLog_ns_dic[maimlelement.lifecycle])
                    if maimlelement.timeAttrib in eventLog_ns_dic.keys():
                        eventlog_Elem.set('xmlns:'+maimlelement.timeAttrib, eventLog_ns_dic[maimlelement.timeAttrib])

            self.createeventlogcontents(eventlog_dic, eventlog_Elem)
            #print('writed <eventLog> contents!')
        else:
            maimlroot.set('xsi:type','protocolFileRootType')

        if filepath is None:
            print('Filepath of output is not found.')
        else:
            #文字列をそのまま扱えるが、改行、インデントがない
            maimltree = ET.ElementTree(maimlroot)
            self.pretty_print(maimltree.getroot())
            #print(maimltree)
            try:
                maimltree.write(filepath, encoding='utf-8', xml_declaration=True)
            except Exception as e:
                print(e)
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise e
        
        return filepath, maiml_dic[maimlelement.maiml][maimlelement.document][maimlelement.uuid]



if __name__ == '__main__':
    createmaiml = ReadWriteMaiML()
    dict_obj = createmaiml.readFile()
    createmaiml.writecontents(dict_obj)