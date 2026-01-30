import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict
from blackjack_env import BlackjackEnv
import time

def run_off_policy_task(episodes):
    env = BlackjackEnv()
    
    # q(s,a) and cumulative denominator c(s,a)
    Q = defaultdict(lambda: np.zeros(4))
    C = defaultdict(lambda: np.zeros(4))
    
    # fixed exploration for behavior policy
    epsilon = 0.2 
    
    print(f"Training off-policy mc for {episodes} episodes...")
    start_time = time.time()
    
    for i in range(1, episodes + 1):
        state = env.reset()
        episode = []
        done = False
        
        # generate episode using behavior policy
        while not done:
            p_sum, d_card, ace, pair = state
            
            # identify legal moves
            legal = [0, 1]
            if len(episode) == 0:
                legal.append(2)
                if pair: legal.append(3)

            # calculate behavior probabilities
            probs = np.zeros(4)
            for action in legal:
                probs[action] = epsilon / len(legal)
                
            current_q = [Q[state][a] if a in legal else -float('inf') for a in range(4)]
            best_legal = np.argmax(current_q)
            probs[best_legal] += (1.0 - epsilon)
            
            action = np.random.choice(range(4), p=probs)
            prob_b = probs[action]
            
            next_state, reward, done = env.step(action)
            episode.append((state, action, reward, prob_b, legal))
            state = next_state
        
        # update q-values using weighted importance sampling
        G = 0.0
        W = 1.0
        for t in range(len(episode)-1, -1, -1):
            s, a, r, prob_b, legal_actions = episode[t]
            G += r
            
            C[s][a] += W
            Q[s][a] += (W / C[s][a]) * (G - Q[s][a])
            
            # check if action matches target policy (greedy)
            qs_legal = [Q[s][act] if act in legal_actions else -float('inf') for act in range(4)]
            if a != np.argmax(qs_legal):
                break
            
            W = W * (1.0 / prob_b)
            
        if i % 10000 == 0:
            print(f"\rProgress: {i}/{episodes} | Time: {time.time()-start_time:.0f}s", end="")

    print("\nTraining complete.")
    return Q

def plot_strategy(Q):
    dealer_range = range(2, 12)
    map_act = {0:'S', 1:'H', 2:'D', 3:'P'}
    
    def get_best(s, d, ace, pair):
        legal = [0, 1, 2]
        if pair: legal.append(3)
        
        if (s, d, ace, pair) not in Q: 
            return 'S' if s >= 17 else 'H'

        qs = Q[(s, d, ace, pair)]
        best_idx = legal[np.argmax([qs[x] for x in legal])]
        return map_act[best_idx]

    # hard totals
    hard = [[get_best(s, d, False, False) for d in dealer_range] for s in range(5, 20)]
    
    # soft totals
    soft = [[get_best(s, d, True, False) for d in dealer_range] for s in range(13, 21)]
    
    # pair configurations
    pair_configs = [
        (4, False), (6, False), (8, False), (10, False), (12, False), 
        (14, False), (16, False), (18, False), (20, False), (12, True)
    ]
    pairs = [[get_best(p_sum, d, is_ace, True) for d in dealer_range] for p_sum, is_ace in pair_configs]

    # labels for heatmap
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
    
    plt.title("off-policy optimal strategy", fontsize=15)
    plt.savefig("week5_strategy.png")
    print("'week5_strategy.png' saved.")

if __name__ == "__main__":
    Q_final = run_off_policy_task(5000000)
    plot_strategy(Q_final)