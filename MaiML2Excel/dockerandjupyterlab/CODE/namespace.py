#####################################
##  MaiMLで使用するNameSpaceの定義
#####################################

## default
class defaultNS():
    namespaces = { 
                'http://www.maiml.org/schemas': None,  # skip
                'http://www.w3.org/2001/XMLSchema-instance': 'xsi' , # 'xsi:で展開する'
               # 'http://www.example.com/maiml/material#' : 'exm' ,  # 'exm:で展開する'
    }