#########################################################
##  ユーザーが指定する定数
#####  _MAIML_ATTR : maiml要素の属性を記述する
#####  _IN_EXCEL_FILENAME  : 入力するエクセルファイル名を記述する
#####  _MaiML_FILENAME  : 出力するMaiMLファイル名を記述する
#########################################################


class defaultNS():
    _MAIML_ATTR = [
        ## ここから編集可
        'version="1.0"', 
        'features="nested-attributes"', 
        'xsi:type="protocolFileRootType"',
        #### 以下名前空間定義
        'xmlns="http://www.maiml.org/schemas"',
    	'xmlns:maiml="http://www.maiml.org/schemas"', 
        'xmlns:time="http://www.xes-standard.org/time.xesext#"',
    	'xmlns:concept="http://www.xes-standard.org/concept.xesext#"',
    	'xmlns:lifecycle="http://www.xes-standard.org/lifecycle.xesext#"',
    	'xmlns:xsd="http://www.w3.org/2001/XMLSchema"',
    	'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"', 
    	'xmlns:BBBB="http://BBBB.corp/index.jp"', 
    	'xmlns:BBBBHPLC="http://BBBB.corp/ontology/hplc"', 
    	'xmlns:CDF="http://BBBB.corp/ontology/cdf"', 
        ##　ここまで編集可
    ]


    ############################################################################
    @property
    def MAIML_ATTR(self):
        return self._MAIML_ATTR
    ############################################################################








import os
class filePath():
    ##　ここから編集可
    _IN_EXCEL_FILENAME = "example.xlsx"
    _MaiML_FILENAME = "output.maiml"
    ##　ここまで編集可
    
    
    ############################################################################
    ## 実行ファイルのディレクトリ
    _cur_file = __file__  #このファイルのパス
    _codedir = os.path.dirname(_cur_file) + '/'
    _rootdir = os.path.abspath(os.path.join(_codedir, os.pardir)) + '/'
    _INPUT_DIR = _rootdir + 'INPUT/'
    _OUTPUT_DIR = _rootdir + 'OUTPUT/'
    
    ## 入出力ディレクトリが存在しない場合は作成しておく
    os.makedirs(_INPUT_DIR, exist_ok=True)
    os.makedirs(_OUTPUT_DIR, exist_ok=True)
    
    # 入出力ファイルパス
    _IN_EXCEL_FILEPATH = _INPUT_DIR + 'excel/' + _IN_EXCEL_FILENAME
    _MaiML_FILEPATH = _OUTPUT_DIR + _MaiML_FILENAME

    @property
    def INPUT_FILE_PATH(self):
        if not os.path.isfile(self._IN_EXCEL_FILEPATH):
            print("入力ファイルが存在しません。 ", self._IN_EXCEL_FILEPATH)
            exit(1)
        return self._IN_EXCEL_FILEPATH
    @property
    def OUTPUT_FILE_PATH(self):
        return self._MaiML_FILEPATH
    @property
    def INPUT_DIR(self):
        return self._INPUT_DIR
    @property
    def OUTPUT_DIR(self):
        return self._OUTPUT_DIR
    ############################################################################
    