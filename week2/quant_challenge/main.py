import numpy as np
import matplotlib.pyplot as plt
from quant_engine import generate_gbm_paths, black_scholes_call, price_american_put_ls

# Configuration
S0, mu, sigma, T, steps, n_paths = 100, 0.05, 0.20, 1.0, 252, 50000

def print_section(title):
    print(f"\n{'='*55}\n{title.center(55)}\n{'='*55}")

# Simulation & Pricing
print_section("QUANTITATIVE PRICING ENGINE")
paths = generate_gbm_paths(S0, mu, sigma, T, steps, n_paths)

# Task 1 Visualization: Asset Paths
print("[*] Generating Asset Path Visualization...")

plt.figure(figsize=(10, 6))
time_grid = np.linspace(0, T, steps + 1)
plt.plot(time_grid, paths[:100, :].T, color='gray', alpha=0.4, linewidth=0.5)

mean_path = np.mean(paths, axis=0)
plt.plot(time_grid, mean_path, 'b--', linewidth=2, label='Simulated Mean Path')
expected_value = S0 * np.exp(mu * time_grid)
plt.plot(time_grid, expected_value, 'r-', linewidth=2, label='Expected Value $E[S_t]$')

plt.title("Geometric Brownian Motion: Simulation vs Theory")
plt.xlabel("Time (Years)")
plt.ylabel("Asset Price ($)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('asset_paths.png')
print("Asset path plot saved.")

# Task 2: European
bs_price = black_scholes_call(S0, 100, T, mu, sigma)
mc_price = np.exp(-mu * T) * np.mean(np.maximum(paths[:, -1] - 100, 0))

# Task 3: Asian
asian_price = np.exp(-mu * T) * np.mean(np.maximum(np.mean(paths, axis=1) - 100, 0))

# Task 4: American
american_put = price_american_put_ls(paths, 100, mu, T)

print(f"{'Black-Scholes Price':<35} | {bs_price:>12.4f}")
print(f"{'Monte Carlo (European)':<35} | {mc_price:>12.4f}")
print(f"{'Asian Call (Arithmetic)':<35} | {asian_price:>12.4f}")
print(f"{'American Put (L-S)':<35} | {american_put:>12.4f}")
print(f"{'='*55}")

print("[*] Generating Analysis Plots...")

# 1. Convergence Plot (Task 2)
n_vals = np.geomspace(100, 50000, 25).astype(int)
errors = [abs(np.exp(-mu*T)*np.mean(np.maximum(generate_gbm_paths(S0, mu, sigma, T, steps, n)[:,-1]-100, 0)) - bs_price) for n in n_vals]

plt.figure(figsize=(10, 5))
plt.loglog(n_vals, errors, 's-', color='darkblue', label='MC Error')
plt.loglog(n_vals, 1/np.sqrt(n_vals), '--', color='gray', label='Theoretical (1/√N)')
plt.title("Task 2: Error Convergence vs Number of Simulations")
plt.xlabel("N (Simulations)"); plt.ylabel("Absolute Price Error"); plt.legend(); plt.grid(True, which="both", alpha=0.3)
plt.savefig('convergence_plot.png')

# 2. Variance Reduction (Task 5)
def get_anti_err(N):
    eps = np.random.normal(0, 1, size=(N // 2, steps))
    shocks = np.concatenate([eps, -eps], axis=0)
    ST = S0 * np.exp(np.sum((mu - 0.5*sigma**2)*(T/steps) + sigma*shocks*np.sqrt(T/steps), axis=1))
    return np.std(np.exp(-mu*T)*np.maximum(ST-100, 0)) / np.sqrt(N)

N_vals_v = np.linspace(1000, 50000, 25).astype(int)
err_v = [np.std(np.exp(-mu*T)*np.maximum(generate_gbm_paths(S0, mu, sigma, T, steps, N)[:,-1]-100, 0))/np.sqrt(N) for N in N_vals_v]
err_a = [get_anti_err(N) for N in N_vals_v]

plt.figure(figsize=(10, 5))
plt.plot(N_vals_v, err_v, 'x-', label='Vanilla MC Error', color='orange')
plt.plot(N_vals_v, err_a, 'o-', label='Antithetic MC Error', color='green')
plt.title("Task 5: Variance Reduction Performance")
plt.xlabel("N (Simulations)"); plt.ylabel("Standard Error"); plt.legend(); plt.grid(alpha=0.3)
plt.savefig('variance_reduction.png')

print("Done. Images saved to directory.")