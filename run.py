import argparse
import asyncio
import yaml
import pandas as pd

from engine.factors import FactorModel
from engine.covariance import CovarianceEstimator
from engine.optimizer import PortfolioOptimizer
from engine.attribution import RiskAttribution
from engine.websocket_feed import stream_multi_asset
from engine.plots import (
    plot_covariance_heatmap,
    plot_factor_loadings,
    plot_portfolio_weights,
    plot_pca_variance
)


def load_config():
    with open("config.yml") as f:
        return yaml.safe_load(f)


def run_pipeline(prices_csv, cfg):
    prices = pd.read_csv(prices_csv, index_col=0, parse_dates=True)

    # Step 1: Compute returns & PCA
    fm = FactorModel(cfg["factors"]["n_pca"])
    returns = fm.compute_returns(prices)
    factors = fm.fit_pca(returns)

    print(fm.get_factor_loadings())
    plot_factor_loadings(fm.get_factor_loadings())
    plot_pca_variance(fm.pca)

    # Step 2: Covariance
    ce = CovarianceEstimator()
    cov = ce.compute(returns)
    plot_covariance_heatmap(cov)

    # Step 3: Optimizer
    mu = returns.mean()
    optimizer = PortfolioOptimizer(cov, mu)
    
    print("Prices shape:", prices.shape)
    print("Returns shape:", returns.shape)
    print("Mean returns:", mu)

    weights = optimizer.mean_variance(cfg["optimizer"]["risk_aversion"])
    print("\nOptimized Weights:\n", weights)
    plot_portfolio_weights(weights)

    # Step 4: Factor Risk Attribution
    ra = RiskAttribution(cov, fm.get_factor_loadings())
    print("\nFactor Risk Contribution:", ra.factor_risk(weights))


def run_feed(cfg):
    symbols = cfg["feed"]["symbols"]
    duration = cfg["feed"]["duration"]
    out = cfg["feed"]["out"]
    asyncio.run(stream_multi_asset(symbols, duration, out))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["feed", "risk", "all"])
    args = parser.parse_args()

    cfg = load_config()

    if args.cmd == "feed":
        run_feed(cfg)
    elif args.cmd == "risk":
        run_pipeline(cfg["feed"]["out"], cfg)
    elif args.cmd == "all":
        run_feed(cfg)
        run_pipeline(cfg["feed"]["out"], cfg)
