'''
 ①xmlファイルをdict型オブジェクトに読み込む
 ②リスト型オブジェクトをcsvファイルに書き込む
'''

import csv
import glob
import xmltodict

maimlfiles = glob.glob('./XMLSample3/*')
fileNum = len(maimlfiles)
index = 0

HEADERS = ['key','description']
rows = []
rows2 = []

namespaces = { 
        'http://www.maiml.org/schemas': None,  # skip
        'http://www.example.com/maiml/material#' : 'exm' ,  # 'exm:で展開する'
}

# Read from maiml
for i in range(fileNum):
    maiml = maimlfiles[index]
    index += 1
    with open(maiml, 'r') as inF:
        maiml_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=namespaces)
        # OrderedDict:maiml_dicから取得したリストから一つずつ取り出し（OrderedDict:x）、dict型に変換（dict:dict(x)）し、リストにしてlist:protocol_listに格納している
        protocol_list = [dict(x) for x in maiml_dic['maiml']['protocol']['method']['program']['materialTemplate']['property']]
        #protocol_list.extend([dict(x) for x in maiml_dic['maiml']['protocol']['method']['program']['conditionTemplate']['property']])
        #protocol_list.extend([dict(x) for x in maiml_dic['maiml']['protocol']['method']['program']['resultTemplate']['property']])

        # to row data
        for data in protocol_list:
            #print(data)
            key = data['@key']
            if 'description' in data.keys():
                description = data['description']
            else:
                description = ""
            rows.append([key, description])

'''For 'data'contens by namespace  
        # 名前空間を使用してコンテンツを取得する
        data_list = []
        if 'data' in maiml_dic['maiml']:
            if 'property' in maiml_dic['maiml']['data']['results']['material']:
                data_list.extend(([dict(y) for y in maiml_dic['maiml']['data']['results']['material']['property']]))
            
            #この場合、戻り値の型が異なるので注意
            if 'exm:property' in maiml_dic['maiml']['data']['results']['material']:
                data_list.extend(([dict(y) for y in [maiml_dic['maiml']['data']['results']['material']['exm:property']]]))
            
        for data2 in data_list:
            #print(data2)
            if data2['@key'].startswith('exm:'): 
                key2 = data2['@key']
                print(key2)
                if 'description' in data2.keys():
                    description2 = data2['description']
                else:
                    description2 = ""
                rows2.append([key2, description2])
'''

# Write to CSV
with open('./csv/temp.csv', 'w', newline='') as outF:
    writer = csv.writer(outF)
    writer.writerow(HEADERS)
    writer.writerows(rows)

'''For 'data'contens by namespace
# Write to CSV
with open('./csv/temp_data.csv', 'w', newline='') as outF:
    writer = csv.writer(outF)
    writer.writerow(HEADERS)
    writer.writerows(rows2)
'''



''' 特定の名前空間でkey属性を絞る
import csv
import glob
import xmltodict

maimlfiles = glob.glob('./XMLSample2/*')
fileNum = len(maimlfiles)
index = 0

HEADERS = ['key','description']
rows = []

namespaces = { 
        'http://www.maiml.org/schemas': None,  # skip
        'http://www.example.com/maiml/material#' : 'exm' ,  # 'exm:で展開する'
}

# Read from maiml
for i in range(fileNum):
    maiml = maimlfiles[index]
    index += 1
    with open(maiml, 'r') as inF:
        maiml_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=namespaces)
        
        data_list = []
        if 'data' in maiml_dic['maiml']:
            if 'property' in maiml_dic['maiml']['data']['results']['material']:
                data_list.extend(([dict(y) for y in maiml_dic['maiml']['data']['results']['material']['property']]))

        # to row data
        for data2 in data_list:
            if data2['@key'].startswith('exm:'): 
                key2 = data2['@key']
                print(key2)
                if 'description' in data2.keys():
                    description2 = data2['description']
                else:
                    description2 = ""
                rows.append([key2, description2])

# Write to CSV
with open('./csv/temp.csv', 'w', newline='') as outF:
    writer = csv.writer(outF)
    writer.writerow(HEADERS)
    writer.writerows(rows)

'''



'''
        for x in maiml_dic['maiml']['protocol']['method']['program']['materialTemplate']['property']:
            print(x)
            #OrderedDict([('@http://www.w3.org/2001/XMLSchema-instance:type', 'stringType'), ('@key', 'exm:MaterialLotNo'), ('value', 'Lot No.'), 
                            ('property', OrderedDict([('@http://www.w3.org/2001/XMLSchema-instance:type', 'stringType'), ('@key', 'exm:LotNumber')]))])
            
            print(dict(x))
            
            #{'@http://www.w3.org/2001/XMLSchema-instance:type': 'stringType', '@key': 'exm:MaterialLotNo', 'value': 'Lot No.',
            #    'property': OrderedDict([('@http://www.w3.org/2001/XMLSchema-instance:type', 'stringType'), ('@key', 'exm:LotNumber')])}

            print([dict(x)])
            #[{'@http://www.w3.org/2001/XMLSchema-instance:type': 'stringType', '@key': 'exm:MaterialLotNo', 'value': 'Lot No.', 
            #    'property': OrderedDict([('@http://www.w3.org/2001/XMLSchema-instance:type', 'stringType'), ('@key', 'exm:LotNumber')])}]
'''
