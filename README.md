# JIS K 0200 :2024 計測分析装置の分析データ共通フォーマット(MaiMLデータフォーマット）を活用するためのプログラム

## MaiML ディレクトリ構成
1. MaiML2Excel　　: `MaiMLファイルから結果情報を抽出しエクセルファイルへ書き出すプログラム`
   1. RUN-python
   2. Run on Docker
   3. README
2. MaiMLViewer　　: `MaiMLファイルに記載されている計測分析のフローを可視化するWEBシステム`
   1. docker-compose.yml
   2. README
3. MaiMLTiffMerger 　　: `MaiMLファイルに記載された計測分析工程の情報に、TIFFのメタ情報などの計測結果情報を追加するWEBシステム`
   1. MorphoS
   2. README
   3. MaiMLTiffMerger説明.pdf
   4. MorphoSmanual.pdf
4. Misc 　　: `MaiMLデータフォーマットを作成、解析するためのサンプルプログラム`
5. MaiMLFileSamples　　: `MaiMLファイルのサンプル集`
6. Excel2MaiML　　:　`計測フローを定義したMaiMLファイルと計測結果を記載したExcelファイルをマージするプログラム`
7. VAMAS2MaiML　　:　`計測フローを記載したMaiMLファイルと計測結果を記載したvamas形式のファイルをマージするプログラム`
8. Excel2MaiMLProtocol　　:　`計測フローデータを記載したExcelデータをMaiMLデータへ変換するプログラム`
