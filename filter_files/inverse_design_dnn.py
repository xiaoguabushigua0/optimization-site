# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Body, Form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
from tensorflow import keras

app = FastAPI()

# 声明参数模型
class Item(BaseModel):
    frequencies: list

app = FastAPI()

# 接受 POST 类型
@app.post("/")
async def read_item(item: Item): # 参数类型是
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
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
    S11_tar = np.zeros([1, 251])
    for i in range(251):
        S11_tar[0, i] = S11_dB[i]

    model = keras.models.load_model('900+3600_2-18-5.h5')
    struc_pre = model.predict(S11_tar)
    origin_struc = struc_pre
    struc_pre[:, 0] = struc_pre[:, 0] * (48 - 18) + 18
    struc_pre[:, 1] = struc_pre[:, 1] * (48.5 - 15.5) + 15.5
    struc_pre[:, 2] = struc_pre[:, 2] * (3.2 - 2) + 2
    struc_pre[:, 3] = struc_pre[:, 3] * (4.7 - 3.2) + 3.2

    # return str(struc_pre[0])
    return {'L1':str(round(struc_pre[0][0],3)), 'L2':str(round(struc_pre[0][1],3)),
            'd12':str(round(struc_pre[0][2],3)), 'd23':str(round(struc_pre[0][3],3))}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8887)
