import cv2
import numpy as np


#画像Aを読み込む

img_a = cv2.resize(cv2.imread('a.png'),dsize=(500,500))
img_b = cv2.resize(cv2.imread('b.jpeg'),dsize=(500,500))
blend=cv2.addWeighted(img_a,0.8,img_b,0.2,0)
blendsrc = cv2.cvtColor(blend, cv2.COLOR_BGR2RGB)



# cv2.imshow("image",blendsrc)
# # キー入力待ち(ここで画像が表示される)
# cv2.waitKey()

img_c = cv2.resize(cv2.imread('c.png', cv2.IMREAD_UNCHANGED),dsize=(500,500))

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

cv2.imwrite('out.png', blendsrc)