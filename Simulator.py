"""
Usage:
  Simpulator.py [--module=<module>] [--class=<class>]

Options:
  --module=<module>     Module Name
  --class=<class>       Class Name, Optional if class name is the same as module name
"""

from typing import List
import logging
import importlib

from docopt import docopt
import matplotlib.pyplot as plt

from MarketDataManager import MarketData, MarketDataManager
from OrderManager import OrderManager, FillData, OrderStatus, OrderData, OrderSide
from Strategy import Strategy
from DummyStrategy import DummyStrategy
import dataloader as dl


class Simulator:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.om = strategy.om
        self.mdm = strategy.mdm
        self._filled_order = set()
        self.tradeId = 0

    def _load_market_data(self):
        self.market_data = [MarketData(**d) for d in dl.get_items("md_30min")]
        # return [MarketData("BTCUSD", 0,0,0,40000,0)]

    def _mock_fill(self, timestamp) -> List[OrderData]:
        res = []
        for order_id, order in self.om.working_order.items():
            if order_id not in self._filled_order:
                order.fills = [FillData(order.order_price, order.order_qty, self.tradeId)]
                order.status = OrderStatus.FILLED
                order.order_timestamp = timestamp
                res.append(order)
                self.tradeId += 1
                self._filled_order.add(order_id)
        return res

    def run(self):
        self._load_market_data()
        for market_data in self.market_data:
            self.mdm.on_md_update(market_data)
            self.strategy.on_md_update()
            filled_orders = self._mock_fill(market_data.timestamp)
            for order in filled_orders:
                self.om.on_order_update(order)
                self.strategy.on_order_update(order)

    def get_perf(self):
        buy = [x for x in self.om.archive_order.values() if x.side is OrderSide.BUY]
        sell = [x for x in self.om.archive_order.values() if x.side is OrderSide.SELL]
        plt.scatter(
            [x.order_timestamp for x in buy],
            [x.order_price for x in buy],
            marker="^", c="green"
        )
        plt.scatter(
            [x.order_timestamp for x in sell],
            [x.order_price for x in sell],
            marker="^", c="red"
        )
        plt.plot([x.timestamp for x in self.market_data] , [x.close for x in self.market_data])
        plt.show()


if __name__ == '__main__':
    args = docopt(__doc__)
    cls = args['--class']
    if cls is None:
        cls = args['--module']
    module = importlib.import_module(args['--module'])

    om = OrderManager()
    mdm = MarketDataManager()

    s = getattr(module, cls)(om, mdm)
    sim = Simulator(s)
    sim.run()
    sim.get_perf()
