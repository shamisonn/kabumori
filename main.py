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

def convert_cv2_pil(img):
    return Image.fromarray((cv2.cvtColor(img, cv2.COLOR_BGR2RGB)))


tools = pyocr.get_available_tools()


# 画像から文字を生成
def image2text(img) -> str:
    return tools[0].image_to_string(
        img,
        lang='eng',
        builder=pyocr.builders.TextBuilder(tesseract_layout=6))


def clean(text: str) -> str:
    m = re.search(r'\d+', text)
    return m.group()


def main() -> ():
    out_name = 'out.png'
    print(clean(image2text(convert_cv2_pil(preformat(get_img('kabu.jpeg'))))))


if __name__ == '__main__':
    main()
