'''
 Tiff画像の読み込み
 ①Pillowライブラリ(PIL)でマルチページTIFFを読み込む
'''


'''
 ①
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
        # 処理
        print(sImg.width, sImg.height)
        print(sImg.info)
        print(image.tag.iterkyrs())

        for key, value in sImg.info.items():  #tag???
            taginfo = TiffTags.lookup(key)
            print(key, " , " , value)
            print(taginfo)
            
            #switching key and value
            tagdict = {(y,) : x for x, y in taginfo.enum.items()}  # tagdict: dict
            
            print(taginfo.name, ':', tagdict.get(value, value))
        '''


'''
 ②
'''
from PIL import TiffTags as TAGS

def readTIFF2(filename):
    print(filename)
    with Image.open(filename) as img:   # img: PIL.TiffImagePlugin.TiffImageFile type
        metadata = img.tag
        print(metadata)  #metadata: dict type

        print('===================================================')
        # tiftagのキー（３桁数字）と値（tiffのタグ名）
        # tiftagのキーとimg.tagのキーを照らし合わせることで、タグ名を取得できる
        for key in metadata.keys():
            keyname = TAGS.lookup(key).name
            #print(keyname, ':', metadata[key])
            #print(item)
        #meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.iterkeys()}
        #print(meta_dict)


#コードを実行
import sys

if __name__ == "__main__":
    args = sys.argv  # 1:実行関数指定　2:読み込むファイル名

    #パス、ファイル名
    read_dir = './IN_DATA/'
    if len(args) >= 3:
        read_file1 = args[2]
    else:
        read_file1 = "image1.tif"  # デフォルトのファイル名

    if args[1] == '1':
        readTIFF1(read_dir + read_file1)
    elif args[1] == '2':
        readTIFF2(read_dir + read_file1) 