import numpy as np
import pandas as pd
from sklearn.covariance import LedoitWolf


class CovarianceEstimator:
    def __init__(self):
        self.cov = None

    def compute(self, returns: pd.DataFrame):
        lw = LedoitWolf().fit(returns)
        self.cov = pd.DataFrame(lw.covariance_, index=returns.columns, columns=returns.columns)
        return self.cov

    def get(self):
        return self.cov
