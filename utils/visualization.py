import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
import os

# ---------- Static chart ----------
def gantt_chart(processes, title="CPU Scheduling Gantt Chart"):
    colors = {p.pid: "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
              for p in processes}
    plt.figure(figsize=(10, 3))
    plt.style.use("seaborn-v0_8-muted")

    for p in processes:
        plt.barh(1, p.burst_time, left=p.start_time,
                 color=colors[p.pid], edgecolor='black', height=0.5)
        plt.text(p.start_time + p.burst_time/2, 1, p.pid,
                 ha='center', va='center', color='white', fontsize=11, fontweight='bold')

    for t in range(0, max(p.finish_time for p in processes)+1):
        plt.axvline(x=t, color='gray', linestyle='--', alpha=0.3)

    plt.xlabel("Time Units")
    plt.title(title, fontsize=13, fontweight='bold', pad=15)
    plt.yticks([])
    plt.tight_layout()
    plt.show()


# ---------- Animated chart ----------
def animate_gantt(processes, title="CPU Scheduling Animation", save_as_gif=True):
    colors = {p.pid: "#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)])
              for p in processes}
    total_time = max(p.finish_time for p in processes)
    os.makedirs("reports", exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 3))
    plt.style.use("seaborn-v0_8-muted")

    bars = []
    for i, p in enumerate(processes):
        bar = ax.barh(i, 0, color=colors[p.pid], edgecolor='black', height=0.5)
        bars.append(bar[0])

    ax.set_xlim(0, total_time + 1)
    ax.set_yticks(range(len(processes)))
    ax.set_yticklabels([p.pid for p in processes])
    ax.set_xlabel("Time Units")
    ax.set_title(title, fontsize=13, fontweight='bold', pad=10)

    def update(frame):
        for i, p in enumerate(processes):
            if p.start_time <= frame <= p.finish_time:
                width = min(frame - p.start_time, p.burst_time)
                bars[i].set_width(width)
        ax.set_title(f"{title}  |  Time = {frame}", fontsize=13, fontweight='bold')
        return bars

    ani = animation.FuncAnimation(fig, update, frames=range(total_time+2),
                                  interval=700, blit=False, repeat=False)

    if save_as_gif:
        ani.save(f"reports/{title.replace(' ', '_')}.gif", writer="pillow", fps=2)
    plt.tight_layout()
    plt.show()
