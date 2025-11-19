**1. Run live multi-asset data feed**

Streams trades from Binance US for all configured symbols.
```bash
python run.py feed
```

**2. Run risk pipeline (PCA → Covariance → Optimization)**
```bash
python run.py risk
```
This step:
Loads prices
Computes returns
Fits PCA factor model
Applies Ledoit–Wolf shrinkage
Optimizes portfolio
Prints allocations

**3. Run entire workflow (feed → risk pipeline)**

```bash
python run.py all
```