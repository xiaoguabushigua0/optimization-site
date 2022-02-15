# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Body, Form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
from sim_func import HFSS

app = FastAPI()

# 声明参数模型
class Item(BaseModel):
    parameters: list

app = FastAPI()

# 接受 POST 类型
@app.post("/")
async def read_item(item: Item): # 参数类型是
    # print(item.frequencies[1])
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    w1 = float(item.parameters[4])
    w2 = float(item.parameters[5])
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

    L1 = float(item.parameters[0])
    L2 = float(item.parameters[1])
    d12 = float(item.parameters[2])
    d23 = float(item.parameters[3])

    f_x = 6
    f_y = 18.7
    Ly = 3.17
    Lz = 1.52
    F_r = 3.55
    F_h = 19.05
    xian_r = 1.52
    box_x = L2 + f_x * 2
    box_y = f_y * 2 + Ly * 4 + d12 * 2 + d23
    box_h = 16
    filename = 2

    h = HFSS()
    h.change_project_name("project_" + str(filename))

    h.set_Variables_my("L1", L1)
    h.set_Variables_my("L2", L2)
    h.set_Variables_my("d12", d12)
    h.set_Variables_my("d23", d23)

    h.set_Variables_my("box_x", box_x)
    h.set_Variables_my("box_y", box_y)
    h.set_Variables_my("box_h", box_h)
    h.set_Variables_my("f_x", f_x)
    h.set_Variables_my("f_y", f_y)
    h.set_Variables_my("Ly", Ly)
    h.set_Variables_my("Lz", Lz)
    h.set_Variables_my("F_r", F_r)
    h.set_Variables_my("F_h", F_h)
    h.set_Variables_my("xian_r", xian_r)

    # draw airbox
    h.create_box1("airbox", "0", "0", "-box_h/2", "box_x", "box_y", "box_h")
    h.change_color("airbox", 143, 175, 143)
    h.change_transparent("airbox", 0.8)

    # draw metal poles
    h.create_box1("L1", "box_x", "f_y", "-Lz/2", "-L1", "Ly", "Lz")
    h.change_color("L1", 255, 128, 64)
    h.change_transparent("L1", 0.5)
    h.set_materials("L1", "pec")

    h.create_box1("L2", "0", "f_y+Ly+d12", "-Lz/2", "L2", "Ly", "Lz")
    h.change_color("L2", 255, 128, 64)
    h.change_transparent("L2", 0.5)
    h.set_materials("L2", "pec")

    h.create_box1("L3", "box_x", "f_y+Ly*2+d12+d23", "-Lz/2", "-L2", "Ly", "Lz")
    h.change_color("L3", 255, 128, 64)
    h.change_transparent("L3", 0.5)
    h.set_materials("L3", "pec")

    h.create_box1("L4", "0", "f_y+Ly*3+d12*2+d23", "-Lz/2", "L1", "Ly", "Lz")
    h.change_color("L4", 255, 128, 64)
    h.change_transparent("L4", 0.5)
    h.set_materials("L4", "pec")

    # draw choutou
    h.create_cylinder1("choutou1", "box_x", "f_y+Ly*0.5", "0",
                       "F_r", "F_h", "X")
    h.change_color("choutou1", 143, 175, 143)
    h.change_transparent("choutou1", 0.8)
    h.create_cylinder1("choutou2", "0", "f_y+Ly*3.5+d12*2+d23", "0",
                       "F_r", "-F_h", "X")
    h.change_color("choutou2", 143, 175, 143)
    h.change_transparent("choutou2", 0.8)

    # draw xian
    h.create_cylinder1("xian1", "box_x+F_h", "f_y+Ly*0.5", "0",
                       "xian_r", "-F_h", "X")
    h.change_color("xian1", 255, 128, 64)
    h.change_transparent("xian1", 0.5)
    h.create_cylinder1("xian2", "0", "f_y+Ly*3.5+d12*2+d23", "0",
                       "xian_r", "-F_h", "X")
    h.change_color("xian2", 255, 128, 64)
    h.change_transparent("xian2", 0.5)

    # unite
    h.unite("airbox", "choutou1")
    h.unite("airbox", "choutou2")
    h.unite("L1", "xian1")
    h.unite("L4", "xian2")

    # set port
    h.set_waveport("1", 149)
    h.set_waveport("2", 157)

    # set analysis
    h.set_analysis(2.5, 20, 0.02, 3, 3)
    h.set_fast_frequency_sweep1("Setup1", 0.5, 4.5, 251, False)
    h.run()
    h.create_report_S11_S21()
    h.save_report_to_csv("D:/UI_learning/optimizaiton_site/12-25/filter_files/optimization_hfss.csv")

    read1 = np.zeros(251)
    df1 = pd.read_csv("D:/UI_learning/optimizaiton_site/12-25/filter_files/optimization_hfss.csv", header=None)
    DF1 = df1.values
    for i in range(251):
        read1[i] = DF1[i + 1, 1]

    F = item.parameters[6]
    for i in range(7):
        F[i] = F[i]*(4.5-0.5)+0.5

    with plt.style.context(['science', 'no-latex']):
        fig, ax = plt.subplots(figsize=(6, 5))
        ax.plot(w, S11_dB, lw=2.2, color='#000000', linestyle='--')
        ax.plot(w, read1, lw=2.7, color='firebrick')
        ax.plot(F[0], -40, 'o',markersize=10, markeredgecolor='cadetblue', markerfacecolor='cadetblue')
        ax.plot(F[1], -40, 'o',markersize=10, markeredgecolor='cadetblue', markerfacecolor='cadetblue')
        ax.plot(F[2], -40, 'o',markersize=10, markeredgecolor='cadetblue', markerfacecolor='cadetblue')
        ax.plot(F[3], -40, 'o',markersize=10, markeredgecolor='cadetblue', markerfacecolor='cadetblue')
        ax.plot(F[4], -24, 'o', markersize=10, markeredgecolor='darkorange', markerfacecolor='darkorange')
        ax.plot(F[5], -24, 'o', markersize=10, markeredgecolor='darkorange', markerfacecolor='darkorange')
        ax.plot(F[6], -24, 'o', markersize=10, markeredgecolor='darkorange', markerfacecolor='darkorange')
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
        ax.legend(['Target', 'Optimization-HFSS'],
                  prop={'size': 14, 'weight': 'roman'}, loc='lower left', facecolor='blue')
        ax.set_xlim(w[0], w[-1])
        ax.set_ylim(min(S11_dB)-7, 0)
        fig.savefig('../opti-site/src/assets/optimization_hfss.svg')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8880)
