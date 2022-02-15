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
    parameters: list

app = FastAPI()

# 接受 POST 类型
@app.post("/")
async def read_item(item: Item): # 参数类型是
    # print(item.parameters)
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    if item.parameters[0] == '' and item.parameters[4] == '':
        return 'non'
    elif item.parameters[0] != '' and item.parameters[4] == '':
        s = 'dnn'
    elif item.parameters[0] == '' and item.parameters[4] != '':
        s = 'cnn'
    else:
        s = 'd_cnn'

    f = np.linspace(0.5, 4.5, 251)
    new_model = keras.models.load_model('forward_2-8-8-new.h5')
    x = np.zeros([1, 5])
    S11_dnn_pre = np.zeros(251)
    S11_cnn_pre = np.zeros(251)

    def Pre(L1, L2 ,d12, d23):
        S11_pre = np.zeros(251)
        L1 = (L1-18)/(48-18)
        L2 = (L2-15.5)/(48.5-15.5)
        d12 = (d12-2)/(3.2-2)
        d23 = (d23-3.2)/(4.7-3.2)
        for i in range(251):
            x[0, 0] = L1
            x[0, 1] = L2
            x[0, 2] = d12
            x[0, 3] = d23
            x[0, 4] = (f[i]-0.5)/(4.5-0.5)
            S11_pre[i] = new_model.predict(x)
        return S11_pre

    if s == 'dnn':
        S11_dnn_pre = Pre(float(item.parameters[0]),float(item.parameters[1]),
                                float(item.parameters[2]),float(item.parameters[3]))
        names = ['Target', 'DNN Design']
    elif s == 'cnn':
        S11_cnn_pre = Pre(float(item.parameters[4]), float(item.parameters[5]),
                                float(item.parameters[6]), float(item.parameters[7]))
        names = ['Target', 'CNN Design']
    elif s == 'd_cnn':
        S11_dnn_pre = Pre(float(item.parameters[0]),float(item.parameters[1]),
                                float(item.parameters[2]),float(item.parameters[3]))
        S11_cnn_pre = Pre(float(item.parameters[4]), float(item.parameters[5]),
                                float(item.parameters[6]), float(item.parameters[7]))
        names = ['Target', 'DNN Design', 'CNN Design']

    w1 = float(item.parameters[8])
    w2 = float(item.parameters[9])
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

    with plt.style.context(['science', 'no-latex']):
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(w, S11_dB, lw=2.2, color='#000000', linestyle='--')
        if S11_dnn_pre.all() != 0:
            ax.plot(w, S11_dnn_pre, lw=2.7, color='firebrick')
        if S11_cnn_pre.all() != 0:
            ax.plot(w, S11_cnn_pre, lw=2.7, color='royalblue')
        ax.set_xlabel('Frequency (GHz)', fontdict={'family': 'Times New Roman', 'size': 20})
        ax.set_ylabel('$\mathregular{|S_{11}|}$  (dB)', fontdict={'family': 'Times New Roman', 'size': 20})
        ax.tick_params(direction='in', which='major', width=1, length=2.75, colors='black'
                       , labelsize=14, top=False, right=False)
        ax.tick_params(direction='in', which='minor', width=0.5, length=2, colors='black'
                       , labelsize=14, top=False, right=False)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Arial') for label in labels]
        xmajorLocator = MultipleLocator(0.5)
        ymajorLocator = MultipleLocator(10)
        ax.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax.xaxis.set_major_locator(xmajorLocator)
        ax.yaxis.set_major_locator(ymajorLocator)
        ax.legend(names,
                  prop={'size': 14, 'weight': 'roman'}, loc='lower left', facecolor='blue')
        ax.set_xlim(w[0], w[-1])
        ax.set_ylim(min(S11_dB)-7, 0)
        fig.savefig('../opti-site/src/assets/forward_prediction.svg')

    # return


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8884)
