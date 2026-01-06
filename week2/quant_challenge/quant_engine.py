import numpy as np
from scipy.stats import norm

def generate_gbm_paths(S0, mu, sigma, T, steps, n_paths):
    """Task 1: Vectorized GBM Simulation"""
    dt = T / steps
    shocks = np.random.normal(0, np.sqrt(dt), size=(n_paths, steps))
    # Ito's Lemma formulation
    drift = (mu - 0.5 * sigma**2) * dt
    diffusion = sigma * shocks
    log_returns = np.cumsum(drift + diffusion, axis=1)
    log_returns = np.insert(log_returns, 0, 0, axis=1) 
    return S0 * np.exp(log_returns)

def black_scholes_call(S, K, T, r, sigma):
    """Task 2: Closed-form solution for sanity check"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def price_american_put_ls(paths, K, r, T):
    """Task 4: Longstaff-Schwartz using Matrix Algebra"""
    n_paths, n_steps = paths.shape
    dt = T / (n_steps - 1)
    df = np.exp(-r * dt)
    
    cash_flows = np.maximum(K - paths[:, -1], 0)
    
    for t in range(n_steps - 2, 0, -1):
        itm = np.where(paths[:, t] < K)[0]
        if len(itm) < 3: continue
            
        X = paths[itm, t]
        Y = cash_flows[itm] * df
        
        # Regression: Continuation Value ~ c0 + c1*S + c2*S^2
        A = np.column_stack([np.ones_like(X), X, X**2])
        coeffs = np.linalg.lstsq(A, Y, rcond=None)[0]
        continuation_val = A @ coeffs
        
        exercise_val = K - X
        exercise_now = exercise_val > continuation_val
        cash_flows[itm[exercise_now]] = exercise_val[exercise_now]
        
        not_exercised = np.ones(n_paths, dtype=bool)
        not_exercised[itm[exercise_now]] = False
        cash_flows[not_exercised] *= df

    return np.mean(cash_flows * df)