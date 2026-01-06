import numpy as np
from scipy.special import erf
from monte_carlo import MonteCarloSimulator

# generates estimates and error percentages for a given simulator
def get_simulation_data(sim, true_val, n_values):
    estimates = [sim.estimate(n) for n in n_values]
    errors = [(abs(e - true_val) / true_val) * 100 for e in estimates]
    return np.array(estimates), np.array(errors)

def get_pi_task():
    return {
        "name": "Circle (Pi)",
        "sim": MonteCarloSimulator(lambda x, y: (x**2 + y**2) <= 1, [-1, 1, -1, 1]),
        "true_val": np.pi
    }

def get_parabola_task():
    return {
        "name": "Parabola",
        "sim": MonteCarloSimulator(lambda x, y: y < x**2, [0, 2, 0, 4]),
        "true_val": 8/3
    }

def get_gaussian_task():
    return {
        "name": "Gaussian",
        "sim": MonteCarloSimulator(lambda x, y: y < np.exp(-x**2), [0, 2, 0, 1]),
        "true_val": (np.sqrt(np.pi)/2) * erf(2)
    }

# estimates e using the expected length of decreasing sequences
def estimate_e(num_tests=10**6):
    u = np.random.rand(num_tests, 10)
    is_decreasing = u[:, :-1] > u[:, 1:]
    decreasing_chain = np.cumprod(is_decreasing, axis=1)
    n_values = np.sum(decreasing_chain, axis=1) + 2
    return np.mean(n_values)