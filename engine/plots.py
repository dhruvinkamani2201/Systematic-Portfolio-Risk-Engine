import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_covariance_heatmap(cov: pd.DataFrame):
    plt.figure(figsize=(8, 6))
    sns.heatmap(cov, annot=False, cmap="viridis")
    plt.title("Covariance Matrix Heatmap")
    plt.tight_layout()
    plt.show()

def plot_factor_loadings(loadings: pd.DataFrame):
    plt.figure(figsize=(10, 5))
    loadings.plot(kind="bar")
    plt.title("Factor Loadings")
    plt.xlabel("Assets")
    plt.ylabel("Loading")
    plt.tight_layout()
    plt.show()

def plot_portfolio_weights(weights: pd.Series):
    plt.figure(figsize=(8, 4))
    weights.plot(kind="bar")
    plt.title("Optimized Portfolio Weights")
    plt.ylabel("Allocation")
    plt.tight_layout()
    plt.show()

def plot_pca_variance(pca):
    var = pca.explained_variance_ratio_
    plt.figure(figsize=(6, 4))
    plt.bar(range(1, len(var)+1), var)
    plt.title("PCA Variance Explained")
    plt.xlabel("Factor")
    plt.ylabel("Fraction")
    plt.tight_layout()
    plt.show()
