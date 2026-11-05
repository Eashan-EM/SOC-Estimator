import matplotlib.pyplot as plt

def soc_pred_vs_actual(time, soc_actual, soc_pred, output_path):
    fig, ax1 = plt.subplots()

    color1 = "#1f77b4"
    ax1.set_xlabel("Time(s)")
    ax1.set_ylabel("SOC Actual(%)", color=color1)
    ax1.plot(time, soc_actual, color=color1, linewidth=2)
    ax1.tick_params(axis='y', labelcolor=color1)
    
    ax2 = ax1.twinx()

    color2 = "#ff7f0e"
    ax2.set_ylabel("SOC Predicted(%)", color=color2)
    ax2.plot(time, soc_pred, color=color2, linewidth=2)
    ax2.tick_params(axis='x', labelcolor=color2)

    fig.tight_layout()
    plt.savefig(f"output/models/{output_path}soc-actual-vs-pred.png")
    plt.close()