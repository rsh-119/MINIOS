import csv, os

def log_results(processes, algo):
    os.makedirs("data", exist_ok=True)
    path = "data/logs.csv"
    header = ["Algorithm", "PID", "AT", "BT", "WT", "TAT"]
    write_header = not os.path.exists(path)

    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        for p in processes:
            writer.writerow([algo, p.pid, p.arrival_time,
                             p.burst_time, p.waiting_time, p.turnaround_time])
