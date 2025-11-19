import asyncio
import websockets
import csv
import json
from datetime import datetime


async def stream_prices(symbol: str, duration: int, out: str):
    uri = f"wss://stream.binance.us:9443/ws/{symbol.lower()}@trade"
    end_time = asyncio.get_event_loop().time() + duration

    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "price"])

        async with websockets.connect(uri) as ws:
            while True:
                if asyncio.get_event_loop().time() >= end_time:
                    break

                msg = await ws.recv()
                data = json.loads(msg)

                price = float(data["p"])
                ts = datetime.fromtimestamp(data["T"] / 1000)

                writer.writerow([ts.isoformat(), price])
                print(ts, price)
