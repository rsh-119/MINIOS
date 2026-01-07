import random
import csv
import numpy as np
import os

class QLearningScheduler:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.2):
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate
        self.q_table = {}       # (state, action): Q-value
        self.actions = ["FCFS", "SJF", "RR"]

    def get_state(self, num_processes, avg_burst):
        # Discretize the environment into states
        if num_processes <= 3:
            load = "LOW"
        elif num_processes <= 6:
            load = "MED"
        else:
            load = "HIGH"

        if avg_burst <= 3:
            burst_cat = "SHORT"
        elif avg_burst <= 6:
            burst_cat = "MED"
        else:
            burst_cat = "LONG"

        return (load, burst_cat)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_vals = [self.q_table.get((state, a), 0) for a in self.actions]
            return self.actions[np.argmax(q_vals)]

    def update(self, state, action, reward, next_state):
        current_q = self.q_table.get((state, action), 0)
        next_max_q = max([self.q_table.get((next_state, a), 0) for a in self.actions], default=0)
        new_q = (1 - self.alpha) * current_q + self.alpha * (reward + self.gamma * next_max_q)
        self.q_table[(state, action)] = new_q

    def train_from_logs(self, log_path="data/logs.csv"):
        if not os.path.exists(log_path):
            print("No logs found for training.")
            return
        with open(log_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                num_processes = int(row["PID"][1:])  # crude proxy if you logged sequentially
                burst = float(row["BT"])
                algo = row["Algorithm"]
                wt = float(row["WT"])
                tat = float(row["TAT"])
                reward = -wt  # we want to minimize waiting time
                state = self.get_state(num_processes, burst)
                self.update(state, algo, reward, state)
        print(f"Training complete! {len(self.q_table)} state-action pairs learned.")

    def decide_best_algorithm(self, num_processes, avg_burst):
        state = self.get_state(num_processes, avg_burst)
        best = self.choose_action(state)
        print(f"[🤖 AI Decision] Best algorithm for {state}: {best}")
        return best
