import cvxpy as cp
import numpy as np
import pandas as pd

class PortfolioOptimizer:
    def __init__(self, returns, cov, mu):
        self.returns = returns

        # Keep the asset names for output
        self.asset_names = mu.index.tolist()

        # Convert inputs to numpy for CVXPY compatibility
        self.mu = np.asarray(mu, dtype=float)
        self.cov = cov.values  # covariance matrix as ndarray
        self.n = len(self.mu)

    def mean_variance(self, risk_aversion=1.0):
        w = cp.Variable(self.n)

        objective = cp.Maximize(
            cp.matmul(self.mu, w) - risk_aversion * cp.quad_form(w, self.cov)
        )

        constraints = [
            cp.sum(w) == 1,
            w >= 0  # long-only
        ]

        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.SCS)

        weights = np.array(w.value).flatten()

        return pd.Series(weights, index=self.asset_names)
