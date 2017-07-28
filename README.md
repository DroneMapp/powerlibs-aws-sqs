# powerlibs-aws-sqs

Amazon SQS helper classes

## Usage

### Manual configuration

```python
from powerlibs.aws.sqs.listener import SQSListener


class MySQSListener(SQSListener):
    def process_message(payload):
        # Do the processing and return True if you
        # want to acknowledge (delete) the message:
        return True


my_listener = MySQSListener(
    aws_access_key_id,
    aws_secret_access_key,
    'us-east-1',  # aws_region
    'MyQueueName'  # queue name
    )

my_listener.process_messages()  # Attention to the plural form!
```


Alternatively, you can process only N messages:


```python
my_listener.process_messages(10)  # Where N = 10, for example.
```


### Configuration via environment variables

It's probable you already have `AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY` and `AWS_REGION` environment variables defined, so
you can just use this helper function:

```python
from powerlibs.aws.sqs import listener

my_listener = listener.get_listener_configured_via_environment_variables()
```
