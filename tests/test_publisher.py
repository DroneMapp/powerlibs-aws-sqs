def test_publish(sqs_publisher):
    sqs_publisher.publish('test1', 'message')

    assert sqs_publisher.sqs_client.mocked_queue.send_message.called
