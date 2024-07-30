'''
 yamlファイルからdocumentのコンテンツを取得
 
'''

import sys
import yaml
import pprint
import json
import codecs

data_dir = './DATA/'

'''
# rootがmaiml要素の場合の処理
try:
    with open( data_dir + 'input.yaml') as file:
        obj = yaml.safe_load(file)  # type(obj)) : dict

        maiml_obj = obj['maiml']  # type(maiml_obj)) : list
        for i in maiml_obj:
            key = i.keys()
            # print(key)
            if list(key)[0] == 'document':
                print('document::', i['document'])
            elif list(key)[0] == 'protocol':
                print('protocol::', i['protocol'])

except Exception as e:
    print('Exception occurred while loading YAML...', file=sys.stderr)
    print(e, file=sys.stderr)
    sys.exit(1)
'''

# rootがdocumentの場合の処理（データ取得のみ）
def getDocment():
    print('getDocument')
    try:
        with open( data_dir + 'input_document.yaml') as file:
            # yaml to dict
            obj = yaml.safe_load(file)  # type(obj)) : dict
            # dict to JSON
            pprint.pprint(json.dumps(obj))

            document_obj = obj['document']  # type(maiml_obj)) : list
            for i in document_obj:
                key = i.keys()
                #print(key)
                if list(key)[0] == 'uuid':
                    print('uuid::', i['uuid'])
                elif list(key)[0] == 'creator':
                    print('creator::', i['creator'])

    except Exception as e:
        print('Exception occurred while loading YAML...', file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

def getData():
    print('getData')


if __name__ == '__main__':
    # 実行時引数（1: document , 2: protocol）
    args = sys.argv
    if args[1] == '1':
        getDocment()
    elif args[1] == '2':
        getData()