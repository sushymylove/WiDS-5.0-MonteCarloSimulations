# WiDS Project: Monte Carlo Simulations
## Week 1: The Toolbox - Python & NumPy Fundamentals 
### Assignment 1.1: The Gambler's Ruin
- The Simulation: Modeled 10,000 gamblers over 1,000 rounds of coin flips using a (10000, 1000) NumPy matrix.
- Statistical Verification: Demonstrated the Central Limit Theorem (CLT). Despite individual outcomes being discrete binary values ($\pm 1$), the sum of these outcomes perfectly converges into a Gaussian "Bell Curve" distribution.
### Assignment 1.2: Building Modular Games (Blackjack)
This task focuses on Object-Oriented Programming (OOP) and the Separation of Concerns to build a professional-grade simulation environment.
- Data Layer (cards.py): Implements Suit and Rank using Python Enums. This prevents hardcoding errors and ensures immutability. The Hand class manages card values, specifically handling the dynamic value of the "Aces" (1 or 11).
- Logic Layer (blackjack.py): Encapsulates the core rules. It handles dealer AI (stopping at 17) and player actions. Because the logic is decoupled from the UI, the engine is "simulation-ready"—capable of running millions of hands per second without the overhead of print statements.
- UI Layer (main.py): A interactive Terminal User Interface (TUI) featuring ASCII-based card rendering. It manages the user session, bankroll tracking, and input validation.
## Week 2: Monte Carlo in Geometry
### Integration and the Curse of Dimensionality
Using random sampling to solve mathematical problems that are difficult or impossible to solve analytically.
- Predicate-Based Design: Developed a MonteCarloSimulator that accepts a lambda predicate. This allows the same engine to estimate $\pi$ (using a circle predicate), the area of a parabola, or the Gaussian Integral ($e^{-x^2}$) simply by swapping the mathematical condition.
- Convergence Analysis: Used Log-Log plots to verify the $1/\sqrt{N}$ error trend, proving that Monte Carlo is superior to grid-based Riemann sums in high-dimensional spaces where the "Curse of Dimensionality" makes grids computationally unfeasible.
## Week 2: The Quant Challenge
### Tasks 1-3: Path Generation & Asian Options
- Vectorized GBM Engine: Implemented Geometric Brownian Motion to model asset price paths.
- Asian Options: Priced path-dependent Asian Call Options. Since the payoff depends on the arithmetic average of the price over time, no simple analytical formula (like Black-Scholes) exists, making Monte Carlo essential for accurate pricing.
### Task 4 & 5: American Options & Engineering Rigor
- Longstaff-Schwartz Algorithm: Solved the "Optimal Stopping" problem for American Puts. Using Backward Induction, the engine runs a polynomial regression at each time step to compare the value of exercising the option immediately versus the "Expected Continuation Value" of holding it.
- Antithetic Variates: Implemented variance reduction by generating negatively correlated paths. This cancels out random noise and allows for 10x higher precision with significantly fewer simulations. 
## Key Fundamental Concepts
- Vectorization: Utilizing NumPy to perform operations on entire arrays simultaneously, bypassing the speed limitations of Python's interpreter.
- Modular Software Design: Separating Data, Logic, and Interface to create code that is testable and scalable.
- Backward Induction: The process of solving a problem from the end-point back to the start, a necessity for pricing early-exercise options. 
## Tools Used
- Core: Python, NumPy
- Visualization: Matplotlib (Log-Log convergence plots, GBM paths)
- Science: SciPy (Error function erf and stats verification)

