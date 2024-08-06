import os,re
import xml.etree.ElementTree as ET
import glob, xmltodict

import uuid as UUID
from datetime import datetime as DT
from zoneinfo import ZoneInfo

TIME_ZONE = 'Asia/Tokyo'
class defaultNS():
    namespaces = { 
                'http://www.maiml.org/schemas': None,  # skip
                'http://www.w3.org/2001/XMLSchema-instance': 'xsi' , # 'xsi:で展開する'
               # 'http://www.example.com/maiml/material#' : 'exm' ,  # 'exm:で展開する'
    }

################################################
##   Read & Write MaiML file class
################################################
class ReadWriteMaiML:
    ''' Global contents    nomal=(True:グローバル要素/False:特定グローバル要素) '''
    def writeGlobalContents(self, mydic, parentET, nomal=True):
        #print('writeGlobalContents')
        uuid = 'uuid'
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
        childUri = 'childUri'     ## >=0
        if childUri in mydic.keys():
            if isinstance(mydic[childUri], list):
                childUri_list = mydic[childUri]
            else:
                childUri_list =[mydic[childUri]]
            for childUri_dic in childUri_list:
                global_childUri_Elem = ET.SubElement(parentET, childUri)
                global_childUri_Elem.text = childUri_dic
        childHash = 'childHash'     ## >=0
        if childHash in mydic.keys():
            if isinstance(mydic[childHash], list):
                childHash_list = mydic[childHash]
            else:
                childHash_list =[mydic[childHash]]
            for childHash_dic in childHash_list:
                global_childHash_Elem = ET.SubElement(parentET, childHash)
                global_childHash_Elem.text = childHash_dic
        childUuid = 'childUuid'     ##  >=0
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

        insertion = 'insertion'  ## >=0
        if insertion in mydic.keys():
            if isinstance(mydic[insertion], list):
                insertion_list = mydic[insertion]
            else:
                insertion_list =[mydic[insertion]]
            for insertion_dic in insertion_list:
                global_isnertion_Elem = ET.SubElement(parentET, insertion)
                insertion_uri = 'uri'  ## =1
                insertion_uri_Elem = ET.SubElement(global_isnertion_Elem, insertion_uri)
                insertion_uri_Elem.text = insertion_dic[insertion_uri]
                insertion_hash = 'hash'  ## =1
                insertion_hash_Elem = ET.SubElement(global_isnertion_Elem, insertion_hash)
                insertion_hash_Elem.text = insertion_dic[insertion_hash]
                '''if '@method' in insertion_dic[insertion_hash].keys():
                    insertion_hash_Elem.set('method', insertion_dic[insertion_hash]['@method'])
                    insertion_hash_Elem.text = insertion_dic[insertion_hash]['#text']
                else:
                    insertion_hash_Elem.text = insertion_dic[insertion_hash]
                '''
                insertion_uuid = 'uuid'   ## 0/1
                if insertion_uuid in insertion_dic.keys():
                    insertion_uuid_Elem = ET.SubElement(global_isnertion_Elem, insertion_uuid)
                    insertion_uuid_Elem.text = insertion_dic[insertion_uuid]
                insertion_format = 'format'   # 0/1
                if insertion_format in insertion_dic.keys():
                    insertion_format_Elem = ET.SubElement(global_isnertion_Elem, insertion_format)
                    insertion_format_Elem.text = insertion_dic[insertion_format]
        name = 'name'        
        if name in mydic.keys():   # 0/1
            p_name_dic = mydic[name]
            p_name_Elem = ET.SubElement(parentET, name)
            p_name_Elem.text = p_name_dic
        description = 'description'
        if description in mydic.keys():   # 0/1
            p_description_dic = mydic[description]
            p_description_Elem = ET.SubElement(parentET, description)
            p_description_Elem.text = p_description_dic
        annotation = 'annotation'
        if annotation in mydic.keys():    # 0/1
            p_annotation_dic = mydic[annotation]
            p_annotation_Elem = ET.SubElement(parentET, annotation)
            p_annotation_Elem.text = p_annotation_dic
        
        ###################################################################################
        ## 汎用データコンテナ
        generalTagList = ['property', 'content']
        ## property, content    >=0
        for generalTag in generalTagList:
            if generalTag in mydic.keys():
                if isinstance(mydic[generalTag], list):
                    property_list = mydic[generalTag]
                else:
                    property_list = [mydic[generalTag]]
                for property_nest in property_list:
                    self.writeGenericdataContainer(property_nest, parentET, generalTag)
        ################################################################################### 
        

    ''' 汎用データコンテナのネスト構造に対応 '''
    def writeGenericdataContainer(self, mydic, parentET, mytag):
        #print('writeGenericdataContainer')
        # set attrib
        my_Elem = ET.SubElement(parentET, mytag, attrib={'xsi:type':mydic['@xsi:type'], 'key':mydic['@key']})    # =1
        # set values  
        if '@formatString' in mydic.keys() and mydic['@formatString'] != '':    # 0/1
            my_Elem.set('formatString', mydic['@formatString'])
        if '@units' in mydic.keys() and mydic['@units'] != '':    # 0/1
            my_Elem.set('units', mydic['@units'])
        if '@scaleFactor' in mydic.keys() and mydic['@scaleFactor'] != '':    # 0/1
            my_Elem.set('scaleFactor', mydic['@scaleFactor'])
        
        ## content, uncertaintyが持つ属性
        if '@axis' in mydic.keys() and mydic['@axis'] != '':    # 0/1
            my_Elem.set('axis', mydic['@axis'])
        if '@size' in mydic.keys() and mydic['@size'] != '':    # 0/1
            my_Elem.set('size', mydic['@size'])
        if '@id' in mydic.keys() and mydic['@id'] != '':    # 0/1
            my_Elem.set('id', mydic['@id'])
        if '@ref' in mydic.keys() and mydic['@ref'] != '':    # 0/1
            my_Elem.set('ref', mydic['@ref'])

        childUri = 'childUri'   # >=0
        if childUri in mydic.keys():
            if isinstance(mydic[childUri], list):
                childUri_list = mydic[childUri]
            else:
                childUri_list = [mydic[childUri]]
            for childUri_dic in childUri_list:
                childUri_Elem = ET.SubElement(my_Elem, childUri)
                childUri_Elem.text = childUri_dic
        childHash = 'childHash'   # >=0
        if childHash in mydic.keys():
            if isinstance(mydic[childHash], list):
                childHash_list = mydic[childHash]
            else:
                childHash_list = [mydic[childHash]]
            for childHash_dic in childHash_list:
                childHash_Elem = ET.SubElement(my_Elem, childHash)
                childHash_Elem.text = childHash_dic
        childUuid = 'childUuid'   # >=0
        if childUuid in mydic.keys():
            if isinstance(mydic[childUuid], list):
                childUuid_list = mydic[childUuid]
            else:
                childUuid_list = [mydic[childUuid]]
            for childUuid_dic in childUuid_list:
                childUuid_Elem = ET.SubElement(my_Elem, childUuid)
                childUuid_Elem.text = childUuid_dic

        ##  EncryptedData  ## 0/1
        ################################
        ## EncryptedData(@xmlns':'http://www.w3.org/2001/04/xmlenc#)   0/1
        ################################
        description = 'description'
        if description in mydic.keys():    # 0/1
            my_Elem.set(description,mydic[description])
        value = 'value'  ## >=0
        if value in mydic.keys():    #  >=0
            if isinstance(mydic[value], list):
                valueList = mydic[value]
            else:
                valueList = [mydic[value]]
            for value_dic in valueList:
                value_Elem = ET.SubElement(my_Elem, value)
                value_Elem.text = value_dic
        ###############################
        ##  uncertainty    >=0
        ###############################
        ##  property, content  >=0
        if 'property' in mydic.keys():
            mytag = 'property'
            if isinstance(mydic['property'], list):
                for sinmydic in mydic['property']:
                    self.writeGenericdataContainer(sinmydic, my_Elem, mytag)
            else:
                a_mydic = mydic['property']
                a_mydic_ET = ET.SubElement(my_Elem, mytag, attrib={'xsi:type':a_mydic['@xsi:type'], 'key':a_mydic['@key']})    # =1
                if '@formatString' in a_mydic.keys():    # 0/1
                    a_mydic_ET.set('formatString', a_mydic['@formatString'])
                if '@units' in a_mydic.keys():    # 0/1
                    a_mydic_ET.set('units', a_mydic['@units'])
                if '@scaleFactor' in a_mydic.keys():    # 0/1
                    a_mydic_ET.set('scaleFactor', a_mydic['@scaleFactor'])
                childUri = 'childUri'   # >=0
                if childUri in a_mydic.keys():
                    if isinstance(a_mydic[childUri], list):
                        a_childUri_list = a_mydic[childUri]
                    else:
                        a_childUri_list = [a_mydic[childUri]]
                    for a_childUri_dic in a_childUri_list:
                        a_childUri_Elem = ET.SubElement(a_mydic_ET, childUri)
                        a_childUri_Elem.text = a_childUri_dic
                childHash = 'childHash'   # >=0
                if childHash in a_mydic.keys():
                    if isinstance(a_mydic[childHash], list):
                         a_childHash_list = a_mydic[childHash]
                    else:
                        a_childHash_list = [a_mydic[childHash]]
                    for a_childHash_dic in a_childHash_list:
                        a_childHash_Elem = ET.SubElement(a_mydic_ET, childHash)
                        a_childHash_Elem.text = a_childHash_dic
                childUuid = 'childUuid'   # >=0
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
                if 'description' in a_mydic.keys():    # 0/1
                    a_mydic_ET.set('description', a_mydic['@description'])
                ##  value  >=0
                if 'value' in a_mydic.keys():    #  >=0
                    if isinstance(a_mydic['value'], list):
                        valueList = a_mydic['value']
                    else:
                        valueList = [a_mydic['value']]
                    for value_dic in valueList:
                        value_Elem = ET.SubElement(a_mydic_ET, 'value')
                        value_Elem.text = value_dic
                        #print(value_dic)
                ###############################
                ##  uncertainty    >=0
                ###############################
                if 'property' in a_mydic.keys():
                    mytag = 'property'
                    if isinstance(a_mydic['property'], list):
                        for sinmydic in a_mydic['property']:
                            self.writeGenericdataContainer(sinmydic, a_mydic_ET, mytag)
                    else:
                        sinmydic = a_mydic['property']
                        #print(sinmydic['@key'],'　　何もしない')     # Debug用
                        self.writeGenericdataContainer(sinmydic, a_mydic_ET, mytag)
                if 'content' in a_mydic.keys():
                    mytag = 'content'
                    if isinstance(a_mydic['content'], list):
                        for sinmydic in a_mydic['content']:
                            self.writeGenericdataContainer(sinmydic, a_mydic_ET, mytag)
                    else:
                        sinmydic = a_mydic['content']
                        self.writeGenericdataContainer(sinmydic, a_mydic_ET, mytag)
        if 'content' in mydic.keys():
            mytag = 'content'
            if isinstance(mydic['content'], list):
                for sinmydic in mydic['content']:
                    self.writeGenericdataContainer(sinmydic, my_Elem, mytag)
            else:
                b_mydic = mydic['content']
                b_mydic_ET = ET.SubElement(my_Elem, mytag, attrib={'xsi:type':b_mydic['@xsi:type'], 'key':b_mydic['@key']})    # =1
                if '@formatString' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('formatString', b_mydic['@formatString'])
                if '@units' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('units', b_mydic['@units'])
                if '@scaleFactor' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('scaleFactor', b_mydic['@scaleFactor'])
                ## content, uncertaintyが持つ属性
                if '@axis' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('axis', b_mydic['@axis'])
                if '@size' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('size', b_mydic['@size'])
                if '@id' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('id', b_mydic['@id'])
                if '@ref' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('ref', b_mydic['@ref'])

                childUri = 'childUri'   # >=0
                if childUri in b_mydic.keys():
                    if isinstance(b_mydic[childUri], list):
                        b_childUri_list = b_mydic[childUri]
                    else:
                        b_childUri_list = [b_mydic[childUri]]
                    for b_childUri_dic in b_childUri_list:
                        b_childUri_Elem = ET.SubElement(b_mydic_ET, childUri)
                        b_childUri_Elem.text = b_childUri_dic
                childHash = 'childHash'   # >=0
                if childHash in b_mydic.keys():
                    if isinstance(b_mydic[childHash], list):
                         b_childHash_list = b_mydic[childHash]
                    else:
                        b_childHash_list = [b_mydic[childHash]]
                    for b_childHash_dic in b_childHash_list:
                        b_childHash_Elem = ET.SubElement(b_mydic_ET, childHash)
                        b_childHash_Elem.text = b_childHash_dic
                childUuid = 'childUuid'   # >=0
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
                if 'description' in b_mydic.keys():    # 0/1
                    b_mydic_ET.set('description', b_mydic['@description'])
                ##  value  >=0
                if 'value' in b_mydic.keys():    #  >=0
                    if isinstance(b_mydic['value'], list):
                        valueList = b_mydic['value']
                    else:
                        valueList = [b_mydic['value']]
                    for value_dic in valueList:
                        value_Elem = ET.SubElement(b_mydic_ET, 'value')
                        value_Elem.text = value_dic
                ###############################
                ##  uncertainty    >=0
                ###############################
                ##  property, content  >=0
                if 'property' in b_mydic.keys():
                    mytag = 'property'
                    if isinstance(b_mydic['property'], list):
                        for sinmydic in b_mydic['property']:
                            self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)
                    else:
                        sinmydic = b_mydic['property']
                        self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)
                if 'content' in b_mydic.keys():
                    mytag = 'content'
                    if isinstance(b_mydic['content'], list):
                        for sinmydic in b_mydic['content']:
                            self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)
                    else:
                        sinmydic = b_mydic['content']
                        self.writeGenericdataContainer(sinmydic, b_mydic_ET, mytag)


    ''' TEMPLATESの作成 '''
    def writeTemplates(self, mydic, parentET):
        #print('writeTemplates')
        ## global contents
        self.writeGlobalContents(mydic, parentET)

        ## placeRef      >=1  参照要素
        if isinstance(mydic['placeRef'], list):
            p_placeRef_list = mydic['placeRef']
        else:
            p_placeRef_list = [mydic['placeRef']]
        for p_placeRef_dic in p_placeRef_list:
            p_placeRef_Elem = ET.SubElement(parentET, 'placeRef', attrib={'id':p_placeRef_dic['@id'], 'ref':p_placeRef_dic['@ref']})
            if 'name' in p_placeRef_dic.keys():   # 0/1
                p_placeRef_name_dic = p_placeRef_dic['name']
                p_placeRef_name_Elem = ET.SubElement(p_placeRef_Elem, 'name')
                p_placeRef_name_Elem.text = p_placeRef_name_dic
            if 'description' in p_placeRef_dic.keys():   # 0/1
                p_placeRef_description_dic = p_placeRef_dic['description']
                p_placeRef_description_Elem = ET.SubElement(p_placeRef_Elem, 'description')
                p_placeRef_description_Elem.text = p_placeRef_description_dic
        ## templateRef      >=0
        if 'templateRef' in mydic.keys():
            if isinstance(mydic['templateRef'], list):
                p_templateRef_list = mydic['templateRef']
            else:
                p_templateRef_list = [mydic['templateRef']]
            for p_templateRef_dic in p_templateRef_list:
                p_templateRef_Elem = ET.SubElement(parentET, 'templateRef', attrib={'id':p_templateRef_dic['@id'], 'ref':p_templateRef_dic['@ref']})
                if 'name' in p_templateRef_dic.keys():   # 0/1
                    p_templateRef_name_dic = p_templateRef_dic['name']
                    p_templateRef_name_Elem = ET.SubElement(p_templateRef_Elem, 'name')
                    p_templateRef_name_Elem.text = p_templateRef_name_dic
                if 'description' in p_templateRef_dic.keys():   # 0/1
                    p_templateRef_description_dic = p_templateRef_dic['description']
                    p_templateRef_description_Elem = ET.SubElement(p_templateRef_Elem, 'description')
                    p_templateRef_description_Elem.text = p_templateRef_description_dic
        

    ''' INSTANCEの作成 '''
    def writeInstanceData(self, results_dic, results_Elem, mytag):
        #print('writeInstanceData')
        if mytag in results_dic.keys():
            if isinstance(results_dic[mytag], list):
                mytag_list = results_dic[mytag]
            else:
                mytag_list = [results_dic[mytag]]
            for mytag_dic in mytag_list:
                mytag_Elem = ET.SubElement(results_Elem, mytag, attrib={'id':mytag_dic['@id'], 'ref':mytag_dic['@ref']})
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in mytag_dic:
                    if rens.search(key):
                        mytag_Elem.set(key[1:],mytag_dic[key])
                ###########################################
                #global contents
                self.writeGlobalContents(mytag_dic, mytag_Elem)
                instanceRef = 'instanceRef'    # >=0  参照要素
                if instanceRef in mytag_dic.keys():
                    if isinstance(mytag_dic[instanceRef], list):
                        mytag_instanceRef_list = mytag_dic[instanceRef]
                    else:
                        mytag_instanceRef_list = [mytag_dic[instanceRef]]
                    for mytag_instanceRef_dic in mytag_instanceRef_list:
                        mytag_instanceRef_Elem = ET.SubElement(mytag_Elem, instanceRef, attrib={'id':mytag_instanceRef_dic['@id'],'ref':mytag_instanceRef_dic['@ref']})
                        ###########################################
                        # namespace
                        rens = re.compile("@xmlns:.*")
                        for key in mytag_instanceRef_dic:
                            if rens.search(key):
                                mytag_instanceRef_Elem.set(key[1:],mytag_instanceRef_dic[key])
                        ###########################################
                        isinstanceRef_name = 'name'   # 0/1
                        if isinstanceRef_name in mytag_instanceRef_dic.keys():
                            mytag_instanceRef_name_Elem = ET.SubElement(mytag_instanceRef_Elem, isinstanceRef_name)
                            mytag_instanceRef_name_Elem.text = mytag_instanceRef_dic[isinstanceRef_name]
                        isinstanceRef_description = 'description'   # 0/1
                        if isinstanceRef_description in mytag_instanceRef_dic.keys():
                            mytag_instanceRef_description_Elem = ET.SubElement(mytag_instanceRef_Elem, isinstanceRef_description)
                            mytag_instanceRef_description_Elem.text = mytag_instanceRef_dic[isinstanceRef_description]


    ''' chain要素のネスト構造に対応 '''  ## 未テスト
    def writeChainContents(self, mydic, parentET):
        ## global contents 特定グローバル要素
        self.writeGlobalContents(mydic, parentET)
        chain_hash = 'hash'   ## =1
        chain_hash_Elem = ET.SubElement(parentET, chain_hash)
        chain_hash_Elem.text = mydic[chain_hash]
        chain = 'chain'  ## >=0
        if chain in mydic.keys():
            if isinstance(mydic[chain], list):
                chain_chain_list = mydic[chain]
            else:
                chain_chain_list = [mydic[chain]]
            for chain_chain_dic in chain_chain_list:
                child_chain_Elem = ET.SubElement(parentET, chain)
                if '@id' in chain_chain_dic.keys():
                    child_chain_Elem.set('id',chain_chain_dic['@id'])
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
        parentT_hash = 'hash'   ## =1
        parentT_hash_Elem = ET.SubElement(parentET, parentT_hash)
        parentT_hash_Elem.text = mydic[parentT_hash]
        parentT = 'parent'  ## >=0
        if parentT in mydic.keys():
            if isinstance(mydic[parentT], list):
                parent_parent_list = mydic[parentT]
            else:
                parent_parent_list = [mydic[parentT]]
            for parent_parent_dic in parent_parent_list:
                child_parent_Elem = ET.SubElement(parentET, parentT)
                if '@id' in parent_parent_dic.keys():
                    child_parent_Elem.set('id',parent_parent_dic['@id'])
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
        mytag_Elem = ET.SubElement(parentET, mytag, attrib={'id':mydic['@id'], 'ref':mydic['@ref']})
        mytag_name = 'name'
        if mytag_name in mydic.keys():
            resultsRef_name_Elem = ET.SubElement(mytag_Elem, mytag_name)
            resultsRef_name_Elem.text = mydic[mytag_name]
        mytag_description = 'description'
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
            with open(maiml, 'r') as inF:
                maiml_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=defaultNS.namespaces)
                return maiml_dic

    ''' １ファイル読み込み '''
    def readFile(self, filepath):
        if filepath is None:
            maimlfile = '/test/input_data/SEMDataSample.maiml'
        else:
            maimlfile = filepath
        with open(maimlfile, 'r') as inF:
            maiml_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=defaultNS.namespaces)
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
        
        tz = ZoneInfo(key=TIME_ZONE)
        nowtimestamp = DT.now(tz)
        create_date = nowtimestamp.strftime('%Y-%m-%dT%H:%M:%S') + nowtimestamp.strftime('%z')[:3] + ':' + nowtimestamp.strftime('%z')[3:]
        date_Elem.text = create_date

        chain = 'chain'   ## >=0 
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

        parent = 'parent'   ## >=0 
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
        
        method = 'method'  ##contents   # >=1
        if isinstance(protocol_dic[method], list):
            method_list = protocol_dic[method]
        else:
            method_list = [protocol_dic[method]]
        for method_dic in method_list:
            #print(dict(method_dic))
            method_Elem = ET.SubElement(protocol_Elem, method, attrib={'id':method_dic['@id']})    # =1
            ###########################################
            # namespace
            rens = re.compile("@xmlns:.*")
            for key in method_dic:
                if rens.search(key):
                    method_Elem.set(key[1:],method_dic[key])
            ###########################################
            ## global contents
            self.writeGlobalContents(method_dic, method_Elem)
            
            pnml = 'pnml'  ##  >=1
            if isinstance(method_dic[pnml], list):
                pnml_list = method_dic[pnml]
            else:
                pnml_list = [method_dic[pnml]]
            for pnml_dic in pnml_list:    # >=1
                pnml_Elem = ET.SubElement(method_Elem, pnml, attrib={'id':pnml_dic['@id']})   # =1
                ###########################################
                # namespace
                rens = re.compile("@xmlns:.*")
                for key in pnml_dic:
                    if rens.search(key):
                        pnml_Elem.set(key[1:],pnml_dic[key])
                ###########################################
                ## global contents
                self.writeGlobalContents(pnml_dic, pnml_Elem)

                place = 'place'    # >=1
                if isinstance(pnml_dic[place], list):
                    place_list = pnml_dic[place]
                else:
                    place_list = [pnml_dic[place]]
                for place_dic in place_list:    # >=1
                    place_Elem = ET.SubElement(pnml_Elem, place, attrib={'id':place_dic['@id']})
                    #place_Elem.text = place_dic['#text']
                    name = 'name'
                    if name in place_dic.keys():   # 0/1
                        place_name_dic = place_dic[name]
                        place_name_Elem = ET.SubElement(place_Elem, name)
                        place_name_Elem.text = place_name_dic
                    description = 'description'
                    if description in place_dic.keys():   # 0/1
                        place_description_dic = place_dic[description]
                        place_description_Elem = ET.SubElement(place_Elem, description)
                        place_description_Elem.text = place_description_dic
                transition = 'transition'    # >=1
                if isinstance(pnml_dic[transition], list):
                    transition_list = pnml_dic[transition]
                else:
                    transition_list = [pnml_dic[transition]]
                for transition_dic in transition_list:    # >=1
                    transition_Elem = ET.SubElement(pnml_Elem, transition, attrib={'id':transition_dic['@id']})
                    #transition_Elem.text = transition_dic[#text]
                    #transition_name = 'name'
                    if name in transition_dic.keys():   # 0/1
                        transition_name_dic = transition_dic[name]
                        transition_name_Elem = ET.SubElement(transition_Elem, name)
                        transition_name_Elem.text = transition_name_dic
                    #transition_description = 'description'
                    if description in transition_dic.keys():   # 0/1
                        transition_description_dic = transition_dic[description]
                        transition_description_Elem = ET.SubElement(transition_Elem, description)
                        transition_description_Elem.text = transition_description_dic
                arc = 'arc'    # >=1
                if isinstance(pnml_dic[arc], list):
                    arc_list = pnml_dic[arc]
                else:
                    arc_list = [pnml_dic[arc]]
                for arc_dic in arc_list:    # >=1
                    arc_Elem = ET.SubElement(pnml_Elem, arc, attrib={'id':arc_dic['@id'], 'source':arc_dic['@source'], 'target':arc_dic['@target']})
                    name = 'name'
                    if name in arc_dic.keys():   # 0/1
                        arc_name_dic = arc_dic[name]
                        arc_name_Elem = ET.SubElement(arc_Elem, name)
                        arc_name_Elem.text = arc_name_dic
                    description = 'description'
                    if description in arc_dic.keys():   # 0/1
                        arc_description_dic = arc_dic[description]
                        arc_description_Elem = ET.SubElement(arc_Elem, description)
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

        results = 'results'   ## >=1
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

            material = 'material'     ## >=0
            ## instance contents
            self.writeInstanceData(results_dic, results_Elem, material)

            condition = 'condition'     ## >=0
            ## instance contents
            self.writeInstanceData(results_dic, results_Elem, condition)

            result = 'result'     ## >=0
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
        maiml = 'maiml'
        uuid = 'uuid'
        ''' maimlの属性値を入れる '''
        maimlroot = ET.Element(maiml, attrib={'version':'1.0', 'features':'nested-attributes', 
                                         })
        if '@xmlns' in maiml_dic[maiml].keys():
            if isinstance(maiml_dic[maiml]['@xmlns'], list):
                maiml_ns_dic_list = maiml_dic[maiml]['@xmlns']
            else:
                maiml_ns_dic_list = [maiml_dic[maiml]['@xmlns']]
            for maiml_ns_dic in maiml_ns_dic_list:
                for key in maiml_ns_dic.keys():
                    setkey = 'xmlns'
                    if key == '':
                        pass
                    else:
                        setkey = setkey + ':' + key
                    maimlroot.set(setkey, maiml_ns_dic[key])
        
        ## document contents
        document = 'document'
        document_dic = maiml_dic[maiml][document]
        document_Elem = ET.SubElement(maimlroot, document, attrib={'id':document_dic['@id']})
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
        protocol = 'protocol'
        protocol_dic = maiml_dic[maiml][protocol]
        protocol_Elem = ET.SubElement(maimlroot, protocol, attrib={'id':protocol_dic['@id']})
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
        data = 'data'
        eventLog = 'eventLog'
        if data in maiml_dic[maiml].keys() and eventLog in maiml_dic[maiml].keys():
            ## data contents
            maimlroot.set('xsi:type','maimlRootType')
            data_dic = maiml_dic[maiml][data]
            data_Elem = ET.SubElement(maimlroot, data, attrib={'id':data_dic['@id']})
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
            concept = 'concept'
            lifecycle = 'lifecycle'
            timeAttrib = 'time'
            eventlog_dic = maiml_dic[maiml][eventLog]
            eventlog_Elem = ET.SubElement(maimlroot, eventLog, attrib={'id':eventlog_dic['@id']})
            if '@xmlns' in eventlog_dic.keys():
                if isinstance(eventlog_dic['@xmlns'], list):
                    eventLog_ns_dic_list = eventlog_dic['@xmlns']
                else:
                    eventLog_ns_dic_list = [eventlog_dic['@xmlns']]
                for eventLog_ns_dic in eventLog_ns_dic_list:
                    if concept in eventLog_ns_dic.keys():
                        eventlog_Elem.set('xmlns:'+concept, eventLog_ns_dic[concept])
                    if lifecycle in eventLog_ns_dic.keys():
                        eventlog_Elem.set('xmlns:'+lifecycle, eventLog_ns_dic[lifecycle])
                    if timeAttrib in eventLog_ns_dic.keys():
                        eventlog_Elem.set('xmlns:'+timeAttrib, eventLog_ns_dic[timeAttrib])

            self.createeventlogcontents(eventlog_dic, eventlog_Elem)
            #print('writed <eventLog> contents!')
        else:
            maimlroot.set('xsi:type','protocolFileRootType')

        if filepath is None:
            print('Filepath of putput is not found.')
        else:
            #文字列をそのまま扱えるが、改行、インデントがない
            maimltree = ET.ElementTree(maimlroot)
            self.pretty_print(maimltree.getroot())
            #print(maimltree)
            maimltree.write(filepath, encoding='utf-8', xml_declaration=True)
        
        return filepath, maiml_dic[maiml][document][uuid]


if __name__ == '__main__':
    createmaiml = ReadWriteMaiML()
    dict_obj = createmaiml.readFile()
    filepath = './output.maiml'
    createmaiml.writecontents(dict_obj, filepath)