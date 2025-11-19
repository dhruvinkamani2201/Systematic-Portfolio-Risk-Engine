import asyncio
import websockets
import json
import csv
from datetime import datetime


async def stream_multi_asset(symbols, duration, out):
    streams = "/".join([f"{s.lower()}@trade" for s in symbols])
    uri = f"wss://stream.binance.us:9443/stream?streams={streams}"

    print(f"[INFO] Connecting to Binance US multi-stream:\n{uri}")

    end_time = asyncio.get_event_loop().time() + duration

    # Keep last known price for each asset
    latest_prices = {s: None for s in symbols}

    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp"] + symbols)

        async with websockets.connect(uri, max_size=2**25) as ws:
            print("[INFO] Streaming multi-asset prices...")

            while True:
                if asyncio.get_event_loop().time() >= end_time:
                    print("[INFO] Streaming complete.")
                    break

                msg = await ws.recv()
                data = json.loads(msg)

                payload = data["data"]
                symbol = payload["s"]
                price = float(payload["p"])
                ts = datetime.fromtimestamp(payload["T"] / 1000)

                latest_prices[symbol] = price

                # Write row even if some assets haven't updated yet
                if all(v is not None for v in latest_prices.values()):
                    row = [ts.isoformat()] + [latest_prices[s] for s in symbols]
                    writer.writerow(row)
                    print(row)
