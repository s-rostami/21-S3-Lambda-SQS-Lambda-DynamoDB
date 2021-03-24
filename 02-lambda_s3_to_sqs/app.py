import json
import boto3
import datetime
import json
import logging
import os
import urllib.parse
from botocore.exceptions import ClientError

# AWS clients
sqs_client = boto3.client('sqs')
s3_client = boto3.client('s3')

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info('Loading function')

# Environment variables (set by SAM template)
sqs_queue_url = os.getenv("SQS_QUEUE_URL")

# AWS clients
sqs_client = boto3.client('sqs')
s3_client = boto3.client('s3')


def lambda_handler(event, context):
    logger.debug('Received event: {}'.format(event))

    bucket = urllib.parse.unquote_plus(event['Records'][0]['s3']['bucket']['name'], encoding='utf-8'
                                       )
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'],
        encoding='utf-8'
    )

    message = {
        'Bucket_Name': bucket,
        'File_name': key
    }
    print(message)
    message = json.dumps(message, separators=(',', ':'))

    send_sqs_message(message)
    return 0


def send_sqs_message(message):
    """
    Send JSON-format message to SQS.
    :param message: Dictionary message object
    :return: Dictionary containing information about the sent message. If
        error, returns None.
    """

    try:
        response = sqs_client.send_message(
            QueueUrl=sqs_queue_url,
            MessageBody=message,
            DelaySeconds=0,
            MessageAttributes={
                'Method': {
                    'StringValue': 'POST',
                    'DataType': 'String'
                }
            }
        )
        return response
    except ClientError as e:
        logger.error(e)
        return None
