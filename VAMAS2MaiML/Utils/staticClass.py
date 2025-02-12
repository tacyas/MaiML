#################################
##   MaiML element define
#################################
class maimlelement:
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


class settings:
    TIME_ZONE = 'Asia/Tokyo'
class staticVal:
    default_data_filepath = '/defaultdata/datasample.maiml'
