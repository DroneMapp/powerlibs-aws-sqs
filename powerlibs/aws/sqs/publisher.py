import json

from .base import SQSBase


class SQSPublisher(SQSBase):
    @staticmethod
    def translate_attributes_into_amazon_bizarre_format(attributes):
        translated_attributes = {}

        for key, value in attributes.items():
            if isinstance(value, str):
                translated_attributes[key] = {
                    'DataType': 'String',
                    'StringValue': value
                }
            elif isinstance(value, (int, float)):
                translated_attributes[key] = {
                    'DataType': 'Number',
                    'StringValue': value
                }

        return translated_attributes

    def publish(self, queue_name, payload, attributes=None):
        queue = self.get_queue(queue_name)
        attributes = self.translate_attributes_into_amazon_bizarre_format(attributes) if attributes else None

        response = queue.send_message(
            MessageAttributes=attributes,
            MessageBody=json.dumps(payload)
        )

        return response.get('MessageId')
