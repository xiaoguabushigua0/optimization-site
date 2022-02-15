import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
import cv2
from fastapi import FastAPI, Body, Form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator

app = FastAPI()

# 声明参数模型
class Item(BaseModel):
    frequencies: list

app = FastAPI()

# 接受 POST 类型
@app.post("/")
async def read_item(item: Item): # 参数类型是
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    num = 1
    w1 = float(item.frequencies[0])
    w2 = float(item.frequencies[1])
    w0 = (w1 + w2) / 2
    band_width = (w2 - w1) / w0
    w = np.linspace(0.5, 4.5, 251)
    w_ = (w / w0 - w0 / w) / band_width
    T4 = 8 * w_ * w_ * w_ * w_ - 8 * w_ * w_ + 1
    k_2 = 0.004  # 波纹高低
    P_LR = 1 + k_2 * T4 * T4
    delta = 0.0000  # 下沿高低
    S21_2 = 1 / (P_LR + delta)
    S11 = np.sqrt(1 - S21_2)
    S11_dB = 20 * np.log10(S11)

    S11 = np.zeros([1, 251])
    for i in range(1):
        for j in range(251):
            S11[i, j] = S11_dB[j]

    #### S11
    S11_pixels = np.zeros([num, 251, 251])
    for i in range(num):
        for j in range(251):
            if S11[i, j] >= 0:
                S11[i, j] = 0
            elif S11[i, j] <= -60:
                S11[i, j] = -60
            cow = math.ceil(-S11[i, j]/60 * 250)
            for k in range(cow):
                S11_pixels[i, k, j] = 255

    write_S11 = np.zeros([251, 251])
    for i in range(num):
        for j in range(251):
            for k in range(251):
                write_S11[j, k] = S11_pixels[i, j, k]
    img_1 = np.zeros([1, 251, 251, 3])
    new_img_1 = np.zeros([1, 251, 251, 3])
    for i in range(1):
        for j in range(251):
            for k in range(251):
                img_1[i,j,k,0] = S11_pixels[i, j, k]/255.
                new_img_1[i,j,k,0] = S11_pixels[i, j, k]/255.
    for i in range(1):
        for j in range(251):
            for k in range(251):
                if new_img_1[i,j,k,0] != 0:
                    new_img_1[i,j,k,1] = 70/255.
                    new_img_1[i,j,k,2] = 20/255.
    plt.imsave("./imgs/1.png", img_1[0,:,:,:])
    plt.imsave("./imgs/1x.png", new_img_1[0,:,:,:])

    #### kS11
    kS11_pixels = np.zeros([num, 251, 251])
    for i in range(num):
        k_max_positive = 0
        k_min_negative = 0
        k = np.zeros(250)
        for j in range(250):
            k[j] = S11[i, j+1] - S11[i, j]
            if np.abs(k[j]) < 1e-2:
                k[j] = 0
            if k[j] > 0 and k[j] > k_max_positive:
                k_max_positive = k[j]
            if k[j] < 0 and k[j] < k_min_negative:
                k_min_negative = k[j]
        k_max = max(k_max_positive, -k_min_negative)
        for j in range(250):
            if k[j] >= 0:
                cow = math.ceil(k[j]/k_max * 250)
                for m in range(cow):
                    kS11_pixels[i, m, j] = 255
                for n in range(251-cow):
                    kS11_pixels[i, cow+n, j] = 0
            else :
                cow = math.ceil(-k[j]/k_max * 250)
                for m in range(cow):
                    kS11_pixels[i, m, j] = 0
                for n in range(251-cow):
                    kS11_pixels[i, cow+n, j] = 255

    write_kS11 = np.zeros([251, 251])
    for i in range(num):
        for j in range(251):
            for k in range(251):
                write_kS11[j, k] = kS11_pixels[i, j, k]
    img_2 = np.zeros([1, 251, 251, 3])
    new_img_2 = np.zeros([1, 251, 251, 3])

    for i in range(1):
        for j in range(251):
            for k in range(251):
                img_2[i,j,k,1] = kS11_pixels[i, j, k]/255.
                new_img_2[i,j,k,1] = kS11_pixels[i, j, k]/255.

    for i in range(1):
        for j in range(251):
            for k in range(251):
                if new_img_2[i,j,k,1] != 0:
                    new_img_2[i,j,k,0] = 130/255.
                    new_img_2[i,j,k,2] = 20/255.
    plt.imsave("./imgs/2.png", img_2[0,:,:,:])
    plt.imsave("./imgs/2x.png", new_img_2[0,:,:,:])

    #### attention
    cow_max = 0
    S11_attention = np.zeros([num, 251, 251])
    for i in range(num):
        for j in range(251):
            if S11[i, j] >= 0:
                S11[i, j] = 0
            elif S11[i, j] <= -60:
                S11[i, j] = -60
            cow = math.ceil(-S11[i, j]/60 * 250)
            cow_max = max(cow, cow_max)
        for j in range(251):
            if S11[i ,j] <= -15:
                cow = math.ceil(-S11[i, j]/60 * 250)
                for k in range(cow):
                    S11_attention[i, k, j] = k * 255 / cow_max

    write_attention = np.zeros([251, 251])
    for i in range(num):
        for j in range(251):
            for k in range(251):
                write_attention[j, k] = S11_attention[i, j, k]
    img_3 = np.zeros([1, 251, 251, 3])
    new_img_3 = np.zeros([1, 251, 251, 3])
    for i in range(1):
        for j in range(251):
            for k in range(251):
                img_3[i,j,k,2] = S11_attention[i, j, k]/255.
                new_img_3[i,j,k,2] = S11_attention[i, j, k]/255.

    for i in range(1):
        for j in range(251):
            for k in range(251):
                if new_img_3[i,j,k,2] != 0:
                    new_img_3[i,j,k,0] = 50/255.
                    new_img_3[i,j,k,1] = 50/255.
    plt.imsave("./imgs/3.png", img_3[0,:,:,:])
    plt.imsave("./imgs/3x.png", new_img_3[0,:,:,:])

    #### merge
    train_imgs = np.zeros([1, 251, 251, 3])
    for i in range(1):
        for j in range(251):
            for k in range(251):
                train_imgs[i,j,k,0] = S11_pixels[i, j, k]/255.
                train_imgs[i,j,k,1] = kS11_pixels[i, j, k]/255.
                train_imgs[i,j,k,2] = S11_attention[i, j, k]/255.

    for i in range(num):
        plt.imsave("./imgs/merge.png", train_imgs[i,:,:,:])


    #######################################

    img1 = cv2.imread("./imgs/1x.png", -1)
    img2 = cv2.imread("./imgs/2x.png", -1)
    img3 = cv2.imread("./imgs/3x.png", -1)
    height, width = img1.shape[:2]
    fx = 1.817
    fy = 1.817
    enlarge1 = cv2.resize(img1, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    enlarge2 = cv2.resize(img2, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    enlarge3 = cv2.resize(img3, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("../opti-site/src/assets/1x.png", enlarge1)
    cv2.imwrite("../opti-site/src/assets/2x.png", enlarge2)
    cv2.imwrite("../opti-site/src/assets/3x.png", enlarge3)

    Img1 = cv2.imread("../opti-site/src/assets/1x.png")
    Img2 = cv2.imread("../opti-site/src/assets/2x.png")
    Img3 = cv2.imread("../opti-site/src/assets/3x.png")
    b1, g1, r1 = cv2.split(Img1)
    b2, g2, r2 = cv2.split(Img2)
    b3, g3, r3 = cv2.split(Img3)
    b = b1+b2+b3
    g = g1+g2+g3
    r = r1+r2+r3
    Img_merge = cv2.merge([b, g, r])

    cv2.imwrite("../opti-site/src/assets/mergex.png", Img_merge)

    img_a = cv2.imread("../opti-site/src/assets/mergex.png")
    img_b = cv2.imread("../opti-site/src/assets/target.png")
    h_titch= np.hstack((img_b, img_a))
    cv2.imwrite("../opti-site/src/assets/mergex1.png", h_titch)

    return {'merge':'mergex1', 'c1':'1x', 'c2':'2x', 'c3':'3x'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8886)
