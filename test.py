import cv2
import numpy as np
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup
# from selenium import webdriver
import random
# import requests
from datetime import datetime
import csv
import time

def image_render(code:str,model:str):
    """
    code コード
    model 型番
    """
    import glob
    images = glob.glob(f'image_folder/{code}*.png')
    
    for image in images:

        #png透過イメージ合成に対応

        img_a = cv2.resize(cv2.imread(image),dsize=(500,500))
        img_b = cv2.resize(cv2.imread('fixed_image/b.png', cv2.IMREAD_UNCHANGED),dsize=(500,500))

        width, height = (500,500)


        maskb = img_b[:,:,3]  # アルファチャンネルだけ抜き出す。
        maskb = cv2.cvtColor(maskb, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
        maskb = maskb / 255  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。後で透過率をかけるのに使う



        img_b = img_b[:,:,:3]  # アルファチャンネルは取り出したため、廃棄

        img_a[0:height:, 0:width] = np.multiply(img_a[0:height:, 0:width], 1-maskb, out=img_a[0:height:, 0:width], casting='unsafe')
        img_a[0:height:, 0:width] = np.add(img_a[0:height:, 0:width], img_b * maskb, out=img_a[0:height:, 0:width], casting='unsafe')

        blendsrc = img_a

        # cv2.imshow('image',img_a)
        # # # キー入力待ち(ここで画像が表示される)
        # cv2.waitKey()

        img_c = cv2.resize(cv2.imread('fixed_image/outer_frame01.png', cv2.IMREAD_UNCHANGED),dsize=(500,500))

        width, height = img_c.shape[:2]


        mask = img_c[:,:,3]  # アルファチャンネルだけ抜き出す。
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)  # 3色分に増やす。
        mask = mask / 255  # 0-255だと使い勝手が悪いので、0.0-1.0に変更。後で透過率をかけるのに使う


        img_c = img_c[:,:,:3]  # アルファチャンネルは取り出したため、廃棄


        # blendsrc[0:height:, 0:width] *= 1 - mask  # 透過率に応じて元の画像を暗くする。
        blendsrc[0:height:, 0:width] = np.multiply(blendsrc[0:height:, 0:width], 1-mask, out=blendsrc[0:height:, 0:width], casting='unsafe')
        # blendsrc[0:height:, 0:width] += img_c * mask  # 貼り付ける方の画像に透過率をかけて加算。
        blendsrc[0:height:, 0:width] = np.add(blendsrc[0:height:, 0:width], img_c * mask, out=blendsrc[0:height:, 0:width], casting='unsafe')

        # cv2.imshow("image",blendsrc)
        # # キー入力待ち(ここで画像が表示される)
        # cv2.waitKey()

        cv2.imwrite(image, blendsrc)


        from PIL import Image, ImageDraw, ImageFont
        import json


        with open("textconfig.json",'r') as f:
            conf = json.load(f)
            textcolor = (conf["colorRGB"][0], conf["colorRGB"][1], conf["colorRGB"][2]) 
            font = ImageFont.truetype(conf["font"], int(conf["size"]))
            im = Image.open(image)
            draw = ImageDraw.Draw(im)# im上のImageDrawインスタンスを作る
            draw.text((conf['x'],conf['y']),model, fill=textcolor,font=font)
            im.save(image)

image_render("ASS001","15620-37010")