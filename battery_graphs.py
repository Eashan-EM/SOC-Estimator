import matplotlib.pyplot as plt
import random

def soc_volt_vs_time(start_idx, end_idx, soc, voltage, time, output_path):
    fig, ax1 = plt.subplots()

    color1 = "#1f77b4"
    ax1.set_xlabel("Time(s)")
    ax1.set_ylabel("SOC(%)", color=color1)
    ax1.plot(time[start_idx:end_idx], soc, color=color1, linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color1)
    
    ax2 = ax1.twinx()

    color2 = "#ff7f0e"
    ax2.set_ylabel("Voltage(V)", color=color2)
    ax2.plot(time[start_idx:end_idx], voltage[start_idx:end_idx], color=color2, linewidth=2)
    ax2.tick_params(axis='x', labelcolor=color2)

    fig.tight_layout()
    plt.savefig(f"output/battery/{output_path}soc-volt-vs-time.png")
    plt.close()

def soc_vs_volt(start_idx, end_idx, soc, voltage, output_path):
    plt.plot(voltage[start_idx:end_idx], soc, color="black", ls="solid")
    plt.xlabel("Voltage(V)")
    plt.ylabel("SOC(%)")

    plt.savefig(f"output/battery/{output_path}soc_voltage.png")
    plt.close()

def soc_temp_map(time, socs, legends, output_path):
    for i, soc in enumerate(socs):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        plt.plot(time, soc, color=color, ls="solid", label=legends[i])
        plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        plt.xlabel("Time(S)")
        plt.ylabel("SOC(%)")
    plt.tight_layout()
    plt.savefig(f"output/battery/{output_path}")