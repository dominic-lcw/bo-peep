from dataclasses import dataclass


@dataclass
class MarketData:
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp: int


class MarketDataManager:
    def __init__(self):
        self.data = {}

    def on_md_update(self, market_data: MarketData):
        self.data[market_data.symbol] = market_data
