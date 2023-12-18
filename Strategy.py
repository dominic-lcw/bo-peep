from MarketDataManager import MarketData, MarketDataManager
from OrderManager import OrderManager, OrderData


class Strategy:
    def __init__(self, om: OrderManager, mdm: MarketDataManager):
        self.om = om
        self.mdm = mdm

    def on_md_update(self):
        pass

    def on_order_update(self, order: OrderData):
        pass
