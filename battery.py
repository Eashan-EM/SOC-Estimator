import pandas as pd
import numpy as np
from battery_graphs import *
from sklearn.preprocessing import StandardScaler

class A123_Battery:
    # Max capacity for 100% SOH is 1.1Ah
    MAX_CAP = 1.1
    # How many previous elements to consider for weighted average
    MAX_WEIGHTED_ELEM = 100
    
    def __init__(self, excel_file, temp, cell_no, type, out: str):
        # relative PATH to store the graphs
        self.output_path = out
        # A string identifin the battery, temperature
        self.temp = temp
        self.cell_no = cell_no
        # OCV or DPF
        self.type = type
        self.out = out
        
        print(excel_file)
        info = 0
        try:
            info = pd.read_excel(excel_file, sheet_name="Channel_1-005")
        except:
            info = pd.read_excel(excel_file, sheet_name="Channel_1-006")
            

        # Holds the index where battery is either 100% or 0% SOC
        self.max_min_idx = []
    
        self.time = info["Test_Time(s)"].to_numpy()
        current = info["Current(A)"].to_numpy()
        voltage = info["Voltage(V)"].to_numpy()
        charge = info["Charge_Capacity(Ah)"].to_numpy()
        discharge = info["Discharge_Capacity(Ah)"].to_numpy()

        self.min_vol = voltage[0]
        self.max_vol = voltage[0]

        blocks = 0
        start_counting = False

        # Weighted average
        weighted_v = []
        weighted_i = []

        intern_resistance = []
        delta_v = voltage[0]
        delta_i = current[0]
        for i, cur in enumerate(current):
            # Calculate the internal resistance
            delta_v = abs(delta_v-voltage[i])
            delta_i = abs(delta_i-cur)
            if delta_i==0:
                intern_resistance.append(intern_resistance[-1] if i!=0 else 0)
            else:
                intern_resistance.append(delta_v/delta_i)
            delta_v = voltage[i]
            delta_i = cur

            # Calculate weighted average of voltage and current
            weighted_v.append(sum(voltage[max(0, i-self.MAX_WEIGHTED_ELEM):i])/self.MAX_WEIGHTED_ELEM)
            weighted_i.append(sum(current[max(0, i-self.MAX_WEIGHTED_ELEM):i])/self.MAX_WEIGHTED_ELEM)

            # Finds blocks of sample when current is 0A. At low current, this should be closer to OCV
            if cur!=0:
                blocks = 0
                start_counting = False
            else:
                blocks += 1
                if blocks > 20 and not start_counting:
                    start_counting = True
                    self.max_min_idx.append(i)
                    self.max_vol = max(self.max_vol, voltage[i])
                    self.min_vol = min(self.min_vol, voltage[i])


        # Capacity of the battery under testing
        self.current_cap = max(discharge)
        self.soh = self.current_cap/self.MAX_CAP
        soc_charge = []
        # Checks if battery is initially chargin/discharging
        is_discharging = (voltage[self.max_min_idx[0]]>self.max_vol-0.5)
        curr_charge = self.current_cap if is_discharging else 0
        for i in range(len(self.max_min_idx)-1):
            for j in range(self.max_min_idx[i], self.max_min_idx[i+1]):
                # Convert to Ah
                curr_charge += current[j]*(self.time[j+1]-self.time[j])/3600
                soc_charge.append(max(0.0, min(1.0, curr_charge/self.current_cap)))
                #if j>self.max_min_idx[1]-200 and j<self.max_min_idx[1]+100:
                #    print(curr_charge, current[j], self.time[j+1], self.time[j], soc_charge[-1])
            is_discharging = not is_discharging
            
        self.soc_charge = np.reshape(soc_charge, (-1, 1))
        
        self.time = self.time[self.max_min_idx[0]:self.max_min_idx[-1]]
        self.current = np.reshape(current[self.max_min_idx[0]:self.max_min_idx[-1]], (-1, 1))
        self.voltage = np.reshape(voltage[self.max_min_idx[0]:self.max_min_idx[-1]], (-1, 1))
        self.intern_resistance = intern_resistance[self.max_min_idx[0]:self.max_min_idx[-1]]
        self.weighted_v = weighted_v[self.max_min_idx[0]:self.max_min_idx[-1]]
        self.weighted_i = weighted_i[self.max_min_idx[0]:self.max_min_idx[-1]]

        scaler = StandardScaler()
        self.voltage_norm = scaler.fit_transform(self.voltage)
        self.current_norm = scaler.fit_transform(self.current)

    def create_data(self, *args):
        return np.column_stack(args)
        
    def print_data(self):
        print(self.out)
        print(f"\t{'MIN Voltage':<15}: {self.min_vol:.2f}V\n\t{'MAX Voltage':<15}: {self.max_vol:.2f}V")
        print(f"\t{'Max Capacity':<15}: {self.current_cap:.4f}Ah")
        print(f"\t{'SOH':<15}: {self.soh:.5f}%")

    def draw_graphs(self):
        soc_volt_vs_time(self.max_min_idx[0], self.max_min_idx[1], self.soc_charge, self.voltage, self.time, self.output_path)
        soc_vs_volt(self.max_min_idx[0], self.max_min_idx[1], self.soc_charge, self.voltage, self.output_path)