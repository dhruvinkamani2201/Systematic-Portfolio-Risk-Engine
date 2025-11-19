import numpy as np
import pandas as pd


class RiskAttribution:
    def __init__(self, cov: pd.DataFrame, loadings: pd.DataFrame):
        self.cov = cov
        self.loadings = loadings

    def factor_risk(self, weights: pd.Series):
        exposures = self.loadings.T @ weights
        factor_cov = self.loadings.T @ self.cov @ self.loadings
        total_factor_risk = exposures.T @ factor_cov @ exposures
        return total_factor_risk

    def total_portfolio_variance(self, weights: pd.Series):
        return np.dot(weights.T, self.cov @ weights)
