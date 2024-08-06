'''
 ①xmlファイルをdict型オブジェクトに読み込む
 ②リスト型オブジェクトをcsvファイルに書き込む
'''
import csv
import glob
import xmltodict

## ディレクトリに存在するファイルをすべて取得
def readfiles():
    maimlfiles = glob.glob('./INPUT/*')
    fileNum = len(maimlfiles)
    index = 0
    namespaces = { 
            'http://www.maiml.org/schemas': None,  # skip
            'http://www.example.com/maiml/material#' : 'exm' ,  # 'exm:で展開する'
    }

    # Read from maiml directory
    for i in range(fileNum):
        maiml = maimlfiles[index]
        index += 1
        with open(maiml, 'r') as inF:
            maiml_dic = xmltodict.parse(inF.read(), process_namespaces=True, namespaces=namespaces)
    return maiml_dic


#### param  1 : dict型のmaimlデータ
def makecsv(maiml_dic):
    # maiml_dicから取得したリストから一つずつ取り出し、dict型に変換し、リストにしてprotocol_listに格納している
    protocol_list = [dict(x) for x in maiml_dic['maiml']['protocol']['method']['program']['materialTemplate']['property']]
    
    HEADERS = ['key','description']
    rows = []
    # to row data
    for data in protocol_list:
        key = data['@key']
        if 'description' in data.keys():
            description = data['description']
        else:
            description = ""
        rows.append([key, description])

    # Write to CSV
    with open('output.csv', 'w', newline='') as outF:
        writer = csv.writer(outF)
        writer.writerow(HEADERS)
        writer.writerows(rows)


'''
#For 'data'contens by namespace  
def makecsv2(maiml_dic):
    # 名前空間を使用してコンテンツを取得する
    data_list = []
    if 'data' in maiml_dic['maiml']:
        if 'property' in maiml_dic['maiml']['data']['results']['material']:
            data_list.extend(([dict(y) for y in maiml_dic['maiml']['data']['results']['material']['property']]))
        
        #この場合、戻り値の型が異なるので注意
        if 'exm:property' in maiml_dic['maiml']['data']['results']['material']:
            data_list.extend(([dict(y) for y in [maiml_dic['maiml']['data']['results']['material']['exm:property']]]))
    
    HEADERS = ['key','description']
    rows = []
    for data2 in data_list:
        #print(data2)
        if data2['@key'].startswith('exm:'): 
            key2 = data2['@key']
            print(key2)
            if 'description' in data2.keys():
                description2 = data2['description']
            else:
                description2 = ""
            rows.append([key2, description2])
    
    #For 'data'contens by namespace
    # Write to CSV
    with open('./csv/temp_data.csv', 'w', newline='') as outF:
        writer = csv.writer(outF)
        writer.writerow(HEADERS)
        writer.writerows(rows)
'''

''' 
#特定の名前空間でkey属性を絞る
def makecsv3():
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

if __name__ == "__main__":
    maimldict = readfiles()
    makecsv(maimldict)