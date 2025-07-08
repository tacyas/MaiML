#########################################################
##  ユーザーが指定する定数
#####  _MAIML_ATTR : maiml要素の属性を記述する
#####  _IN_EXCEL_FILENAME  : 入力するエクセルファイル名を記述する
#####  _MaiML_FILENAME  : 出力するMaiMLファイル名を記述する
#########################################################


import os
class filePath():
    ##　ここから編集可
    _INPUT_EXCEL_PATH = "A-preparation.4.xlsx"
    _INPUT_MaiML_PATH = "A-preparation.1.maiml"
    _MaiML_FILENAME = "A-preparation.2.maiml"
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
    _IN_EXCEL_FILEPATH = _INPUT_DIR + 'excel/' + _INPUT_EXCEL_PATH
    _IN_MaiML_PATH = _INPUT_DIR + 'maiml/' + _INPUT_MaiML_PATH
    _IN_OTHER_FILEPATH = _INPUT_DIR + 'others/'
    _MaiML_FILEPATH = _OUTPUT_DIR + _MaiML_FILENAME

    @property
    def INPUT_EXCEL_PATH(self):
        if not os.path.isfile(self._IN_EXCEL_FILEPATH):
            print("入力ファイルが存在しません。 ", self._IN_EXCEL_FILEPATH)
            exit(1)
        return self._IN_EXCEL_FILEPATH
    @property
    def INPUT_MaiML_PATH(self):
        if not os.path.isfile(self._IN_MaiML_PATH):
            print("入力ファイルが存在しません。 ", self._IN_MaiML_PATH)
            exit(1)
        return self._IN_MaiML_PATH
    @property
    def INPUT_OTHER_PATH(self):
        return self._IN_OTHER_FILEPATH
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
    
    
class time():
    _TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
    ##　ここから編集可
    _TIME_ZONE = "Asia/Tokyo"
    ##　ここまで編集可
    
    ############################################################################
    @property
    def TIME_FORMAT(self):
        return self._TIME_FORMAT
    @property
    def TIME_ZONE(self):
        return self._TIME_ZONE
    ############################################################################