from unittest import mock

import pytest

from powerlibs.aws.sqs.publisher import SQSPublisher


@pytest.fixture
def mock_boto_client_sqs():

    mocked_queue = mock.Mock(
        send_message=mock.Mock(),
    )

    def create_queue(Name):
        return mocked_queue

    def get_queue_by_name(QueueName):
        return mocked_queue

    return mock.Mock(
        get_queue_by_name=mock.Mock(return_value=mocked_queue),
        create_queue=mock.Mock(return_value=mocked_queue),
        mocked_queue=mocked_queue,
    )


@pytest.fixture
def sqs_publisher(mock_boto_client_sqs):
    sqs_publisher = SQSPublisher()
    sqs_publisher.sqs_client = mock_boto_client_sqs

    return sqs_publisher
