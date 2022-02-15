# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Body, Form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import time
from tensorflow import keras
import scipy.signal as signal
from sko.DE import DE


app = FastAPI()

# 声明参数模型
class Item(BaseModel):
    parameters: list

app = FastAPI()

# 接受 POST 类型
@app.post("/")
async def read_item(item: Item): # 参数类型是
    start_time = time.time()

    w1 = float(item.parameters[6])
    w2 = float(item.parameters[7])
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

    uppers_y = S11_dB[signal.argrelextrema(S11_dB, np.greater)]
    uppers_x = signal.argrelextrema(S11_dB, np.greater)
    lowers_y = S11_dB[signal.argrelextrema(-S11_dB, np.greater)]
    lowers_x = signal.argrelextrema(-S11_dB, np.greater)

    F_ = []
    for j in range(4):
        F_.append(np.round(lowers_x[0][j] * (4.5 - 0.5) / 251 + 0.5,2))
    for i in range(3):
        F_.append(np.round(uppers_x[0][i] * (4.5 - 0.5) / 251 + 0.5,2))

    for i in range(7):
        F_[i] = (F_[i]-0.5)/(4.5-0.5)

    F = []
    gap = (F_[3]-F_[0])/3
    for i in range(4):
        F.append(F_[0]+gap*i)
    for i in range(3):
        F.append(F_[0]+gap/2+gap*i)

    y1 = -40
    y2 = -24
    new_model = keras.models.load_model('forward_2-8-8.h5')

    # 目标函数
    def mae(xx):
        x1, x2, x3, x4 = xx
        X = np.zeros([1, 5])
        S11_pre = np.zeros(1)
        X[0, 0] = x1
        X[0, 1] = x2
        X[0, 2] = x3
        X[0, 3] = x4

        X[0, 4] = F[0]
        S11_pre[0] = new_model.predict(X)
        g1 = np.abs(y1 - S11_pre[0])

        X[0, 4] = F[1]
        S11_pre[0] = new_model.predict(X)
        g2 = np.abs(y1 - S11_pre[0])

        X[0, 4] = F[2]
        S11_pre[0] = new_model.predict(X)
        g3 = np.abs(y1 - S11_pre[0])

        X[0, 4] = F[3]
        S11_pre[0] = new_model.predict(X)
        g4 = np.abs(y1 - S11_pre[0])

        X[0, 4] = F[4]
        S11_pre[0] = new_model.predict(X)
        g5 = np.abs(y2 - S11_pre[0])

        X[0, 4] = F[5]
        S11_pre[0] = new_model.predict(X)
        g6 = np.abs(y2 - S11_pre[0])

        X[0, 4] = F[6]
        S11_pre[0] = new_model.predict(X)
        g7 = np.abs(y2 - S11_pre[0])

        return g1 + g2 + g3 + g4 + g5 + g6 + g7

    inverse_L1 = float(item.parameters[2])
    inverse_L2 = float(item.parameters[3])
    inverse_d12 = float(item.parameters[4])
    inverse_d23 = float(item.parameters[5])

    min_bounds = [(inverse_L1 - 0.6 - 18) / (48 - 18), (inverse_L2 - 0.6 - 15.5) / (48.5 - 15.5),
                  0, 0]
    max_bounds = [(inverse_L1 + 0.6 - 18) / (48 - 18), (inverse_L2 + 0.6 - 15.5) / (48.5 - 15.5),
                  1, 1]

    de = DE(func=mae, n_dim=4, size_pop=20, max_iter=15,
            lb=min_bounds, ub=max_bounds, prob_mut=1, F=0.5)
    best_x, best_y = de.run()
    print('best_x is ', best_x, 'best_y is', best_y)
    print(best_x[0] * (48 - 18) + 18)
    print(best_x[1] * (48.5 - 15.5) + 15.5)
    print(best_x[2] * (3.2 - 2) + 2)
    print(best_x[3] * (4.7 - 3.2) + 3.2)
    end_time = time.time()
    print('用时：', end_time - start_time, '秒')

    return {'time':np.round(end_time - start_time),
            'L1':np.round(best_x[0] * (48 - 18) + 18,3),
            'L2':np.round(best_x[1] * (48.5 - 15.5) + 15.5,3),
            'd12':np.round(best_x[2] * (3.2 - 2) + 2,3),
            'd23':np.round(best_x[3] * (4.7 - 3.2) + 3.2,3), 'F':F_}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8878)
