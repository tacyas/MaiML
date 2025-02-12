# VAMAS2MaiML
## A：実行方法
### [入出力データ]
- 入力データ　　※条件等は下記[B:詳細]を参照
  1. document,protocolのコンテンツをもつMaiMLデータファイル <br/>
　　INPUT/maiml/input.maiml  or  INPUT/xxxxx/yyyyyy.maiml 
  1. 計測に使用した情報をもつVAMASデータファイル<br/>
　　INPUT/vamas/input.vms  or  INPUT/xxxxx/zzzzzz.vms
- 出力データ
  1. 入力データをマージしたMaiMLファイル <br/>
　　OUTPUT/output.maiml<br/>
  1. VAMASデータファイルから取得した情報を書き出したテキストファイル <br/>
　　TMP/vamas_output.txt
 
### [実行方法]
- その１.
  1. 入力ファイルを準備 <br/>
　　/INPUT/maiml/ ディレクトリにMaiMLファイル <br/>
　　/INPUT/vamas/ ディレクトリにVAMASファイル <br/>
  2. コマンド実行 <br/>
　　python3 vms2maiml.py <br/>
- その２.
  1. 入力ファイルを準備 <br/>
　　/INPUT/XXXXX/　ディレクトリにMaiMLファイル、VAMASファイル　 <br/>
　　　※'XXXXX'は任意の名前 <br/>
  1. コマンド実行 <br/>
　　python3 vms2maiml.py XXXXX <br/>


## B:詳細
### [入力するMaiMLデータ]
  ・program１つを保証 <br/>
  ・VAMASフォーマットのキーを、materilaTemplate/conditionTemplate/resultTemplateがもつ <br/>
  　汎用データコンテナのkeyとしてもつ <br/>

<br/>

### ［作成するMaiMLデータ］
  ・VAMASファイルに複数回の計測データをもつ場合はresultsを複数作成 <br/>
  ・入力MaiMLファイルのtemplateをインスタンスとしてコピーする <br/>
  ・templateがもつ汎用データコンテナのkeyとVAMASファイルのkeyが一致した場合のみ、valueをVAMASデータで更新 <br/>
  　　（一致しなければ、VAMASデータは無視される） <br/>
  ・eventLogを１つ作成 <br/>
　・複数回の計測データをもつ場合はtraceを複数作成 <br/>
　・VAMASフォーマットにおいてLISTやオプションとしてデータをもつ以下のキーが存在した場合は、 <br/>
 　　propertyListTypeで包括した汎用データコンテナを作成 <br/>
　　　1. corresponding_variables
　　　2. AdditionalNumericalParam
　　　3. LinescanCoordinates
　　　4. SputteringSource
   　　　

## C:python実行環境の構築
### [pythonバージョン]
  ・3.12.x <br/>
### [pythonパッケージ]
  ・requirements.txt <br/>
