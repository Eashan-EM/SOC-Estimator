import pandas as pd
import numpy as np
import openpyxl
from battery_graphs import *
from battery import A123_Battery
from FNN import FNN
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
get_all_files(Path("./data/LC-OCV"))

min_len = min([len(obj.soc_charge) for obj in batteries])
soc_temp_map(
    batteries[0].time[0:min_len], 
    [obj.soc_charge[0:min_len] for obj in batteries], 
    [obj.out for obj in batteries], 
    "temp_map.png")