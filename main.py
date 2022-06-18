import cv2
import numpy as np
import matplotlib.pyplot as plt

# 100nm = 46pixel
PIXEL2MICROMETER = 100/46

def horizontal_line(upperleft, downright,contoured_img,max_contour):
    #TODO #2:10等分位置の作成
    global PIXEL2MICROMETER
    img = contoured_img

    #線が横の場合、upperleftからdownrightの幅[0]を使用する
    start = upperleft[0]
    stop = downright[0]
    # 線の真ん中に10個欲しいので、12個
    num = 12

    lins = np.linspace(start, stop, num)[1:11]
    #ピクセルとして扱うため、intに変換
    lins_pixel = [int(x) for x in lins]
    #TODO:横ピクセルに相当する縦ピクセルの最大値と最小値を取得する

    max_contours = [x[0] for x in max_contour]
    gauges = []

    for horizontal_point in lins_pixel:
        data = [x for x in max_contours if x[0]==horizontal_point]
        gauges.append(data)

    # imgg = cv2.imread('testoutput.jpg')

    #TODO:list作成
    gauge_list = []
    point_text_list = []
    for gauge in gauges:
        pt1 = np.amin(gauge,axis=0)
        
        pt2 = np.amax(gauge,axis=0)

        img = cv2.line(img,pt1,pt2,(0,255,0),thickness=5)
        length = int(abs((pt2 - pt1).sum()*PIXEL2MICROMETER))
        text = f'{length}μm'
        point=(int(pt1[0]),min(pt1[1],pt2[1])-50)
        point_text_list.append([point,text])
        # img = cv2.putText(img, text, point, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), thickness=2)
        gauge_list.append(length)
    #CSV形式にて、[元画像ファイル名,出力画像ファイル名,縦横判定,白黒判定,線幅 X 10]

    return gauge_list, img, point_text_list

def vertical_line(upperleft, downright,contoured_img,max_contour):

    #10等分位置の作成
    global PIXEL2MICROMETER
    img = contoured_img

    #線が縦の場合、upperleftからdownrightの高さ[1]を使用する
    start = upperleft[1]
    stop = downright[1]
    # 線の真ん中に10個欲しいので、12個
    num = 12

    lins = np.linspace(start, stop, num)[1:11]
    #ピクセルとして扱うため、intに変換
    lins_pixel = [int(x) for x in lins]
    #横ピクセルに相当する縦ピクセルの最大値と最小値を取得する

    max_contours = [x[0] for x in max_contour]

    gauges = []

    for vertical_point in lins_pixel:
        data = [x for x in max_contours if x[1]==vertical_point]
        gauges.append(data)
 

    #list作成
    gauge_list = []
    point_text_list = []

    for gauge in gauges:
        pt1 = np.amin(gauge,axis=0)
        
        pt2 = np.amax(gauge,axis=0)

        img = cv2.line(img,pt1,pt2,(0,255,0),thickness=5)
        
        length = int(abs((pt2 - pt1).sum()*PIXEL2MICROMETER))

        text = f'{length}μm'
        #右にずらす
        point=(int(pt2[0] + 20),pt2[1])
        point_text_list.append([point,text])
        # img = cv2.putText(img, text, point, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), thickness=2)
        gauge_list.append(length)

    return gauge_list, img, point_text_list


def input_text(opencv_img, point_text_list):

    from  PIL import ImageDraw, ImageFont,Image

    # PIL画像に変換
    pil_image = Image.fromarray(opencv_img)

    # フォントの指定
    font = ImageFont.truetype("ipaexg00401/ipaexg00401/ipaexg.ttf",  size=30)



    # コピーした画像にテキストを追加してplot
    draw = ImageDraw.Draw(pil_image)
    for point, text in point_text_list:
        draw.text(point, text, (0, 255, 0), font=font)
    
    import numpy as np
    
    # OpenCV画像に変換
    numpy_image = np.array(pil_image)

    return numpy_image



def main(WHITE_BOUNDARY=127,BLACK_BOUNDARY = 40):


    import cv2
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import glob

    


    files = glob.glob("before/*.jpg")
    
    #CSV形式にて、[元画像ファイル名,出力画像ファイル名,縦横判定,白黒判定,線幅 X 10]
    csvdata = []

    for img_file_name in files:

        #初期化
        is_black_line = True
        contour_horizontal = True
        output_file_name = 'gauged_' + img_file_name.replace("before\\",'')
        gauge_item = ''

        #画像の読み込み
        img = cv2.imread(img_file_name)


        #BGR =>　グレースケールに変換
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        #グレースケール　=>　二値に変換
        ret, thresh = cv2.threshold(gray, WHITE_BOUNDARY,255, cv2.THRESH_BINARY_INV)

        #デバッグ用二値をblackandwhite.jpgとして保存
        # cv2.imwrite("blackandwhite.jpg",thresh)

        # todo: 白黒判定を行って、背景が黒であれば、二値化をやり直してから反転する
        if np.count_nonzero(thresh) > thresh.size / 2:
            ret, thresh = cv2.threshold(gray, BLACK_BOUNDARY,255, cv2.THRESH_BINARY_INV)
            thresh = 255 - thresh
            is_black_line = False

        # 輪郭の取得
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        
        # 面積の降順にソート
        contours = sorted(contours, key=cv2.contourArea,reverse=True)


        max_contour = None

        # contoursから左下と右下の領域を除く
        # 左下
        white_point1 = (150,1150)
        # 右下
        white_point2 = (1500,1150)
        for cont in contours:
            result1 = cv2.pointPolygonTest(cont, white_point1, measureDist=False)
            result2 = cv2.pointPolygonTest(cont, white_point2, measureDist=False)
            if result1 == -1 and result2 == -1:
                max_contour = cont
                break

        #輪郭を発見できなかったら終了
        if max_contour is None:
            return False

        #輪郭を描画
        img = cv2.drawContours(img, max_contour, -1, (255, 0, 255), 3)

        # 線の縦横判定　最小値と最大値の差が大きいかを判断する
        downright = max_contour.max(axis=0)[0]
        upperleft = max_contour.min(axis=0)[0]



        # 輪郭領域の(横の長さ)-(縦の長さ)
        if (downright[0] - upperleft[0]) >= (downright[1] - upperleft[1]):
            contour_horizontal = True
        else:
            contour_horizontal = False




        # 水平と垂直と処理を分ける
        if contour_horizontal:
            gauge_list, res_img, point_text_list = horizontal_line(upperleft,downright,img,max_contour)
        else:
            gauge_list, res_img, point_text_list = vertical_line(upperleft,downright,img,max_contour)

        res_img = input_text(res_img,point_text_list)

        # デバッグ用　画像ファイルの表示
        # plt.figure(figsize=(8,8))
        # plt.xticks([]), plt.yticks([]) 
        # plt.imshow(res_img)

        #測定画像を出力
        cv2.imwrite(f"after/{output_file_name}",res_img)

        #CSV形式にて、[元画像ファイル名,出力画像ファイル名,縦横判定,白黒判定,線幅 X 10]
        gauge_item = [
            img_file_name.replace("before\\",''),
            output_file_name,
            '横'if contour_horizontal else '縦',
            '黒線' if is_black_line else '白線'
            ]
        gauge_item = gauge_item + gauge_list
        csvdata.append(gauge_item)
    
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    df = pd.DataFrame(csvdata)
    df.to_csv(f'after/result{timestamp}.csv')

if __name__ == "__main__":
    #背景白画像の際の、画像を二値化する際の境界値
    WHITE_BOUNDARY = 127
    #背景黒画像の際の、画像を二値化する際の境界値
    BLACK_BOUNDARY = 40
    main(WHITE_BOUNDARY,BLACK_BOUNDARY)