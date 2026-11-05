import matplotlib.pyplot as plt

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