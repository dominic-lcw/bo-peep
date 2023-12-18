import logging
from collections import defaultdict
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"

    def get_sign(self):
        if self is OrderSide.BUY:
            return 1
        elif self is OrderSide.SELL:
            return -1

@dataclass
class FillData:
    price: float
    qty: float
    tradeId: int


class OrderStatus(Enum):
    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"
    FILLED = "FILLED"


@dataclass
class OrderData:
    order_id: str
    symbol: str
    side: OrderSide
    order_qty: float
    order_price: float
    fills: List[FillData]
    status: OrderStatus
    order_timestamp: Optional[int] = None


class OrderManager:

    def __init__(self):
        self.working_order = {}  # type: Dict[str, OrderData]
        self.archive_order = {}  # type: Dict[str, OrderData]
        self.order_id = 0
        self.trade_ids = set()
        self.pos = defaultdict(float)

    def submit_order(self, symbol, side: OrderSide, quantity, price):
        order_id = str(self.order_id)
        self.working_order[order_id] = OrderData(order_id, symbol, side, quantity, price, [], OrderStatus.NEW)
        self.order_id += 1
        logging.info(f"Order submitted: {symbol=}, {side=}, {quantity=}, {price=}")

    def on_order_update(self, order: OrderData):
        self.working_order[order.order_id] = order
        for fill in order.fills:
            if fill.tradeId not in self.trade_ids:
                self.pos[order.symbol] += order.side.get_sign() * fill.qty
                self.trade_ids.add(fill.tradeId)
        if order.status in (OrderStatus.FILLED, OrderStatus.CANCELED, OrderStatus.REJECTED):
            self.archive_order[order.order_id] = order
            del self.working_order[order.order_id]
