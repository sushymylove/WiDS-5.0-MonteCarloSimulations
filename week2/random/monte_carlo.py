import numpy as np

class MonteCarloSimulator:
    def __init__(self, predicate_func, bounds):
        self.predicate = predicate_func
        self.bounds = bounds
        self.box_area = (bounds[1] - bounds[0]) * (bounds[3] - bounds[2])

    def estimate(self, N):
        x = np.random.uniform(self.bounds[0], self.bounds[1], int(N))
        y = np.random.uniform(self.bounds[2], self.bounds[3], int(N))
        
        inside_mask = self.predicate(x, y)
        points_inside = np.sum(inside_mask)
        
        return (points_inside / N) * self.box_area