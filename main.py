import urllib.request
import urllib.parse
from PIL import Image
import re

import numpy
import cv2
import pyocr
import pyocr.builders


# OpenCV形式で画像読み込み
def get_img(path: str):
    return cv2.imread(path)


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


def gray(img):
    g, _ = cv2.decolor(img)
    return g


# 前処理。OpenCV形式の画像からカブ価の箇所を切り取り
def preformat(img: numpy.ndarray):
    return gray(crop(img, 410, 530, 50, 150))


# openCVの形式からPython標準の形式に変換
def convert_cv2_pil(img: numpy.ndarray) -> Image:
    return Image.fromarray(img)


tools = pyocr.get_available_tools()


# pyocrで画像解析。
def image2text(img: Image) -> str:
    return tools[0].image_to_string(
        img,
        lang='jpn',
        builder=pyocr.builders.TextBuilder(tesseract_layout=6))


# 丸文字のリストを生成
def circle_numbers():
    nums = []
    for i in range(ord('①'), ord('⑳') + 1):
        nums.append(chr(i))
    for i in range(ord('㉑'), ord('㉟') + 1):
        nums.append(chr(i))
    for i in range(ord('㊱'), ord('㊿') + 1):
        nums.append(chr(i))
    return nums


# 丸文字と数字のdictを生成
def circle_number_dict():
    keys = circle_numbers()
    values = []
    for i in range(1, 51):
        values.append(str(i))
    dic = {}
    for i in range(0, 50):
        dic[keys[i]] = values[i]
    return dic


# 生の文字データを数字列に変換。カブ価を取得する
def clean(text: str) -> str:
    pattern = re.compile('[0123456789{}]+'.format(''.join(circle_numbers())))
    m = pattern.search(text)
    bell = m.group()
    for k, v in circle_number_dict().items():
        bell = bell.replace(k, v)
    return bell


# twimgのurlからOpenCVのimageインスタンスを生成する
def url2image(image_url):
    res = urllib.request.urlopen(image_url)
    image = numpy.asarray(bytearray(res.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)


# tweetのhtml文字列からimageのurlを撮ってくる
def body2image_url(html_body):
    m = re.search(r'https://pbs\.twimg\.com/media/\S+\.jpg', html_body)
    return m.group()


# tweetのurlからtweet imageのurlを撮ってくる
def tweet2image_url(tweet_url):
    with urllib.request.urlopen(tweet_url) as response:
        body = response.read().decode("utf-8")
        image_url = body2image_url(body)
        return image_url + '?format=jpg&name=large'


# tweetのurlからカブ価を取得する
def tweet2bell(tweet_url) -> str:
    image_url = tweet2image_url(tweet_url)
    bell = clean(image2text(convert_cv2_pil(preformat(url2image(image_url)))))
    return bell


if __name__ == '__main__':
    print(tweet2bell('https://twitter.com/nosimahs/status/1246852380030693376'))
