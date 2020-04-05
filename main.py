from PIL import Image
import re

import numpy
import cv2
import pyocr
import pyocr.builders


# OpenCV形式で画像読み込み
def get_img(path: str):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)


# 画像から切り取る。
# 基点: (x, y)
# 画像指定: {
#   "左上": "x, y",
#   "左下": "x, y+h",
#   "右上": "x+w, y",
#   "右下": "x+w, y+h"
# }
# 元画像の左上: {x == 0, && y == 0}
def crop(img: numpy.ndarray, x: int, y: int, h: int, w: int):
    return img[y:y + h, x:x + w]


# 前処理。OpenCV形式の画像からカブ価の箇所を切り取り
def preformat(img: numpy.ndarray):
    return crop(img, 410, 530, 50, 150)


# openCVの形式からPython標準の形式に変換
def convert_cv2_pil(img: numpy.ndarray) -> Image:
    return Image.fromarray(img)


tools = pyocr.get_available_tools()


# pyocrで画像解析。
def image2text(img: Image) -> str:
    return tools[0].image_to_string(
        img,
        lang='eng',
        builder=pyocr.builders.TextBuilder(tesseract_layout=6))


def clean(text: str) -> str:
    m = re.search(r'\d+', text)
    return m.group()


def main() -> ():
    print(clean(image2text(convert_cv2_pil(preformat(get_img('kabu.jpeg'))))))


if __name__ == '__main__':
    main()
