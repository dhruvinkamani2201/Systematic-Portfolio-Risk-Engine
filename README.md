**1. Run live multi-asset data feed**

Streams trades from Binance US for all configured symbols.
python run.py feed

**2. Run risk pipeline (PCA → Covariance → Optimization)**
python run.py risk

This step:
Loads prices
Computes returns
Fits PCA factor model
Applies Ledoit–Wolf shrinkage
Optimizes portfolio
Prints allocations
