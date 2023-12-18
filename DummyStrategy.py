from Strategy import Strategy
from OrderManager import OrderSide


class DummyStrategy(Strategy):
    def on_md_update(self):
        symbol = "BTCUSDT"
        close = self.mdm.data[symbol].close
        if close <= 20000:
            self.om.submit_order(symbol, OrderSide.BUY, 0.01, close)
        elif self.mdm.data[symbol].close >= 24000:
            self.om.submit_order(symbol, OrderSide.SELL, 0.01, close)
