#################################
##   static class
#################################
from datetime import datetime as DT
from datetime import timezone as TZ
from datetime import timedelta as TD


#################################
##   static val
#################################
class staticVal():
    ## default UUID value
    upload_maiml_id = '88aff11e-a38c-4e65-b3d1-e62a76fbd75f'
    default_data_filepath = '/defaultdata/datasample.maiml'

    tiffmetatype = {
        '1' : 'unsignedByteType', # xs:unsignedByte 1	1byte	BYTE	UInt8(符号無し8bit整数)
        #'ASCII' : 2,
        '3' : 'unsignedShortType', # xs:unsignedShort 3	2byte	SHORT	Uint16(符号無し16bit整数)
        '4' : 'unsignedLongType', # xs:unsignedLong 4	4byte	LONG	Uint32(符号無し32bit整数)
        #'5' : 'RATIONAL',
        '6' : 'byteType', # xs:byte 6	1byte	SBYTE	SInt8(符号付き8bit)
        #'7' : 'UNDEFINED',
        '8' : 'shortType', # xs:short 8	2byte	SSHORT	SInt16(符号付き16bit整数)
        '9' : 'longType', # xs:long 9	4byte	SLONG	SInt32(符号付き32bit整数)
        # '10' : 'SIGNED_RATIONAL',
        '11' : 'floatType', # xs:float 11	4byte	FLOAT	浮動小数点（IEEE 単精度浮動小数点)
        '12' : 'doubleType', # xs:double 12	8byte	DOUBLE	浮動小数点（IEEE 倍精度浮動小数点)
        #'13' : 'IFD',
        #'16' : 'LONG8',
        }

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
    generalTagList = ['property', 'content']
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
    ns= 'xmlns:'

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
    nsd= '@xmlns:'

    ## eventLogに関するattributes
    conceptd = '@concept'
    lifecycled = '@lifecycle'
    timeAttribd = '@time'

    ## insertionに関するattributes
    methodd = '@method'
    # insertion要素の値を判別するための名前
    insertiontext = '#text'

class tiffKeys():
    datetime = 'DateTime'
    time = 'time:timestamp'


class messagesList():
    # Notice to users
    invalidFiles = 'InputFiles is invalid data.'
    # Internal errors
    readTiffError = 'Errors occurred in utils.readTIFF'
    # DB errors
    registrationError = 'Data registration error.'