
#インポートエリア######################################################
import cv2
from pathlib import Path
import pandas as pd

#定数エリア###########################################################
DIFF_RATIO = 1 #荷物判定の割合(% 3%なら3を指定)

#空のボックス画像を指定
EMPTYFILE = Path("../images/nimotsu0.jpeg").resolve()

#比較対象の画像を指定
FILE = Path("../images/nimotsu5.jpeg").resolve()

#####################################################################

def set_box(file:Path) -> dict:

    img = cv2.imread(str(file))

    box = dict()
    # 各ボックスの座標データ　左上から縦に１列ずつ合計40ボックス
    # 読み方：img[Y座標上:Y座標下, X座標左, X座標右]
    box[0]=img[1039:1296,96:885]
    box[1]=img[1309:1558,110:906]
    box[2]=img[1570:1810,142:916]
    box[3]=img[1816:2055,168:936]
    box[4]=img[2066:2294,193:948]
    box[5]=img[2303:2526,213:970]
    box[6]=img[2533:2747,245:982]
    box[7]=img[2761:2980,268:996]
    box[8]=img[1034:1290,920:1692]
    box[9]=img[1292:1553,936:1696]
    box[10]=img[1558:1795,950:1712]
    box[11]=img[1800:2041,970:1713]
    box[12]=img[2048:2281,984:1722]
    box[13]=img[2288:2512,990:1729]
    box[14]=img[2518:2734,1005:1732]
    box[15]=img[2748:2969,1018:1738]
    box[16]=img[1025:1284,1728:2486]
    box[17]=img[1291:1536,1729:2482]
    box[18]=img[1542:1782,1742:2476]
    box[19]=img[1784:2022,1746:2488]
    box[20]=img[2030:2260,1766:2472]
    box[21]=img[2264:2492,1756:2474]
    box[22]=img[2496:2724,1762:2468]
    box[23]=img[2724:2936,1768:2470]
    box[24]=img[1011:1268,2532:3285]
    box[25]=img[1272:1524,2524:3286]
    box[26]=img[1520:1776,2520:3248]
    box[27]=img[1778:2024,2520:3248]
    box[28]=img[2012:2252,2520:3230]
    box[29]=img[2244:2494,2516:3224]
    box[30]=img[2482:2708,2514:3210]
    box[31]=img[2712:2940,2508:3204]
    box[32]=img[994:1248,3316:4028]
    box[33]=img[1248:1508,3314:4020]
    box[34]=img[1510:1756,3300:4018]
    box[35]=img[1764:1998,3282:4012]
    box[36]=img[2004:2240,3274:3998]
    box[37]=img[2240:2468,3264:3964]
    box[38]=img[2482:2698,3246:3964]
    box[39]=img[2688:2910,3234:3954]
    return box

def make_emptyimage(box:dict):
    """荷物が入っているか比較する際の、空ポストの画像ファイルを作成します

    Args:
        box (dict): set_box関数で作成された各ポストの画像リスト
    """
    i = 0
    for chi_img in box.values():
        filename = Path(f'../images/empty/empty{i}.jpeg').resolve()
        cv2.imwrite(str(filename),chi_img)
        i += 1

def make_sourceimage(box:dict):
    """荷物が入っているか比較する際の、現在のポストの画像ファイルを作成します

    Args:
        box (dict): set_box関数で作成された各ポストの画像リスト
    """
    i = 0
    for chi_img in box.values():
        filename = Path(f'../images/source/source{i}.jpeg').resolve()
        cv2.imwrite(str(filename),chi_img)
        i += 1


def export_result(result:list):

    filename =  Path('./result/result.csv').resolve()
    if Path.exists(filename):
        stored_res = pd.read_csv(filename, header=None)
        res = stored_res.values.tolist()
        res.append(result)
        if len(res) > 3:
            res.pop(0)
        res = pd.DataFrame(res)
        # stored_res = stored_res.append(res)
        res.to_csv(filename,index=False,header=False)
    else:
        res = []
        res.append(result)
        res = pd.DataFrame(res)
        res.to_csv(filename,index=False,header=False)
    
    #3回連続のアラート情報がある場合、メッセージ表示
    if len(res) == 3:
        for i in range(len(res.iloc[0,:])):
            if res.iloc[0,i] and res.iloc[1,i] and res.iloc[2,i] :
                msg = f'{i} 番ポスト　郵送物あり'
                print(msg)

def compare_img(img_1, img_2) -> float:
    """_summary_

    Args:
        img_1: 郵便受けの画像
        img_2: 空の郵便受けの画像

    Returns:
        float: 画像の差の割合
    Examples:
        diff_ratio = compare_img(cv2.imread('nimotsu_output3.jpg'),cv2.imread('empty_output3.jpg'))
    """
    import cv2
    import os
    import numpy as np


    height = img_1.shape[0]
    width = img_1.shape[1]

    img_size = (int(width), int(height))

    # # 画像をリサイズする
    image1 = cv2.resize(img_1, img_size)
    image2 = cv2.resize(img_2, img_size)

    # ２画像の差異を計算
    im_diff = image1.astype(int) - image2.astype(int)

    #変化総量　要素ごとの　BGRの値を足し合わせる
    ratio = (np.abs(im_diff).sum()) / (im_diff.size * 255)
    return(ratio, im_diff)


def main():


    #空のボックス画像をボックス毎に切り分ける
    empty_box = set_box(EMPTYFILE)
    #空のボックス画像を比較用として作成する
    make_emptyimage(empty_box)

    #実行エリア

    box = set_box(FILE)
    make_sourceimage(box)


    import pandas as pd
    result = list()
    txt = f'画像相違割合 のしきい値は　 {DIFF_RATIO} %'
    print(txt)
    for i in range(len(box)):
        ratio, img_diff =compare_img(box[i], empty_box[i])
        filename = Path(f'../images/difference/difference{i}.jpeg').resolve()
        cv2.imwrite(str(filename),img_diff)
        txt = f'i = {i}  画像相違割合 = {(ratio * 100):.3g} %'
        print(txt)
        print((ratio * 100 > DIFF_RATIO))
        result.append(ratio * 100 > DIFF_RATIO)
        
    export_result(result)

if __name__ == '__main__':
    main()
