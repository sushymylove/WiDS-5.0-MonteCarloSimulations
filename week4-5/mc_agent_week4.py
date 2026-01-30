import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from blackjack_env import BlackjackEnv
import time

# task 1: mc prediction
def run_task_1(episodes=10000):
    env = BlackjackEnv()
    returns = defaultdict(list)
    # policy: stick if >= 20, else hit
    for _ in range(episodes):
        for target in [5, 21]:
            state = env.reset(force_player_sum=target)
            done = False
            total_r = 0
            while not done:
                action = 0 if state[0] >= 20 else 1
                state, reward, done = env.step(action)
                total_r += reward
            returns[target].append(total_r)
    print(f"Value of 21: {np.mean(returns[21]):.4f}") 
    print(f"Value of 5: {np.mean(returns[5]):.4f}")

# task 2: glie mc control
def run_task_2(episodes):
    env = BlackjackEnv()
    
    Q_sum = defaultdict(lambda: np.zeros(4))
    Q_count = defaultdict(lambda: np.zeros(4))
    Q = defaultdict(lambda: np.zeros(4))
    
    # epsilon decay setup
    epsilon = 1.0
    epsilon_min = 0.005 
    decay_steps = int(episodes * 0.4)
    decay_rate = (epsilon_min / epsilon) ** (1 / decay_steps)
    
    print(f"Training for {episodes} episodes...")
    start_time = time.time()
    rewards_history = []
    
    for i in range(1, episodes + 1):
        state = env.reset()
        episode = []
        done = False
        
        while not done:
            p_sum, d_card, ace, pair = state
            
            # identify legal moves
            legal = [0, 1] # stand, hit
            if len(episode) == 0:
                legal.append(2) # double
                if pair: legal.append(3) # split

            # epsilon-greedy choice
            if np.random.random() < epsilon:
                action = np.random.choice(legal)
            else:
                action = legal[np.argmax([Q[state][x] for x in legal])]

            next_state, reward, done = env.step(action)
            episode.append((state, action, reward))
            state = next_state
        
        # first-visit update
        G = 0
        visited = set()
        for t in range(len(episode)-1, -1, -1):
            s, a, r = episode[t]
            G += r
            if (s, a) not in visited:
                visited.add((s, a))
                Q_sum[s][a] += G
                Q_count[s][a] += 1
                Q[s][a] = Q_sum[s][a] / Q_count[s][a]
        
        if epsilon > epsilon_min:
            epsilon *= decay_rate
            
        if i % 10000 == 0:
            print(f"\rProgress: {i}/{episodes} | Epsilon: {epsilon:.4f}", end="")
            rewards_history.append(G) 

    print("\nTraining complete.")
    return Q, rewards_history

# task 3: visualization
def plot_strategy(Q):
    dealer_range = range(2, 12)
    map_act = {0:'S', 1:'H', 2:'D', 3:'P'}
    
    def get_best(s, d, ace, pair):
        legal = [0, 1, 2]
        if pair: legal.append(3)
        
        if (s, d, ace, pair) not in Q: 
            return 'S' if s >= 17 else 'H'

        qs = Q[(s, d, ace, pair)]
        legal_qs = np.array([qs[a] for a in legal])
        best_idx = legal[np.argmax(legal_qs)]
        return map_act[best_idx]

    # generate hard totals
    hard = []
    for s in range(5, 20):
        row = [get_best(s, d, False, False) for d in dealer_range]
        hard.append(row)
    
    # generate soft totals
    soft = []
    for s in range(13, 21):
        row = [get_best(s, d, True, False) for d in dealer_range]
        soft.append(row)
    
    # generate pairs
    pair_configs = [
        (4, False), (6, False), (8, False), (10, False), (12, False), 
        (14, False), (16, False), (18, False), (20, False), (12, True)
    ]
    pairs = [[get_best(p_sum, d, is_ace, True) for d in dealer_range] for p_sum, is_ace in pair_configs]

    # plot labels
    hard_labels = [str(i) for i in range(5, 20)]
    soft_labels = [f"A,{i-11}" for i in range(13, 21)]
    pair_labels = ["2,2","3,3","4,4","5,5","6,6","7,7","8,8","9,9","T,T","A,A"]
    
    all_data = hard + soft + pairs
    all_labels = hard_labels + soft_labels + pair_labels
    
    val_map = {'S':0, 'H':1, 'D':2, 'P':3}
    num_data = [[val_map[item] for item in row] for row in all_data]

    plt.figure(figsize=(10, 18))
    cmap = sns.color_palette(["#d62728", "#2ca02c", "#1f77b4", "#bcbd22"]) 
    
    sns.heatmap(num_data, annot=np.array(all_data), fmt="", 
                xticklabels=[2,3,4,5,6,7,8,9,10,'A'], 
                yticklabels=all_labels, cmap=cmap, cbar=False, linewidths=0.5, linecolor='gray')
    
    plt.title("optimal strategy", fontsize=15)
    plt.savefig("week4_strategy.png")
    print("'week4_strategy.png' saved.")

if __name__ == "__main__":
    run_task_1()
    Q_final, history = run_task_2(2000000)
    plot_strategy(Q_final)