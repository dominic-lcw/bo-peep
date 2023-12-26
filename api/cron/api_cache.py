"""
    The cron job here calls the API and caches the data in the database.
"""

from api.cache.uploader import Uploader, UploadItem
from api.cache.handler import Snap
from logger.logger import logger

import argparse

def snap_orderbook():

    # Get data from API
    snap = Snap()
    orderbook = snap.get_btc_order_book()

    # Upload data to DB
    uploader = Uploader()
    uploader.add_to_list(UploadItem(orderbook, 'md_orderbook'))
    uploader.upload()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process api actions.')
    parser.add_argument('action', type=str, help='The action to perform')

    args = parser.parse_args()

    if args.action == 'snap':
        snap_orderbook()










