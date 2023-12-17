""" 
    This script contains the uploaded that pulls data
        and inserts data to DB
"""

from api.handler import Snap
from collections import namedtuple
from logger.logger import logger

import boto3
import pandas as pd
from boto3.dynamodb.conditions import DynamoDBNeedsKeyConditionError
from typing import List

# Message node
UploadItem = namedtuple('UploadItem', ['data', 'table'])

class Uploader:
    
    def __init__(self):
        
        self.upload_list = []
        self.dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        logger.info(f"Started uploaded: {self.dynamodb}...")

    def add_to_list(self, upload_item: UploadItem) -> None:
        """ Add the UploadItem to the upload list
        """
        self.upload_list.append(upload_item)

    def upload(self) -> None:
        """ Upload all things from upload_list to repsective DB.
        """

        for item in self.upload_list:
            table = self.dynamodb.Table(item.table)
            table.put_item(Item = item.data)
            logger.info(f"Added data to table: {item.table}")
        else:
            logger.info("Successfully uploaded data to DB...")




