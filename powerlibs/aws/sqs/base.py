import os
import logging

import boto3
from cached_property import cached_property


class SQSBase:
    def __init__(self, aws_access_key_id=None, aws_secret_access_key=None, aws_region=None):
        self.aws_access_key_id = aws_access_key_id or os.environ['AWS_ACCESS_KEY_ID']
        self.aws_secret_access_key = aws_secret_access_key or os.environ['AWS_SECRET_ACCESS_KEY']
        self.aws_region = aws_region or os.environ['AWS_REGION']

        self.logger = logging.getLogger()

    @cached_property
    def sqs_client(self):
        return boto3.resource(
            'sqs',
            self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def get_queue(self, name):
        return self.sqs_client.get_queue_by_name(QueueName=name)
