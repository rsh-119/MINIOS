from core.process import Process
from core.scheduler import Scheduler
from core.logger import log_results
from utils.visualization import gantt_chart, animate_gantt
from ai_module.q_learning import QLearningScheduler


def get_processes():
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        at = int(input(f"Arrival time for P{i + 1}: "))
        bt = int(input(f"Burst time for P{i + 1}: "))
        processes.append(Process(f"P{i + 1}", at, bt))
    return processes


def print_table(processes):
    print("\nPID | AT | BT | ST | FT | WT | TAT")
    for p in processes:
        print(f"{p.pid:>3} | {p.arrival_time:>2} | {p.burst_time:>2} | "
              f"{p.start_time:>2} | {p.finish_time:>2} | "
              f"{p.waiting_time:>2} | {p.turnaround_time:>3}")


if __name__ == "__main__":
    # 🧠 Initialize AI Scheduler
    ai_scheduler = QLearningScheduler()
    ai_scheduler.train_from_logs("data/logs.csv")

    # 🧩 Get processes
    processes = get_processes()
    scheduler = Scheduler(processes)

    # 🧭 Menu
    print("\nChoose Scheduling Algorithm:")
    print("1. FCFS\n2. SJF\n3. Round Robin\n4. Let AI decide 🧠")
    choice = int(input("Enter choice (1-4): "))

    # ⚙️ Algorithm selection
    if choice == 1:
        result = scheduler.fcfs()
        algo_name = "First Come First Serve (FCFS)"
    elif choice == 2:
        result = scheduler.sjf()
        algo_name = "Shortest Job First (SJF)"
    elif choice == 3:
        quantum = int(input("Enter time quantum: "))
        result = scheduler.round_robin(quantum)
        algo_name = f"Round Robin (Quantum = {quantum})"
    elif choice == 4:
        avg_burst = sum(p.burst_time for p in processes) / len(processes)
        algo_name = ai_scheduler.decide_best_algorithm(len(processes), avg_burst)
        if algo_name == "FCFS":
            result = scheduler.fcfs()
        elif algo_name == "SJF":
            result = scheduler.sjf()
        else:
            quantum = int(input("Enter time quantum: "))
            result = scheduler.round_robin(quantum)
    else:
        print("Invalid choice.")
        exit()

    # 📊 Display process table
    print_table(result)

    # 📈 Average metrics
    avg_wt, avg_tat = scheduler.calculate_averages(result)
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

    # 💾 Memory usage report
    report = scheduler.memory.usage_report()
    print(f"\n💾 Memory Used: {report['used']} MB ({report['percent']}%) | Free: {report['free']} MB")

    # 🗂️ Log results for future AI learning
    log_results(result, algo_name)
    print("📘 Logged results to data/logs.csv")

    # 🎨 Visualizations
    gantt_chart(result, title=algo_name)
    animate_gantt(result, title=f"CPU Scheduling Animation - {algo_name}", save_as_gif=True)
