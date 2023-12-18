import logging
from typing import Dict, Sequence, List
import numbers

import boto3
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal

dyn_resource = boto3.resource("dynamodb", region_name='ap-southeast-2')


def format_item(item: Dict):
    return {k: Decimal(v) if isinstance(v, numbers.Real) else v for k, v in item.items()}


def put_items(table_name, items: Sequence[Dict]):
    table = dyn_resource.Table(table_name)
    for item in items:
        table.put_item(Item=format_item(item))
    logging.info(f"{len(items)} rows inserted")


def get_items(table_name) -> List[Dict]:
    table = dyn_resource.Table(table_name)
    return [item for item in table.scan()['Items']]
