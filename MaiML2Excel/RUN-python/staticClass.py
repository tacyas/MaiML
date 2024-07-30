
#################################
##   static class
#################################

## MaiML DATA FORMAT element and attribute name #################################
class maimlelement():
    ## elements
    maiml = 'maiml'
    document = 'document'
    protocol = 'protocol'
    data = 'data'
    eventlog = 'eventLog'

    uuid = 'uuid'    
    childUri = 'childUri'     ## >=0
    childHash = 'childHash'     ## >=0
    childUuid = 'childUuid'     ##  >=0
    insertion = 'insertion'  ## >=0
    name = 'name'        
    description = 'description'
    annotation = 'annotation'
    property = 'property'
    content = 'content'
    uncertainty = 'uncertainty'
    generalTagList = ['property', 'content', 'uncertainty']
    value = 'value'  ## >=0
    templateRef = 'templateRef'      ## >=0
    instanceRef = 'instanceRef'    # >=0  参照要素
    chain_hash = 'hash'   ## =1
    chain = 'chain'  ## >=0
    parentT_hash = 'hash'   ## =1
    parentT = 'parent'  ## >=0
    uri = 'uri'
    hash = 'hash'
    format = 'format'

    creator = 'creator'   ##>=1  特定グローバル要素
    vendorRef = 'vendorRef'  ## >=1 参照要素
    instrumentRef = 'instrumentRef'    ## >=0　参照要素
    vendor = 'vendor'    ## >=1　　特定グローバル要素
    owner = 'owner'    ## >=1　　特定グローバル要素
    instrument = 'instrument'   ##  >=0　　特定グローバル要素
    date = 'date'    ## =1   xs:dateTime（2018-11-10T22:12:59+09:00）
    method = 'method'  ##contents   # >=1
    pnml = 'pnml'  ##  >=1
    place = 'place'    # >=1
    transition = 'transition'    # >=1
    arc = 'arc'    # >=1
    program = 'program'   ## contents   >=1
    instruction = 'instruction'    #  >=1
    transitionRef = 'transitionRef'    ##  >=1 参照要素
    materialTemplate = 'materialTemplate' 
    conditionTemplate = 'conditionTemplate'
    resultTemplate = 'resultTemplate'
    placeRef = 'placeRef'

    results = 'results'   ## >=1
    material = 'material'     ## >=0
    condition = 'condition'     ## >=0
    result = 'result'     ## >=0

    log = 'log'   ##  >=1  参照付グローバル
    trace = 'trace'   ## >=1  参照付グローバル
    event = 'event'   # >=1  参照付グローバル
    resultsRef = 'resultsRef'    # >=0  参照要素
    event_creatorRef = 'creatorRef'    # >=0  参照要素
    event_ownerRef = 'ownerRef'    # >=0  参照要素

    ## attributes
    type = 'xsi:type'
    id = 'id'
    ref = 'ref'
    key = 'key'
    formatString ='formatString'
    units = 'units'
    scaleFactor = 'scaleFactor'
    axis = 'axis'
    size = 'size'

    ## eventLogに関するattributes
    concept = 'concept'
    lifecycle = 'lifecycle'
    timeAttrib = 'time'
    conceptinstance = 'concept:instance'
    time = 'time:timestamp'
    lifecycletransition = 'lifecycle:transition'

    ## attributes
    typed = '@xsi:type'
    idd = '@id'
    refd = '@ref'
    keyd = '@key'
    formatStringd ='@formatString'
    unitsd = '@units'
    scaleFactord = '@scaleFactor'
    axisd = '@axis'
    sized = '@size'
    sourced = '@source'
    targetd = '@target'

    ## eventLogに関するattributes
    conceptd = '@concept'
    lifecycled = '@lifecycle'
    timeAttribd = '@time'

    ## insertionに関するattributes
    methodd = '@method'
    # insertion要素の値を判別するための名前
    insertiontext = '#text'


#################################
##   プログラム実行に関する定数
#################################
## FILE DIR PATH #################################################
import os
class filepath:
    cur_file = __file__  #このファイルのパス
    print(os.path.dirname(cur_file))

    codedir = os.path.dirname(cur_file) + '/'
    rootdir = os.path.abspath(os.path.join(codedir, os.pardir)) + '/'
    input_dir = rootdir + 'DATA/INPUT/'
    output_dir = rootdir + 'DATA/OUTPUT/'
    tmp_dir = rootdir + 'DATA/TMP/'

## コマンド引数定義  #################################################################
import argparse
class commandargs():
    parser = argparse.ArgumentParser()
    # '-t' > '-j' > '-m'
    parser.add_argument('-j', '--json', action='store_true') # use json file Flag
    parser.add_argument('-m', '--maiml',default='') # input maiml file name
    parser.add_argument('-o', '--xl', default='') # output file name
    parser.add_argument('-si', '--selectid',  nargs="*", default='') # result ID
    parser.add_argument('-sk', '--selectkey',  nargs="*", default='') # general container key
    #parser.add_argument('-d', '--doc', action='store_true') # get document contents Flag
    parser.add_argument('-t', '--test', action='store_true') # tests run Flag


#################################
##   static val
#################################
from openpyxl.styles import PatternFill

### excel header定義 ###############################################################
headerlistA={
    'A':'hierarchy',
    'B':'element',
    'C':'@xsi:type',
    'D':'@key',
    'E':'@formatString',
    'F':'@units',
    'G':'@scaleFactor',
    'H':'@axis',
    'I':'@size',
    'J':'@id',
    'K':'@ref',
    'L':'childUri',
    'M':'childHash',
    'N':'childUuid',
    'O':'EncryptedData',
    'P':'description',
    'Q':'value',
    }

### excel header定義 ###############################################################
headerlist={
    'A':'MaiML file lineNo',
    'B':'hierarchy',
    'C':'element',
    'D':'description',
    'E':'element data',
    'F':'@xsi:type',
    'G':'@key',
    'H':'@formatString',
    'I':'@units',
    'J':'@scaleFactor',
    'K':'@axis',
    'L':'@size',
    'M':'@id',
    'N':'@ref',
    'O':'value'
    }

### excel header定義 ###############################################################
headerlistET={
    'A':'MaiML file lineNo',
    'B':'hierarchy',
    'C':'element',
    'D':'description',
    'E':'element data',
    'F':'{http://www.w3.org/2001/XMLSchema-instance}type',
    'G':'key',
    'H':'formatString',
    'I':'units',
    'J':'scaleFactor',
    'K':'axis',
    'L':'size',
    'M':'id',
    'N':'ref',
    'O':'value'
    }

encheaderlist = [
    "childUri",
    "childHash",
    "childUuid",
    "EncryptedData"
]

### excel headerのstyle定義 ########################################################
fill = PatternFill(patternType='solid', fgColor='EAE7F3')
