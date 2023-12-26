<h1>Backtest / Trading</h1>

<h1>Backtest Usage</h1>

<h2>Command Line</h2>

```commandline
python Simulator.py --module=DummyStrategy --class=DummyStrategy
```
<h2>Jupyter Notebook</h2>

```python
from Simulator import Simulator
from OrderManager import OrderManager
from MarketDataManager import MarketDataManager

om = OrderManager()
mdm = MarketDataManager()
# replace by your strategy script
from DummyStrategy import DummyStrategy
s = DummyStrategy(om, mdm)  

sim = Simulator(s)
sim.run()
sim.get_perf()
```

<h1>Framework</h1>

```python
class OrderManager:
    def submit_order(self, symbol, side, quantity):
        """timestamp for backtest use"""
        pass
    def get_pos(self):
        pass
    def on_order_update(self, order: OrderData):
        pass
    
class Strategy:
    def __init__(self, om: OrderManager):
        pass
    
    def on_md_update(self, market_data):
        """Put strategy logic here"""
        symbol = "BTCUSD"
        if market_data[symbol].close <= 40000:
            self.om.submit_order(symbol, OrderSide.BUY, 0.01)
        elif market_data[symbol].close >= 41000:
            self.om.submit_order(symbol, OrderSide.SELL, 0.01)
    
    def on_order_update(self, order):
        """Trigger when there is order update"""
        pass

class Simulator:
    def __init__(self, strategy: Strategy, om: OrderManager, mdm: MarketDataManager):
        self.strategy = strategy
        self.om = om
        self.mdm = mdm
    
    def _mock_fill(self) -> List[OrderData]:
        pass
    
    @staticmethod
    def _load_market_data() -> list:
        pass
    
    def run(self):
        """
        1. Get market data from database
        2. Trigger strategy.on_md_update
        3. Fill order in mock exchange
        4. Trigger strategy.on_order_update
        """
        for market_data in self._load_market_data():
            self.mdm.on_md_update(market_data)
            self.strategy.on_md_update()
            filled_orders = self._mock_fill()
            for order in filled_orders:
                self.om.on_order_update(order)
                self.strategy.on_order_update(order)
```
