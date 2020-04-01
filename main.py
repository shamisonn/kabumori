from PIL import Image
import re

import cv2
import pyocr
import pyocr.builders


def get_img(path: str):
    return cv2.imread(path)


def crop(img, x: int, y: int, h: int, w: int):
    return img[y:y + h, x:x + w]


def gray(img):
    g, _ = cv2.decolor(img)
    return g


# 前処理
def preformat(img):
    return gray(crop(img, 410, 530, 50, 150))


# return gray(crop(img, 184, 235, 27, 60))

def write(img, out: str):
    cv2.imwrite(out, img)


tools = pyocr.get_available_tools()


# 画像から文字を生成
def image2text(path) -> str:
    return tools[0].image_to_string(
        Image.open(path),
        lang='eng',
        builder=pyocr.builders.TextBuilder(tesseract_layout=6))


def clean(text: str) -> str:
    m = re.search(r'\d+', text)
    return m.group()


def main() -> ():
    out_name = 'out.png'
    write(preformat(get_img('kabu2.jpeg')), out_name)
    print(clean(image2text(out_name)))


if __name__ == '__main__':
    main()
