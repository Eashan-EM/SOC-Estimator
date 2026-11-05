import pandas as pd
import numpy as np
import openpyxl
from battery_graphs import *
from FNN import FNN

class Battery:
    MAX_CAP = 1.1
    def __init__(self, excel_file, channel, iden, out):
        self.output_path = out
        self.identifier = iden
        info = pd.read_excel(excel_file, sheet_name=channel)

        self.data = info[["Current(A)", "Voltage(V)"]].to_numpy()
        self.time = info["Test_Time(s)"]
        self.current = info["Current(A)"]
        self.voltage = info["Voltage(V)"]
        self.charge = info["Charge_Capacity(Ah)"]
        discharge = info["Discharge_Capacity(Ah)"]

        self.min_vol = self.voltage[0]
        self.max_vol = self.voltage[0]

        blocks = 0
        start_counting = False
        self.voltage_index = []
        intern_resistance = []
        delta_v = self.voltage[0]
        delta_i = self.current[0]
        for i, cur in enumerate(self.current):
            delta_v = abs(delta_v-self.voltage[i])
            delta_i = abs(delta_i-self.voltage[i])
            if delta_i==0:
                intern_resistance.append(intern_resistance[-1])
            else:
                intern_resistance.append(delta_v/delta_i)
            delta_v = self.voltage[i]
            delta_i = self.current[i]
            if cur!=0:
                blocks = 0
                start_counting = False
            else:
                blocks += 1
                if blocks > 20 and not start_counting:
                    start_counting = True
                    self.voltage_index.append(i)
                    if self.voltage[i]>self.max_vol:
                        self.max_vol = self.voltage[i]
                    elif self.voltage[i]<self.min_vol:
                        self.min_vol = self.voltage[i]

        self.data = np.column_stack((self.data, np.array(intern_resistance)))
        self.data = self.data[self.voltage_index[0]:self.voltage_index[-1]]
        self.time = self.time[self.voltage_index[0]:self.voltage_index[-1]]

        self.current_cap = max(discharge)
        self.soh = self.current_cap/self.MAX_CAP
        soc_charge = []
        for i in range(self.voltage_index[0], self.voltage_index[1]):
            soc_charge.append(1-discharge[i]/self.current_cap)
        for i in range(self.voltage_index[1], self.voltage_index[2]):
            soc_charge.append(self.charge[i]/self.current_cap)
        self.soc_charge = np.array(soc_charge).reshape(-1, 1)

    def print_data(self):
        print(self.identifier)
        print(f"\t{'MIN Voltage':<15}: {self.min_vol:.2f}V\n\t{'MAX Voltage':<15}: {self.max_vol:.2f}V")
        print(f"\t{'Max Capacity':<15}: {self.current_cap:.4f}Ah")
        print(f"\t{'SOH':<15}: {self.soh:.5f}%")

    def draw_graphs(self):
        soc_volt_vs_time(self.voltage_index[0], self.voltage_index[1], self.soc_charge, self.voltage, self.time, self.output_path)
        soc_vs_volt(self.voltage_index[0], self.voltage_index[1], self.soc_charge, self.voltage, self.output_path)



LC_OCV_007 = Battery("data/LC-OCV/OCV0-20120618/A1-007-OCV0-20120618.xlsx", "Channel_1-005", "0 degree;LC-OCV;Cell 007", "LC-OCV-007-0/")
LC_OCV_007.print_data();
#LC_OCV_007.draw_graphs()

LC_OCV_008 = Battery("data/LC-OCV/OCV0-20120618/A1-008-OCV0-20120618.xlsx", "Channel_1-006", "0 degree;LC-OCV;Cell 008", "LC-OCV-008-0/")
LC_OCV_008.print_data();
#LC_OCV_008.draw_graphs()

xtrain = LC_OCV_007.data
ytrain = LC_OCV_007.soc_charge
split_at = int(len(LC_OCV_008.data)*0.85)
xval = LC_OCV_008.data[split_at:]
yval = LC_OCV_008.soc_charge[split_at:]
xtest = LC_OCV_008.data[:split_at]
ytest = LC_OCV_008.soc_charge[:split_at]
fnn = FNN(xtrain, ytrain, xval, yval, xtest, ytest);
fnn.train()
fnn.save()
fnn.evaluate()
fnn.predict(LC_OCV_008.time[:split_at])
