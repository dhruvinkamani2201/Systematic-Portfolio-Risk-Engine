**1. Run live multi-asset data feed**

Streams trades from Binance US for all configured symbols.
```bash
python run.py feed
```

**2. Run risk pipeline (PCA → Covariance → Optimization)**
```bash
python run.py risk
```
This step: <br/>
Loads prices<br/>
Computes returns<br/>
Fits PCA factor model<br/>
Applies Ledoit–Wolf shrinkage<br/>
Optimizes portfolio<br/>
Prints allocations<br/>

**3. Run entire workflow (feed → risk pipeline)**

```bash
python run.py all
```


This performs: <br/>
Stream multi-asset prices <br/>
Build factors <br/>
Estimate covariance <br/>
Solve optimizer <br/>
Display results <br/>
