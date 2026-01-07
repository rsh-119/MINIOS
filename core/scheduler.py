from core.process import Process
from core.memory_manager import MemoryManager

class Scheduler:
    def __init__(self, processes, total_memory=512):
        self.processes = processes
        self.memory = MemoryManager(total_memory=total_memory)

    # ---------- FCFS ----------
    def fcfs(self):
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        current_time = 0
        for p in processes:
            # Simulate memory allocation before running
            self.memory.allocate(p, size=50)
            if current_time < p.arrival_time:
                current_time = p.arrival_time
            p.start_time = current_time
            p.finish_time = current_time + p.burst_time
            p.turnaround_time = p.finish_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            current_time = p.finish_time
            # Free memory when finished
            self.memory.free(p.pid)
        return processes

    # ---------- SJF ----------
    def sjf(self):
        processes = sorted(self.processes, key=lambda p: p.arrival_time)
        completed, time = [], 0
        ready_queue = []

        while len(completed) < len(processes):
            for p in processes:
                if p.arrival_time <= time and p not in completed and p not in ready_queue:
                    ready_queue.append(p)
            if ready_queue:
                ready_queue.sort(key=lambda p: p.burst_time)
                current = ready_queue.pop(0)
                self.memory.allocate(current, size=50)
                current.start_time = time
                time += current.burst_time
                current.finish_time = time
                current.turnaround_time = current.finish_time - current.arrival_time
                current.waiting_time = current.turnaround_time - current.burst_time
                completed.append(current)
                self.memory.free(current.pid)
            else:
                time += 1
        return completed

    # ---------- Round Robin ----------
    def round_robin(self, quantum=2):
        queue = sorted(self.processes, key=lambda p: p.arrival_time)
        time, completed = 0, []
        ready_queue = []

        # allocate all processes once at start
        for p in queue:
            self.memory.allocate(p, size=50)

        while queue or ready_queue:
            while queue and queue[0].arrival_time <= time:
                ready_queue.append(queue.pop(0))

            if ready_queue:
                p = ready_queue.pop(0)
                if p.remaining_time == 0:
                    continue
                if p.start_time == 0:
                    p.start_time = time
                exec_time = min(p.remaining_time, quantum)
                p.remaining_time -= exec_time
                time += exec_time
                if p.remaining_time == 0:
                    p.finish_time = time
                    p.turnaround_time = p.finish_time - p.arrival_time
                    p.waiting_time = p.turnaround_time - p.burst_time
                    completed.append(p)
                    self.memory.free(p.pid)
                else:
                    ready_queue.append(p)
            else:
                time += 1
        return completed

    # ---------- Averages ----------
    def calculate_averages(self, processes):
        n = len(processes)
        avg_wt = sum(p.waiting_time for p in processes) / n
        avg_tat = sum(p.turnaround_time for p in processes) / n
        return avg_wt, avg_tat
