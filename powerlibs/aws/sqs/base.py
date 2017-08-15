import logging

import boto3
from cached_property import cached_property


class SQSBase:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, queue_name):
        self.aws_region = aws_region
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

        self.logger = logging.getLogger()

    @cached_property
    def sqs_client(self):
        return boto3.resource(
            'sqs',
            self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    @cached_property
    def sqs_queue(self):
        return self.sqs_client.get_queue_by_name(QueueName=self.queue_name)
