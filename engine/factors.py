import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

class FactorModel:
    def __init__(self, n_pca=3):
        self.n_pca = n_pca
        self.pca = None
        self.factor_loadings = None

    def compute_returns(self, prices: pd.DataFrame):
        return prices.pct_change().dropna()

    def fit_pca(self, returns: pd.DataFrame):
        self.pca = PCA(n_components=self.n_pca)
        factors = self.pca.fit_transform(returns)

        self.factor_loadings = pd.DataFrame(
            self.pca.components_.T,
            index=returns.columns,
            columns=[f"PCA_{i+1}" for i in range(self.n_pca)]
        )
        return pd.DataFrame(factors, index=returns.index)

    def get_factor_loadings(self):
        return self.factor_loadings
