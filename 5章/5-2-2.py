import pathlib
from PIL import Image
import numpy as np
import cv2

#vscodeの場合、実行したファイルをpathとしないので、open('cat.jpg')としても、動かない
PATH = pathlib.Path(__file__).parent #この実行ファイルの場所 pathlib.Path(__file__)

img = Image.open(PATH / 'cat.jpg')

w,h = img.size

#縮小
img_resize = img.resize((int(w/10), int(h/10))) # <-2重括弧でないと、エラー
img_resize.show()

#リサイズ
img_resize = img_resize.resize((w,h))
img_resize.show()

# vscodeだと、cv2でエラーが起きるらしい