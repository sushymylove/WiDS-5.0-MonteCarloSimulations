import numpy as np
import matplotlib.pyplot as plt
from task_logic import get_simulation_data, get_pi_task, get_parabola_task, get_gaussian_task, estimate_e

def plot_convergence(n_values, estimates, errors, true_val, title, filename):
    plt.figure(figsize=(12, 5))
    
    # value convergence plot
    plt.subplot(1, 2, 1)
    plt.semilogx(n_values, estimates, '-o', markersize=4, alpha=0.7, label='Estimate')
    plt.axhline(y=true_val, color='r', linestyle='--', label='True Value')
    plt.xlabel('N (Log Scale)')
    plt.ylabel('Value')
    plt.title(f'{title} Convergence')
    plt.legend()

    # log-log error analysis
    plt.subplot(1, 2, 2)
    plt.loglog(n_values, errors, '-s', markersize=4, color='orange', label='Actual Error')
    plt.loglog(n_values, 100/np.sqrt(n_values), color='gray', linestyle=':', label=r'$1/\sqrt{N}$ Trend')
    plt.xlabel('N (Log Scale)')
    plt.ylabel('Error (%)')
    plt.title(f'{title} Error Analysis')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def run_assignments():
    n_values = np.geomspace(10, 10**6, 40).astype(int)
    tasks = [get_pi_task(), get_parabola_task(), get_gaussian_task()]

    # run and plot standard MC tasks
    for task in tasks:
        print(f"--- {task['name']} ---")
        estimates, errors = get_simulation_data(task['sim'], task['true_val'], n_values)
        
        final_estimate = task['sim'].estimate(10**7)
        print(f"Estimate:       {final_estimate:.8f}")
        print(f"True Value:     {task['true_val']:.8f}")
        print(f"Absolute Error: {abs(final_estimate - task['true_val']):.8f}\n")
        
        plot_filename = f"{task['name'].lower().replace(' ', '_')}_plot.png"
        plot_convergence(n_values, estimates, errors, task['true_val'], task['name'], plot_filename)

    # specific output for e
    e_estimate = estimate_e()
    print(f"--- e Estimation ---")
    print(f"Estimate:       {e_estimate:.8f}")
    print(f"True Value:     {np.e:.8f}")
    print(f"Absolute Error: {abs(e_estimate - np.e):.8f}")

if __name__ == "__main__":
    run_assignments()