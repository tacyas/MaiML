import copy
from pathlib import Path
import os, sys
import uuid as UUID 
from datetime import datetime as DATETIME
import pytz
from vamas import Vamas
#from vamas.vamas_block import CorrespondingVariable,AdditionalNumericalParam, Optional,SputteringSource

from Utils.createMaiMLFile import ReadWriteMaiML, UpdateMaiML
from Utils.staticClass import maimlelement, settings


################################################
## FILE DIR PATH 
################################################
class filepath:
    cur_file = __file__  #このファイルのパス
    codedir = os.path.dirname(cur_file) + '/'
    rootdir = os.path.abspath(os.path.join(codedir, os.pardir)) + '/'
    input_dir = codedir + 'INPUT/'
    output_dir = codedir + 'OUTPUT/'

################################################
### event要素に設定する日付のフォーマット　
##### YYYY-MM-DDTHH:MM:SS-xx:xx #########
################################################
def formatter_datetime(year,month,day,hour,min,sec,gmtime):
    #print(e_datetime) #2000/3/1 1:00
    vms_datetime = DATETIME(year, month, day, hour, min, sec)
    #print(vms_datetime) # 2000-03-01 01:00:00

    TIME_ZONE = settings.TIME_ZONE #'Asia/Tokyo'
    tokyo_tz = pytz.timezone(TIME_ZONE)
    vms_datetime = tokyo_tz.localize(vms_datetime)
    # 日時を 'YYYY-MM-DDTHH:MM:SS' フォーマットに変換
    datetime_str = vms_datetime.strftime('%Y-%m-%dT%H:%M:%S')

    # タイムゾーンオフセットを取得し、フォーマットを整える（+09:00の形式に）
    offset = vms_datetime.strftime('%z')  # 例: +0900
    formatted_offset = offset[:3] + ':' + offset[3:]  # 例: +09:00

    # 日時とタイムゾーンオフセットを合体
    datetime = f'{datetime_str}{formatted_offset}'
    return datetime

################################################
## results１つが持つ汎用データコンテナと、VAMASデータの１ブロックのデータを比較
## keyが一致した場合、汎用データコンテナのvalueにvamasファイルのデータを挿入
################################################
def writeValue(generallist1, vmsdict):
    blockdata = copy.deepcopy(vmsdict)
    new_generallist = []
    for glindex, generaldict in enumerate(generallist1):
        ## propertyListTypeを処理
        new_generaldict = generaldict
        #print(new_generaldict[maimlelement.typed])
        if new_generaldict[maimlelement.typed] == 'propertyListType':
            if new_generaldict[maimlelement.keyd] == 'corresponding_variables':
                #print('corresponding_variables')
                cv_num = blockdata.num_corresponding_variables  ## corresponding_variableのlistの数
                if cv_num > 0:
                    vmscvlist = blockdata.corresponding_variables
                    child_generallist = []
                    for vmscvdata in vmscvlist:
                        y_values = str(getattr(vmscvdata,'y_values'))
                        if y_values.startswith('['):
                            y_values = y_values[1:]
                        if y_values.endswith(']'):
                            y_values = y_values[:-1]
                        child_generaldict= {
                                            maimlelement.typed : 'propertyListType',
                                            maimlelement.keyd  : str(getattr(vmscvdata,'label')),
                                            maimlelement.property : [{
                                                        maimlelement.keyd : 'y_values',
                                                        maimlelement.unitsd : str(getattr(vmscvdata,'unit')),
                                                        maimlelement.typed : 'floatListType',
                                                        maimlelement.value : y_values},
                                                        {
                                                        maimlelement.keyd : 'y_min',
                                                        maimlelement.unitsd : str(getattr(vmscvdata,'unit')),
                                                        maimlelement.typed : 'floatType',
                                                        maimlelement.value : str(getattr(vmscvdata,'y_min'))},
                                                        {
                                                        maimlelement.keyd  : 'y_max',
                                                        maimlelement.unitsd : str(getattr(vmscvdata,'unit')),
                                                        maimlelement.typed : 'floatType',
                                                        maimlelement.value : str(getattr(vmscvdata,'y_max'))},
                                                        ]
                                            }
                        child_generallist.append(child_generaldict)
                    new_generaldict[maimlelement.property] = child_generallist
            elif generaldict[maimlelement.keyd] == 'additional_numerical_params':
                #print('additional_numerical_params')
                anp_num = blockdata.num_additional_numerical_params  ## additional_numerical_paramsのlistの数
                if anp_num > 0:
                    vmsanplist = blockdata.additional_numerical_params
                    child_generallist = []
                    for vmsanpdata in vmsanplist:
                        child_generaldict= { 
                                maimlelement.keyd   : str(getattr(vmsanpdata,'label')),
                                maimlelement.unitsd : str(getattr(vmsanpdata,'unit')),
                                maimlelement.typed  : 'floatType',
                                maimlelement.value  : str(getattr(vmsanpdata,'value'))
                                            }
                        child_generallist.append(child_generaldict)
                    new_generaldict[maimlelement.property] = child_generallist
            elif generaldict[maimlelement.keyd] == 'sputtering_source':
                #print('sputtering_source')
                vmsssdata = blockdata.sputtering_source.SputteringSource  # SputteringSource
                child_generallist= [{ maimlelement.keyd   : 'energy',
                                        maimlelement.typed  : 'floatType',
                                        maimlelement.value  : str(getattr(vmsssdata,'energy'))
                                    },
                                    { maimlelement.keyd   : 'beam_current',
                                        maimlelement.typed  : 'floatType',
                                        maimlelement.value  : str(getattr(vmsssdata,'beam_current'))
                                    },
                                    { maimlelement.keyd   : 'width_x',
                                        maimlelement.typed  : 'floatType',
                                        maimlelement.value  : str(getattr(vmsssdata,'width_x'))
                                    },
                                    { maimlelement.keyd   : 'width_y',
                                        maimlelement.typed  : 'floatType',
                                        maimlelement.value  : str(getattr(vmsssdata,'width_y'))
                                    },
                                    { maimlelement.keyd   : 'polar_incidence_angle',
                                        maimlelement.typed  : 'floatType',
                                        maimlelement.value  : str(getattr(vmsssdata,'polar_incidence_angle'))
                                    },
                                    { maimlelement.keyd   : 'azimuth',
                                        maimlelement.typed  : 'floatType',
                                        maimlelement.value  : str(getattr(vmsssdata,'azimuth'))
                                    },
                                    { maimlelement.keyd   : 'mode',
                                        maimlelement.typed  : 'stringType',
                                        maimlelement.value  : str(getattr(vmsssdata,'mode'))
                                    },
                                    ]
                new_generaldict[maimlelement.property] = child_generallist
            elif generaldict[maimlelement.keyd] == 'linescan_coordinates':
                #print('linescan_coordinates')
                vmslcdata = blockdata.linescan_coordinates.LinescanCoordinates  # LinescanCoordinates
                child_generallist= [{ maimlelement.keyd   : 'first_linescan_start_x',
                                        maimlelement.typed  : 'intType',
                                        maimlelement.value  : str(getattr(vmslcdata,'first_linescan_start_x'))
                                    },
                                    { maimlelement.keyd   : 'first_linescan_start_y',
                                        maimlelement.typed  : 'intType',
                                        maimlelement.value  : str(getattr(vmslcdata,'first_linescan_start_y'))
                                    },
                                    { maimlelement.keyd   : 'first_linescan_finish_x',
                                        maimlelement.typed  : 'intType',
                                        maimlelement.value  : str(getattr(vmslcdata,'first_linescan_finish_x'))
                                    },
                                    { maimlelement.keyd   : 'first_linescan_finish_y',
                                        maimlelement.typed  : 'intType',
                                        maimlelement.value  : str(getattr(vmslcdata,'first_linescan_finish_y'))
                                    },
                                    { maimlelement.keyd   : 'last_linescan_finish_x',
                                        maimlelement.typed  : 'intType',
                                        maimlelement.value  : str(getattr(vmslcdata,'last_linescan_finish_x'))
                                    },
                                    { maimlelement.keyd   : 'last_linescan_finish_y',
                                        maimlelement.typed  : 'intType',
                                        maimlelement.value  : str(getattr(vmslcdata,'last_linescan_finish_y'))
                                    }
                                    ]
                new_generaldict[maimlelement.property] = child_generallist
        else:
            # 汎用データコンテナを持つか
            if maimlelement.property in new_generaldict:
                generallist2 = new_generaldict[maimlelement.property] if isinstance(new_generaldict[maimlelement.property],list) else [new_generaldict[maimlelement.property]]
                new_generaldict[maimlelement.property] = writeValue(generallist2,vmsdict)
            if maimlelement.content in new_generaldict:
                generallist2 = new_generaldict[maimlelement.content] if isinstance(new_generaldict[maimlelement.content],list) else [new_generaldict[maimlelement.content]]
                new_generaldict[maimlelement.content] = writeValue(generallist2,vmsdict)
            #print("blockdata::",blockdata)
            key = new_generaldict[maimlelement.keyd]
            value = ''
            try:
                value = getattr(blockdata, key)
                #print("type:",type(value))
                if isinstance(value,str) or isinstance(value,float) or isinstance(value,int):
                    #print("hit key::",key)
                    new_generaldict[maimlelement.value] = str(value)
                elif value == None:
                    #print("hit key:None::",key)
                    new_generaldict[maimlelement.value] = ''
                elif isinstance(value,list):
                    print(key, ':list type')
            except Exception as e:
                print(e)
                #print("pass key=",key)
                new_generaldict[maimlelement.value] = ''
                
        new_generallist.append(new_generaldict) 
        
    return new_generallist


###########################################
## main method
###########################################
def main(maimlpath, vmsfilepath):
    ## 1. VAMAS
    ### 1-1. 読み込む
    vamas_data = ''
    vms_headerdata = ''
    vms_datablocks = ''
    try:
        vamas_data = Vamas(vmsfilepath)
        vms_headerdata = vamas_data.header # header data=>
        vms_datablocks = vamas_data.blocks # bloks=>[results],[trace]
    except Exception as e:
        print("VAMAS file reading error.")
        raise e
    
    # VAMAS Fileの情報をテキストファイルに出力
    try:
        with open('./TMP/vamas_output.txt', 'w', encoding='utf-8') as file:
            file.write('HEADER' + "\n")
            file.write(str(vms_headerdata) + "\n")
            file.write('DATA BLOCK' + "\n")
            for block in vms_datablocks:
                file.write(str(block) + "\n")
    except Exception as e:
        print("VAMASファイルのテキスト出力に失敗: ",e)
        pass
        
    ### headerの処理があれば書く
    
    ## 2. MaiML
    ### 2-1. 読み込む
    maimldict = ''
    try:
        readWriteMaiML = ReadWriteMaiML()
        maimldict = readWriteMaiML.readFile(maimlpath)
    except Exception as e:
        print("MaiML file error.")
        raise e
        
    ### 2-2. 計測データを書き出すための準備
    #### 2-2-1. methodのID,programのID,instanceのIDを取得
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
        ### 2-2-2. methoddictに含まれるinstructionのIDを取得し、instructionIDlistリストを作成
        programlist = methoddict[maimlelement.program] if isinstance(methoddict[maimlelement.program],list) else [methoddict[maimlelement.program]]
        for programdict in programlist:
            instructionlist = programdict[maimlelement.instruction] if isinstance(programdict[maimlelement.instruction],list) else [programdict[maimlelement.instruction]]
            for instructiondict in instructionlist:
                instprogIDdict__.update({
                    instructiondict[maimlelement.idd]:{
                    'programID':programdict[maimlelement.idd],
                    'methodID':methoddict[maimlelement.idd],
                }})
    
    ### 2-3. ファイルから取得したmaimlデータのprotocolからdata,eventLogの仮データを作成
    fullmaimldict = ''
    try:
        updateMaiML = UpdateMaiML()
        fullmaimldict = updateMaiML.createFullMaimlDict(maimldict) 
    except Exception as e:
        print("Error in UpdateMaiML-createFullMaimlDict.")
        raise e
    
    #### 2-3-1. results実データ作成の準備
    resultsdict__ = fullmaimldict[maimlelement.maiml][maimlelement.data].pop(maimlelement.results)
    resultslist__ = resultsdict__ if isinstance(resultsdict__, list) else [resultsdict__]  # 念の為

    #### 2-3-2. eventLog実データ作成の準備
    logdict__ = fullmaimldict[maimlelement.maiml][maimlelement.eventlog][maimlelement.log]
    loglist = logdict__ if isinstance(logdict__,list) else [logdict__]
    
    ## 本当は１つのresultsを特定すべきであるが、今回は１つしかないこと(=programが１つ)が前提(全てのresultsがVAMAS-block数分作成される)
    ## method IDを入力すること で対象となるresultsの特定が可能
    #for rindex, resultsdict1__ in enumerate(resultslist__):
    resultsdict1_ = resultslist__[0]

    ### 2-3-3. instance内の汎用データコンテナを取得し更新
    resultslist = []
    datelist = []
    for vmsindex, vms_datablock in enumerate(vms_datablocks):
        resultsdict1 = copy.deepcopy(resultsdict1_)
        instancelist = []
        materiallist = resultsdict1[maimlelement.material] if isinstance(resultsdict1[maimlelement.material],list) else [resultsdict1[maimlelement.material]]
        instancelist.extend(materiallist)
        conditionlist = resultsdict1[maimlelement.condition] if isinstance(resultsdict1[maimlelement.condition],list) else [resultsdict1[maimlelement.condition]]
        instancelist.extend(conditionlist)
        resultlist = resultsdict1[maimlelement.result] if isinstance(resultsdict1[maimlelement.result],list) else [resultsdict1[maimlelement.result]]
        instancelist.extend(resultlist)
        
        generallist = []
        for instancedict in instancelist:
            if maimlelement.property in instancedict:
                propertylist = instancedict[maimlelement.property] if isinstance(instancedict[maimlelement.property],list) else [instancedict[maimlelement.property]]
                generallist.extend(propertylist)
            if maimlelement.content in instancedict:
                contentlist = instancedict[maimlelement.content] if isinstance(instancedict[maimlelement.content],list) else [instancedict[maimlelement.content]]
                generallist.extend(contentlist)
        
        ### 2-3-3-2. results１つが持つ汎用データコンテナと、VAMASデータの１ブロックのデータを比較
        try:
            generallist = writeValue(generallist,vms_datablock)
            #print(generallist)
        except Exception as e:
            print("Error in generallist: ")
            raise e
        
        ### 2-3-3-3. reslutslistに作成したresultsを追加
        new_resultsID = resultsdict1[maimlelement.idd] + str(vmsindex)
        resultsdict1[maimlelement.idd] = new_resultsID
        resultsdict1[maimlelement.uuid] = str(UUID.uuid4())
        resultslist.append(resultsdict1)
    
        ### 2-3-4-2. 実行日のデータを取得し加工
        try:
            year = vms_datablock.year
            month = vms_datablock.month
            day = vms_datablock.day
            hour = vms_datablock.hour
            min = vms_datablock.minute
            sec = vms_datablock.second
            gmtime = vms_datablock.num_hours_advance_gmt
            datetime = formatter_datetime(year,month,day,hour,min,sec,gmtime)
        except Exception as e:
            print("dataformat error.")
            raise e
        datelist.append({'resultsID':new_resultsID,'datetime':datetime})
        
                
    ### 2-3-4. trace内のeventを取得し更新
    ### 2-3-4-1. loglistから更新するeventを取得
    ## 本当は１つのlogを特定すべきであるが、今回は１つしかないこと(=programが１つ、つまりmethodが１つ)が前提(全てのlog内のtraceがVAMAS-block数分作成される)
    ## method IDを入力することで対象となるlogの特定が可能
    for logdict1 in loglist:
        #if(logdict[maimlelement.refd] == methoddict[maimlelement.idd]):
        new_tracelist = []                    
        tracelist__ = logdict1.pop(maimlelement.trace)
        tracelist__ = tracelist__ if isinstance(tracelist__,list) else [tracelist__]
        ## programIDを入力することで、対象となるtraceの特定が可能
        #for tracedict1 in tracelist__:
        tracedict1 = tracelist__[0]
        for dlindex, datedict in enumerate(datelist):
            new_tracedict = copy.deepcopy(tracedict1)
            ### 2-3-4-3. event要素を更新
            eventlist_ = copy.deepcopy(new_tracedict[maimlelement.event])
            for eindex, eventdict_ in enumerate(eventlist_):
                eventdict_[maimlelement.idd] = eventdict_[maimlelement.idd] + str(eindex) + str(dlindex)
                eventdict_[maimlelement.uuid] = str(UUID.uuid4())
                eventdict_[maimlelement.resultsRef] = {
                                                        maimlelement.idd:eventdict_[maimlelement.idd]+'_resultref' + str(eindex) + str(dlindex), 
                                                        maimlelement.refd:datedict['resultsID']
                                                    }
                propertylist = eventdict_[maimlelement.property] # 必ずlist
                for propertydict in propertylist:
                    if propertydict[maimlelement.keyd] == maimlelement.time and datedict['datetime'] != '':
                        propertydict[maimlelement.value] = datedict['datetime']
            new_tracedict[maimlelement.event] = eventlist_
            new_tracedict[maimlelement.idd] = new_tracedict[maimlelement.idd] + str(dlindex)
            new_tracedict[maimlelement.uuid] = str(UUID.uuid4())
            new_tracelist.append(new_tracedict)
        
        ### 2-3-4-4. 新しいtracelistで更新
        logdict1.update({maimlelement.trace:new_tracelist})
            
    ## fullmaimldict[results]を、作成したresultslistで置き換える
    fullmaimldict[maimlelement.maiml][maimlelement.data].update({maimlelement.results:resultslist})
  
    ### 2-4. outputファイルを保存
    try:
        outmaimlpath = './OUTPUT/output.maiml'
        path, duuid = readWriteMaiML.writecontents(fullmaimldict, outmaimlpath)
    except Exception as e:
        print('Error while writing to the file.')
        raise e
    
    return path



###########################################
## 実行関数
###########################################
if __name__ == '__main__':
    maimlfilename = "input.maiml"
    vmsfilename = 'input.vms'
    maimlpath = ''
    vmsfilepath = ''
    # inputファイルを取得
    if len(sys.argv) > 1:
        rootdir = Path(filepath.input_dir + sys.argv[1])
        if rootdir.exists() and rootdir.is_dir():
            for file in rootdir.rglob('*'):  # rglob('*') で再帰的にすべてのファイルを取得
                if file.is_file():  # ファイルかどうかを確認
                    # ファイル名と拡張子を分けて取得
                    file_extension = file.suffix  # 拡張子を取得
                    if file_extension == '.maiml':
                        maimlfilename = file
                    elif file_extension == '.vms':
                        vmsfilename = file
            maimlpath = rootdir / maimlfilename
            vmsfilepath = rootdir / vmsfilename
    else:
        maimlpath = Path(filepath.input_dir + 'maiml/'+ maimlfilename)
        vmsfilepath = Path(filepath.input_dir + 'vamas/'+ vmsfilename)

    print('INPUT FILES ==')
    print('maimlpath: ',maimlpath)
    print('exfilename: ',vmsfilepath)
        
    try:        
        outputfilepath = main(maimlpath, vmsfilepath)
        print('Successfully created the data file.: ',outputfilepath)
    except Exception as e:
        print('Error : ',e)