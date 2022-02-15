# -*- coding: UTF-8 -*-
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
    # print(item.frequencies[1])
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

    with plt.style.context(['science', 'no-latex']):
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(w, S11_dB, lw=2.2, color='#000000', linestyle='--')
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
        ax.legend(['Target'],
                  prop={'size': 14, 'weight': 'roman'}, loc='lower left', facecolor='blue')
        ax.set_xlim(w[0], w[-1])
        ax.set_ylim(min(S11_dB)-7, 0)
        fig.savefig('../opti-site/src/assets/target.svg')
        fig.savefig('../opti-site/src/assets/target.png')
        # fig.savefig('./opti-site/src/imgs/target.svg')
    return w1,w2



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8888)
