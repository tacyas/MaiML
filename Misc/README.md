# Misc

動作の保証は無しです！

---

* createMaiMLFile.py
    1. pythonのdict型からMaiMLファイルを作成する関数(writecontents)
    2. MaiMLファイルからpythonのdict型のデータを生成する関数(readFile)
    3. グローバル要素型のMaiMLデータを生成する関数(writeGlobalContents)
    4. 汎用データコンテナ型のMaiMLデータを生成する関数(writeGenericdataContainer)
    5. テンプレート要素のMaiMLデータを生成する関数(writeTemplates)
    6. インスタンス要素のMaiMLデータを生成する関数(writeInstanceData)
    7. chain要素のMaiMLデータを生成する関数(writeChainContents)
    8. parent要素のMaiMLデータを生成する関数(writeParentContents)
    9. 参照要素型のMaiMLデータを生成する関数(writeReferenceContents)
    10. document要素のMaiMLデータを生成する関数(createdocumentcontents)
    11. protocol要素のMaiMLデータを生成する関数(createprotocolcontents)
    12. data要素のMaiMLデータを生成する関数(createdatacontents)
    13. eventLog要素のMaiMLデータを生成する関数(createeventlogcontents)
* filehash.py
    1. ファイルのハッシュ値を求めるプログラム
* tiffTest.py
    1. マルチTIFFを読み込む関数(readTIFF1)
    2. TIFFファイルからメタデータを取得する関数(readTIFF2)
* xmltodicttocsv.py
    1. INPUTディレクトリに存在するファイルをすべて取得し、pythonのdict型に変換する関数(readfiles)
    2. pythonのdict型データをCSV形式のファイルoutput.csvに出力する関数(makecsv)
* xmltodicttojson.py
    1. XML形式のデータをpythonのdict型のデータへ変換し、それをJSON形式のデータへ変換するプログラム
* yamltomaiml.py
    1. YAML形式のデータからMaiML形式のデータを取得する関数(getDocment1)
