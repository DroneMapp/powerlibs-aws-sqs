import os
import json

from .base import SQSBase


class SQSListener(SQSBase):
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
