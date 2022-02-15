# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Body, Form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
import geatpy as ea
import time
from tensorflow import keras
import scipy.signal as signal

app = FastAPI()

# 声明参数模型
class Item(BaseModel):
    parameters: list

app = FastAPI()

# 接受 POST 类型
@app.post("/")
async def read_item(item: Item): # 参数类型是
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

    # 目标函数
    def aim(Phen):  # 传入种群染色体矩阵解码后的基因表现型矩阵
        y1 = -40
        y2 = -24
        Y = [y1, y1, y1, y1, y2, y2, y2]
        new_model = keras.models.load_model('forward_2-8-8.h5')
        fre_num = 6
        x1 = Phen[:, [0]]
        x2 = Phen[:, [1]]
        x3 = Phen[:, [2]]
        x4 = Phen[:, [3]]
        pop_num = len(x1)
        X = np.zeros([pop_num, fre_num, 5])
        S11_pre = np.zeros([pop_num, fre_num])
        G = np.zeros([pop_num, fre_num])
        func_sum = np.zeros(pop_num)
        func = np.zeros([pop_num, 1])
        str_fre = np.zeros([1, 5])
        for i in range(pop_num):
            X[i, :, 0] = x1[i]
            X[i, :, 1] = x2[i]
            X[i, :, 2] = x3[i]
            X[i, :, 3] = x4[i]
            for j in range(4):
                X[i, j, 4] = F[j]
                str_fre[0, :] = X[i, j, :]
                S11_pre[i, j] = new_model.predict(str_fre)
                G[i, j] = np.abs(S11_pre[i, j] - Y[j])
            for j in range(2):
                X[i, j + 4, 4] = F[j + 4]
                str_fre[0, :] = X[i, j + 4, :]
                S11_pre[i, j + 4] = new_model.predict(str_fre)
                G[i, j + 4] = (S11_pre[i, j + 4] - Y[j + 4])
                if G[i, j + 4] < -3:
                    G[i, j + 4] = 0
        for i in range(pop_num):
            for j in range(fre_num):
                func_sum[i] = func_sum[i] + G[i, j]
        for i in range(pop_num):
            func[i, 0] = func_sum[i]
        return func

    L1 = float(item.parameters[2])
    L2 = float(item.parameters[3])
    d12 = float(item.parameters[4])
    d23 = float(item.parameters[5])

    x1 = [(L1 - 1.2 - 18) / (48 - 18), (L1 - 0.3 - 18) / (48 - 18)]
    x2 = [(L2 - 0.1 - 15.5) / (48.5 - 15.5), (L2 + 1 - 15.5) / (48.5 - 15.5)]
    x3 = [(2 - 2) / (3.2 - 2), (2.5 - 2) / (3.2 - 2)]
    x4 = [(3.2 - 3.2) / (4.7 - 3.2), (3.6 - 3.2) / (4.7 - 3.2)]
    b1 = [1, 1]
    b2 = [1, 1]
    b3 = [1, 1]  # 第一个决策变量边界，1表示包含范围的边界，0表示不包含
    b4 = [1, 1]  # 第二个决策变量边界，1表示包含范围的边界，0表示不包含

    # 生成自变量的范围矩阵，使得第一行为所有决策变量的下界，第二行为上界
    ranges = np.vstack([x1, x2, x3, x4]).T
    # 生成自变量的边界矩阵

    borders = np.vstack([b1, b2, b3, b4]).T
    varTypes = np.array([0, 0, 0, 0])  # 决策变量的类型，0表示连续，1表示离散
    """==========================染色体编码设置========================="""
    Encoding = 'BG'
    # 'BG'表示采用二进制/格雷编码
    codes = [1, 1, 1, 1]  # 决策变量的编码方式，两个1表示变量均使用格雷编码
    precisions = [6, 6, 6, 6]  # 决策变量的编码精度，表示解码后能表示的决策变量的精度可达到小数点后6位
    scales = [0, 0, 0, 0]  # 0表示采用算术刻度，1表示采用对数刻度
    # 调用函数创建译码矩阵
    FieldD = ea.crtfld(Encoding, varTypes, ranges, borders, precisions, codes, scales)
    # """=========================遗传算法参数设置========================"""
    NIND = int(item.parameters[0])  # 种群个体数目
    MAXGEN = int(item.parameters[1])  # 最大遗传代数
    maxormins = np.array([1])  # 表示目标函数是最小化，元素为-1则表示对应的目标函数是最大化
    selectStyle = 'sus'  # 采用随机抽样选择
    recStyle = 'xovdp'  # 采用两点交叉
    mutStyle = 'mutbin'  # 采用二进制染色体的变异算子
    Lind = int(np.sum(FieldD[0, :]))  # 计算染色体长度
    pc = 1  # 交叉概率
    pm = 0.9*Lind / Lind  # 变异概z率
    obj_trace = np.zeros((MAXGEN, 2))  # 定义目标函数值记录器
    var_trace = np.zeros((MAXGEN, Lind))  # 染色体记录器，记录历代最优个体的染色体
    """=========================开始遗传算法进化========================"""
    start_time = time.time()  # 开始计时
    Chrom = ea.crtpc(Encoding, NIND, FieldD)  # 生成种群染色体矩阵
    variable = ea.bs2ri(Chrom, FieldD)  # 对初始种群进行解码
    ObjV = aim(variable)  # 计算初始种群个体的目标函数值
    best_ind = np.argmin(ObjV)  # 计算当代最优个体的序号
    # 开始进化
    for gen in range(MAXGEN):
        FitnV = ea.ranking(maxormins * ObjV)  # 根据目标函数大小分配适应度值
        SelCh = Chrom[ea.selecting(selectStyle, FitnV, NIND - 1), :]  # 选择
        SelCh = ea.recombin(recStyle, SelCh, pc)  # 重组
        SelCh = ea.mutate(mutStyle, Encoding, SelCh, pm)  # 变异
        # #把父代精英个体与子代的染色体进行合并，得到新一代种群
        Chrom = np.vstack([Chrom[best_ind, :], SelCh])
        Phen = ea.bs2ri(Chrom, FieldD)  # 对种群进行解码(二进制转十进制)
        ObjV = aim(Phen)  # 求种群个体的目标函数值#记录
        best_ind = np.argmin(ObjV)  # 计算当代最优个体的序号
        obj_trace[gen, 0] = np.sum(ObjV) / ObjV.shape[0]  # 记录当代种群的目标函数均值
        obj_trace[gen, 1] = ObjV[best_ind]  # 记录当代种群最优个体目标函数值
        var_trace[gen, :] = Chrom[best_ind, :]  # 记录当代种群最优个体的染色体
    # 进化完成

    """============================输出结果============================"""
    best_gen = np.argmin(obj_trace[:, [1]])
    print('最优解的目标函数值：', obj_trace[best_gen, 1])
    variable = ea.bs2ri(var_trace[[best_gen], :], FieldD)
    # 解码得到表现型（即对应的决策变量值）
    print('最优解的决策变量值为：')

    print('L1 =', variable[0, 0] * (48 - 18) + 18)
    print('L2 =', variable[0, 1] * (48.5 - 15.5) + 15.5)
    print('d12 =', variable[0, 2] * (3.2 - 2) + 2)
    print('d23 =', variable[0, 3] * (4.7 - 3.2) + 3.2)

    end_time = time.time()  # 结束计时
    # ea.trcplot(obj_trace, [['种群个体平均目标函数值', '种群最优个体目标函数值']])  # 绘制图像
    print('用时：', end_time - start_time, '秒')

    return {'time':np.round(end_time - start_time),
            'L1':np.round(variable[0, 0] * (48 - 18) + 18,3),
            'L2':np.round(variable[0, 1] * (48.5 - 15.5) + 15.5,3),
            'd12':np.round(variable[0, 2] * (3.2 - 2) + 2,3),
            'd23':np.round(variable[0, 3] * (4.7 - 3.2) + 3.2,3), 'F':F_}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8882)
