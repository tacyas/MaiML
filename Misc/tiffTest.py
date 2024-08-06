'''
 Tiff画像の読み込み
'''


'''
 ①Pillowライブラリ(PIL)でマルチページTIFFを読み込む
'''
from PIL import Image
from PIL import TiffTags

def readTIFF1(filename):
    # Tiff画像を読み込む
    image = Image.open(filename)
    
    # １ページずつ抜き出して処理
    fLength = image.n_frames
    for i in range( 0, fLength ):
        image.seek(i)
        sImg = image.copy()



'''
 ② Tiffのメタデータを取得
'''
from PIL import TiffTags as TAGS
def readTIFF2(filename):
    tiffdict = {}
    with Image.open(f'{filename}') as img:   # img: PIL.TiffImagePlugin.TiffImageFile type
        metadata = img.tag  #metadata: dict type
        # tiftagのキー（３桁数字）と値（tiffのタグ名）
        # tiftagのキーとimg.tagのキーを照らし合わせることで、タグ名を取得できる
        for key in metadata.keys():
            keyname = TAGS.lookup(key).name
            tiffdict[keyname] = {'keynum':key, 'value':str(metadata[key])}
    print(tiffdict)


#コードを実行
import sys
#### param  1 : 実行関数指定    2 : filepath
if __name__ == "__main__":
    args = sys.argv
    #パス、ファイル名
    if len(args) >= 3:
        read_file1 = args[2]
    else:
        exit

    if args[1] == '1':
        readTIFF1(read_file1)
    elif args[1] == '2':
        readTIFF2(read_file1) 