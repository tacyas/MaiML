import os, sys, re
import copy,hashlib,mimetypes
import uuid as UUID
import pandas as pd
from pathlib import Path
from Utils.staticClass import maimlelement, settings
from Utils.createMaiMLFile import  ReadWriteMaiML, UpdateMaiML


################################################
## FILE DIR PATH 
################################################
class filepath:
    cur_file = __file__  #このファイルのパス
    codedir = os.path.dirname(cur_file) + '/'
    rootdir = os.path.abspath(os.path.join(codedir, os.pardir)) + '/'
    input_dir = codedir + 'INPUT/'
    output_dir = codedir + 'OUTPUT/'
    
### excelの日付データのフォーマットを変換 ###################################
## YYYY-MM-DDTHH:MM:SS-xx:xx #########
def changeTimeFormat(e_datetime):
    #print(e_datetime) #2024/3/5 9:03
    e_datetime = pd.to_datetime(e_datetime)
    #print(e_datetime) # 2024-03-05 09:03:00
    #TIME_ZONE = 'Asia/Tokyo'
    TIME_ZONE = settings.TIME_ZONE
    e_datetime = e_datetime.tz_localize(TIME_ZONE)
    # 日時を 'YYYY-MM-DDTHH:MM:SS' フォーマットに変換
    datetime_str = e_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    # タイムゾーンオフセットを取得してフォーマットする
    offset = e_datetime.strftime('%z')
    formatted_offset = offset[:3] + ':' + offset[3:]  # '+09:00'
    # 日付とタイムゾーンオフセットを合体
    datetime = f'{datetime_str}{formatted_offset}'
    #print(datetime) # 2024-03-05T09:03:00-09:00
    return datetime


### エクセルの文字列指定'をフォーマット #################################################
def formatter_dash(value):
    if value == 'nan': ## エクセルの値が空白の場合（エラーとはしない）
        return ''
    return value.lstrip("'")


### valueの数値をフォーマット #################################################
def formatter_num(format_string, number):
    if number == '':
        return number
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


### insertionコンテンツを作成 #################################################
def makeInsertion(value, otherspath):
    filename = str(value)
    file_path = otherspath / filename
    # formatの取得
    extension = os.path.splitext(filename)[1]
    mime_type=''
    hash_sha256 = ''
    mimetypes.init()
    try:
        mime_type = mimetypes.types_map[extension]
    except Exception as e:
        print("insertion file's mime_type is not exist.: ",e)
        mime_type = 'none'
    try:
        with open(file_path, 'rb') as f:
            hash_sha256 = hashlib.sha256()
            while chunk := f.read(8192):  # 8KBごとにファイルを読み込む
                hash_sha256.update(chunk) 
            hash_sha256 = hash_sha256.hexdigest()
    except FileNotFoundError:
        print("insertion file's name '" + filename + "' does not exist.")
    except Exception as e:
        raise e
    insertion_dict = {
        maimlelement.uri:'./'+ filename,
        maimlelement.hash:str(hash_sha256),
        maimlelement.format:mime_type
        } 
    return insertion_dict


### propertyのコンテンツを作成 #################################################
def makeProperty(propertylist,key,value):
    #propertylist = instancedict[maimlelement.property]
    for propertydict in propertylist:
        if propertydict[maimlelement.keyd] == key:
            ## excel特有の文字列前の'を削除
            value = formatter_dash(str(value))
            if maimlelement.formatStringd in propertydict:
                propertydict[maimlelement.value] = formatter_num(propertydict[maimlelement.formatStringd], value)
            else:
                propertydict[maimlelement.value] = value
            return propertylist
        else:
            pass
        if maimlelement.property in propertydict.keys():
            propertylist2 = propertydict[maimlelement.property] if isinstance(propertydict[maimlelement.property],list) else [propertydict[maimlelement.property]]
            propertylist = makeProperty(propertylist2,key,value) 
    return propertylist


def main(maimlpath, exfilepath, otherspath):
    ## 1. MaiML
    ### 1-1. 読み込む
    readWriteMaiML = ReadWriteMaiML()
    maimldict = readWriteMaiML.readFile(maimlpath)
    
    ### 1-2. maimlのprotocolからdata,eventLogの仮データを作成
    updateMaiML = UpdateMaiML()
    fullmaimldict = updateMaiML.createFullMaimlDict(maimldict) 
    
    ### 1-3. 計測データを書き出すための準備
    #### 1-3-1. results実データ作成の準備
    resultsdict__ = fullmaimldict[maimlelement.maiml][maimlelement.data].pop(maimlelement.results)
    resultslist = []
    
    ### 1-4. methodのIDを取得
    methoddict_ = maimldict[maimlelement.maiml][maimlelement.protocol][maimlelement.method]
    methodIDlist = methoddict_ if isinstance(methoddict_,list) else [methoddict_]
    
    for methoddict in methodIDlist:
        instprogIDdict__ = {}
        '''
            instprogIDdict = {'instructionID':{
                'programID':'',
                'methodID':'',
                },}
        '''
        programIDdict ={}
        '''
                programIDdict=['programID' : {
                    'instlist':[{
                                'insID':'',
                                'column':''}],
                    'tracedict':{}
                },]'''
        ### 1-5. methoddictに含まれるinstructionのIDを取得し、instructionIDlistリストを作成
        programlist = methoddict[maimlelement.program] if isinstance(methoddict[maimlelement.program],list) else [methoddict[maimlelement.program]]
        for programdict in programlist:
            instructionlist = programdict[maimlelement.instruction] if isinstance(programdict[maimlelement.instruction],list) else [programdict[maimlelement.instruction]]
            for instructiondict in instructionlist:
                instprogIDdict__.update({
                    instructiondict[maimlelement.idd]:{
                    'programID':programdict[maimlelement.idd],
                    #'methodID':methoddict[maimlelement.idd],
                }})
        
        ## 2. エクセルを読み込む
        df = pd.read_excel(exfilepath, sheet_name=methoddict[maimlelement.idd], header=None)
        ### 2-1. 1行目と2行目のデータを取り出しておく(テンプレートのID、キー)
        ### 2-1-1. 1行目のデータ
        row1_1 = df.iloc[0]
        
        templateIDdict = {}
        '''
            templateIDdict = {
                'templateID1':[列番号のリスト],
                'templateID2':[列番号のリスト],
                }
        '''
        row1 = row1_1[1:]
        for index in row1.index:
            if pd.notna(row1[index]):
                ## instruction or template
                if row1[index] in instprogIDdict__.keys():
                    #instructionIDlist += row1[index]
                    '''
                    instructionlist=
                    {'instructionID1': {'programID': 'programIDtest2'}, 
                     'instructionID2': {'programID': 'programIDtest2'}}
                    '''
                    programID = instprogIDdict__[row1[index]]['programID']
                    if programID in programIDdict.keys():
                        programIDdict[programID]['instlist'].append({'insID':row1[index], 'column':index})
                    else:
                        programIDdict[programID]={
                                    'instlist':[{
                                                'insID':row1[index],
                                                'column':index}],
                                }
                elif templateIDdict and row1[index] in templateIDdict.keys(): # 該当キー（templateのID）に値（index）を追加
                    if isinstance(templateIDdict[row1[index]],list):
                        templateIDdict[row1[index]].append(index)
                    else:
                        templateIDdict[row1[index]] = [index]
                else: # キーと値を追加
                    templateIDdict.update({row1[index]:[index]})
         
        #### 1-3-2. trace実データ作成の準備
        logdict_ = fullmaimldict[maimlelement.maiml][maimlelement.eventlog][maimlelement.log]
        loglist = logdict_ if isinstance(logdict_,list) else [logdict_]
        tracelist__ = []
        for logdict in loglist:
            if(logdict[maimlelement.refd] == methoddict[maimlelement.idd]):
                tracelist__ = logdict.pop(maimlelement.trace)
                tracelist__ = tracelist__ if isinstance(tracelist__,list) else [tracelist__]
                for tracedict1 in tracelist__:
                    if tracedict1[maimlelement.refd] in programIDdict.keys():                    
                        programIDdict[tracedict1[maimlelement.refd]].update({'tracedict':copy.deepcopy(tracedict1)})
                    else:
                        pass
                    
        ### 2-1-2. 2行目のデータ
        row2 = df.iloc[1]
        
        ### 2-2. 3行目以降のデータをMaiMLデータに変換
        df_rest = df.iloc[2:]
        ### 2-2-1. 3行目以降のデータ１行ごとにreaults,traceを作成する
        tracelist = []                    
        for row3 in df_rest.itertuples(index=True):
            #### 2-2-1-1. results
            resultsdict = copy.deepcopy(resultsdict__)
            resultsdict[maimlelement.idd] = str(row3[1])
            resultsdict[maimlelement.uuid] = str(UUID.uuid4())
            instancedictlist = []
            instancedictlist.extend(resultsdict[maimlelement.material] if isinstance(resultsdict[maimlelement.material],list) else [resultsdict[maimlelement.material]])
            instancedictlist.extend(resultsdict[maimlelement.condition] if isinstance(resultsdict[maimlelement.condition],list) else [resultsdict[maimlelement.condition]])
            instancedictlist.extend(resultsdict[maimlelement.result] if isinstance(resultsdict[maimlelement.result],list) else [resultsdict[maimlelement.result]])
            
            for id, i_list in templateIDdict.items(): ## エクセルから取得したtemplateIDの数分繰り返し処理
                templateID = id
                instanceID = templateID + '_instance'
                instancedict = next((item for item in instancedictlist if item[maimlelement.idd] == instanceID), None)
                instancedict[maimlelement.uuid] = str(UUID.uuid4())
                instancedict[maimlelement.idd] = instancedict[maimlelement.idd] + str(row3.Index)
                if instancedict: ## エクセルから取得したinstanceIDがmaimlファイルに存在する場合
                    #propertyのvalueを上書き
                    propertylist = instancedict[maimlelement.property] if isinstance(instancedict[maimlelement.property],list) else [instancedict[maimlelement.property]]
                    for id_index in i_list: ## keyの数分popertyにvalueを追加する
                        key = row2[id_index]
                        value = row3[id_index+1]
                        if key == 'INSERTION':
                            if pd.notna(value):
                                insertiondict = makeInsertion(value, otherspath)
                                instancedict[maimlelement.insertion] = insertiondict
                            else:
                                pass
                        else:
                            propertylist = makeProperty(propertylist,key,value)
                else:
                    print(templateID + " does not exist.")     
            resultslist.append(resultsdict)
            
            ### 2-2-1-1. trace
            # エクセルの３行目以降、1行ごとにtraceを作成する
            '''
            programIDdict='progranID':{
                'instlist':[{
                            'insID':'',
                            'column':''}],
                'tracedict':{}
            }
            '''
            for program_ID, insttracedict in programIDdict.items():
                tracedict_ = copy.deepcopy(insttracedict['tracedict'])
                instructionIDlist = insttracedict['instlist']
                eventlist_ = []
                eventpoplist = []
                for instructionIDdict in instructionIDlist:
                    ## instructionIDを参照しているeventを更新
                    ## エクセル３行目のcolumnの値列の値（DATATIME）をMaiMLのフォーマットに変換
                    dateindex = instructionIDdict['column']+1
                    if pd.notna(row3[dateindex]):
                        datetime = str(changeTimeFormat(row3[dateindex]))
                    else:
                        datetime = ''
                    eventlist_ = tracedict_[maimlelement.event]
                    for eindex, eventdict_ in enumerate(eventlist_):
                        if eventdict_[maimlelement.refd] == instructionIDdict['insID']:
                            eventdict_[maimlelement.idd] = eventdict_[maimlelement.idd] + str(row3.Index)
                            eventdict_[maimlelement.uuid] = str(UUID.uuid4())
                            eventdict_[maimlelement.resultsRef] = {
                                                                    maimlelement.idd:eventdict_[maimlelement.idd]+'_resultref'+str(row3.Index), 
                                                                    maimlelement.refd:resultsdict[maimlelement.idd]
                                                                }
                            #eventpoplist.append(eventdict_[maimlelement.idd]) ## 追加したeventのIDリスト
                            propertylist = eventdict_[maimlelement.property] # 必ずlist
                            for propertydict in propertylist:
                                if propertydict[maimlelement.keyd] == maimlelement.time and datetime != '':
                                    propertydict[maimlelement.value] = datetime
                                    eventpoplist.append(eventdict_[maimlelement.idd]) ## 追加したeventのIDリスト
                                else:
                                    pass
                        else:
                            pass
                ## エクセルに存在しないINSTRUCTIONに対応するeventは消してしまう
                if eventpoplist :
                    for eindex2, eventdict2_ in enumerate(eventlist_):
                        if eventdict2_[maimlelement.idd] in eventpoplist:
                            pass
                        else:
                            del eventlist_[eindex2]
                    tracedict_[maimlelement.idd] = tracedict_[maimlelement.idd] + str(row3.Index)
                    tracedict_[maimlelement.uuid] = str(UUID.uuid4())
                    tracelist.append(tracedict_)
                else :
                    pass
                
        ## fulllmaimldictのlog[ref=methodID]のtracelistを、作成したtracelistで置き換える
        for logdict in loglist:
            if(logdict[maimlelement.refd] == methoddict[maimlelement.idd]):
                logdict[maimlelement.trace] = tracelist
                
        ## fullmaimldict[results]を、作成したresultslistで置き換える
        fullmaimldict[maimlelement.maiml][maimlelement.data][maimlelement.results] = resultslist
    
    ## outputファイルを保存
    try:
        outmaimlpath = './OUTPUT/output.maiml'
        path, duuid = readWriteMaiML.writecontents(fullmaimldict, outmaimlpath)
    except Exception as e:
        print('Error while writing to the file.',e) 
        raise e



if __name__ == '__main__':
    maimlfilename = "input.maiml"
    exfilename = 'input.xlsx'
    maimlpath = ''
    exfilepath = ''
    otherspath = ''
    
    if len(sys.argv) > 1:
        rootdir = Path(filepath.input_dir + sys.argv[1])
        if rootdir.exists() and rootdir.is_dir():
            for file in rootdir.rglob('*'):  # rglob('*') で再帰的にすべてのファイルを取得
                if file.is_file():  # ファイルかどうかを確認
                    # ファイル名と拡張子を分けて取得
                    file_extension = file.suffix  # 拡張子を取得
                    if file_extension == '.maiml':
                        maimlfilename = file
                    elif file_extension == '.xlsx':
                        exfilename = file
            maimlpath = rootdir / maimlfilename
            exfilepath = rootdir / exfilename
            otherspath = rootdir
    else:
        maimlpath = Path(filepath.input_dir + 'maiml/'+ maimlfilename)
        exfilepath = Path(filepath.input_dir + 'excel/'+ exfilename)
        otherspath = Path(filepath.input_dir + 'others/')
    try:
        print('INPUT FILES ==')
        print('maimlpath: ',maimlpath)
        print('exfilename: ',exfilepath)
        print('======================')
        main(maimlpath, exfilepath, otherspath)
        print('Successfully created the data file.')
    except Exception as e:
        print('Error : ',e)
     

    