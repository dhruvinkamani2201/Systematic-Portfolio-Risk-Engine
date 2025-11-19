import numpy as np
import cvxpy as cp
import pandas as pd


class PortfolioOptimizer:
    def __init__(self, cov: pd.DataFrame, mu: pd.Series):
        self.cov = cov
        self.mu = mu

    def mean_variance(self, risk_aversion=1.0):
        n = len(self.mu)
        w = cp.Variable(n)

        objective = cp.Maximize(self.mu @ w - risk_aversion * cp.quad_form(w, self.cov))
        constraints = [cp.sum(w) == 1, w >= 0]  # long-only

        prob = cp.Problem(objective, constraints)
        prob.solve()

        return pd.Series(w.value, index=self.mu.index)

    def risk_budget(self, risk_fraction=0.20):
        n = len(self.mu)
        w = cp.Variable(n)

        portfolio_var = cp.quad_form(w, self.cov)
        objective = cp.Minimize(portfolio_var)

        constraints = [
            cp.sum(w) == 1,
            w >= 0,
            portfolio_var <= risk_fraction
        ]

        cp.Problem(objective, constraints).solve()
        return pd.Series(w.value, index=self.mu.index)
