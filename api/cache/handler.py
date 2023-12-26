import requests
from logger.logger import logger

from typing import Dict
from datetime import datetime

class Snap:

    @staticmethod
    def get_btc_price() -> Dict:
        pass

    @staticmethod
    def get_btc_order_book() -> Dict:
        try:
            url = "https://api.binance.com/api/v3/depth"
            params = {
                "symbol": "BTCUSDT"
            }

            response = requests.get(url, params = params)
            data = response.json()
            data["last_update_id"] = str(data["lastUpdateId"])
            data["symbol"] = "BTCUSDT"
            data["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            del data["lastUpdateId"]
            logger.info("Snapped Data Successfully...")
        except Exception as e:
            logger.error(e)
            exit()

        return data


if __name__ == "__main__":
    data = Snap.get_btc_order_book()

