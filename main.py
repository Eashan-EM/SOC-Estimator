import pandas as pd
import numpy as np
import openpyxl
from battery_graphs import *
from battery import A123_Battery
from FNN import FNN
from LSTM_RNN import LSTM_RNN
from pathlib import Path

batteries = []
def get_all_files(folder_path):
    for item in folder_path.iterdir():
        if "~" in item.name:
            continue
        
        if item.is_file():
            path = str(item.absolute())
            name = item.name.split("-")
            batteries.append(A123_Battery(path, name[2][3:], name[1], name[2], f"{name[2]}-{name[2][3:]}-{name[1]}"))
        else:
            get_all_files(item.absolute())
get_all_files(Path("./data/LC-OCV/OCV0-20120618/"))

min_len = min([len(obj.soc_charge) for obj in batteries])

data = [batt.create_data(batt.current, batt.voltage) for batt in batteries]

def create_seq(x, y, history):
    xs = []
    ys = []

    for i in range(len(x)-history):
        xs.append(x[i:i+history])
        ys.append(y[i:i+history])

    return np.asarray(xs, dtype=np.float32), np.asarray(ys, dtype=np.float32)
    
xtrain, ytrain = create_seq(data[0], batteries[0].soc_charge, 50)
x2, y2 = create_seq(data[1], batteries[1].soc_charge, 50)
split_at = int(len(data[1])*0.85)
xval = x2[split_at:]
yval = y2[split_at:]
xtest = x2[:split_at]
ytest = y2[:split_at]

time = batteries[1].time[:split_at]

lstm = LSTM_RNN(xtrain, ytrain, xval, yval, xtest, ytest)
lstm.train()
lstm.save()
lstm.evaluate()
lstm.predict(time)