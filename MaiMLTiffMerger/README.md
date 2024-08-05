# MaiMLTiffMerger
## 概要
TIFF画像を出力する計測工程の情報をもつMaiMLファイルと、計測結果の情報をマージするwebシステムである。

---


## (a) システムの使用方法
1. MorphoSmanual.pdf、MaiMLTiffMerger説明.pdfを参照

## (b) 動作確認済みの入出力データ条件
### [入力データ]
1. document層、protocol層をもつMaiMLファイル
    1. \<instruction>を１つもつ
    2. instructionの出力である\<resultTemplate>を１つもつ
2. メタデータを持つTIFFファイル
    1. TIFF画像を出力したdatetimeをもつ
3. 入力するMaiMLに追加する結果のデータ
    1. 計測で利用した\<material>、\<condition>のコンテンツに追加するデータ
    2. TIFFファイルのメタデータから抽出可能なデータ以外の、\<result>コンテンツに追加するデータ

### [出力データ]
1. 入力MaiMLデータ（計測工程のデータ）に、data層、eventLog層のコンテンツ（計測結果のデータ）を生成追加したMaiMLデータ
    1. template(\<materialTemplate>、\<conditionTemplate>、\<resultTemplate>)のコンテンツをinstance(\<material>、\<condition>、\<result>)に引き継いだ\<data>要素のコンテンツをもつ
    2. protocol層でもっている参照関係が、自動でdata層に引き継がれることはない
    3. １つの\<instruction>要素に対して１つの\<event>要素をもつ
    4. TIFFのメタデータのキー'DateTime'の値を\<eventLog>要素の完了時刻としてもつ
    5. 4以外のTIFFのメタデータを\<result>要素の汎用データコンテナとしてもつ
    6. 入力TIFFファイルのURI、hash値を\<result>要素の\<insertion>要素のコンテンツとしてもつ
2. 1.のMaiMLファイル
3. 1.のMaiMLファイルと入力TIFFファイルをZIPしたファイル

## (c) システムの起動方法
1. docker composeサービスを起動
2. docker環境を下記コマンドで起動
   docker-compose up -d
3. webブラウザからローカルホストにアクセス
   http://127.0.0.1:80/
