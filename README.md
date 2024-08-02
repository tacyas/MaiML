# JIS K 0200 :2024 計測分析装置の分析データ共通フォーマット(MaiMLデータフォーマット）を活用するためのプログラム

## MaiML ディレクトリ構成
1. MaiML2Excel　　: `MaiMLファイルから結果情報を抽出しエクセルファイルへ書き出すプログラム`
   1. RUN-python
   2. Run on Docker
   3. README
3. MaiMLViewer　　: `MaiMLファイルに記載されている計測分析のフローを可視化するWEBシステム`
   1. docker-compose.yml
   2. README
4. MaiMLTiffMerger 　　: `MaiMLファイルに記載された計測分析工程の情報に、TIFFのメタ情報などの計測結果情報を追加するWEBシステム`
   1. MorphoS
   2. README
   3. MaiMLTiffMerger説明.pdf
   4. MorphoSmanual.pdf
5. Misc 　　: `MaiMLデータフォーマットを作成、解析するためのサンプルプログラム`
