# -*- coding: UTF-8 -*-
from fastapi import FastAPI, Body, Form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, AutoMinorLocator
from tensorflow import keras
import math
from matplotlib import cm
import cv2
from keras.models import load_model

app = FastAPI()

# 声明参数模型
class Item(BaseModel):
    name: str

app = FastAPI()

# 接受 POST 类型
@app.post("/")
async def read_item(item: Item): # 参数类型是
    # 加载测试数据并进行相同预处理操作
    name = item.name
    image = cv2.imread(name)
    image = cv2.resize(image, (251, 251))
    # scale图像数据
    image = image.astype("float") / 255.0
    # 对图像进行拉平操作
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # 读取模型和标签
    model = load_model('resnet_34_500epo_min_loss.h5')
    # 预测
    preds = model.predict(image)
    print(preds)

    return {'L1':str(round(preds[0][0] * (48 - 18) + 18,3)),
            'L2':str(round(preds[0][1] * (48.5 - 15.5) + 15.5,3)),
            'd12':str(round(preds[0][2] * (3.2 - 2) + 2,3)),
            'd23':str(round(preds[0][3] * (4.7 - 3.2) + 3.2,3))}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.1.101", port=8885)
