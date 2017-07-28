import os
import json
import logging

import boto3
from cached_property import cached_property


class SQSListener:
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, queue_name):
        self.queue_name = queue_name
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

    def receive_messages(self, max_number_of_message=1, wait_time=5, visibility_timeout=30):
        return self.sqs_queue.receive_messages(
            MaxNumberOfMessages=max_number_of_message,
            WaitTimeSeconds=wait_time,
            VisibilityTimeout=visibility_timeout)

    def process_messages(self, max_messages=None):
        counter = 0
        for message in self.receive_messages():
            body = json.loads(message.body)
            payload = json.loads(body['Message'])
            ret = self.process_message(payload)
            if ret is True:
                message.delete()

            if max_messages is not None:
                counter += 1
                if counter >= max_messages:
                    return

    def process_message(self, message):
        self.logger.info('Processing message: {}'.format(message))


def get_listener_configured_via_environment_variables(queue_name):
    aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    aws_region = os.environ['AWS_REGION']

    return SQSListener(aws_access_key_id, aws_secret_access_key, aws_region, queue_name)
