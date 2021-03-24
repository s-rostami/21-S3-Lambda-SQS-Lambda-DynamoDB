import logging
import json
import urllib.parse
from json import loads
import boto3

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.info('Loading function')

dynamodb = boto3.resource(
    'dynamodb', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")


def lambda_handler(event, context):
    print(event)
    logger.debug('Received event: {}'.format(event))
    #event_body = json.loads(event['body'])
    #city_name = urllib.parse.unquote_plus(event['Records'][0]['body']['Bucket_Name'], encoding='utf-8')
    city_name = event['Records']
    city_name1 = city_name[0]
    city_name2 = city_name1['body']
    event_body = json.loads(city_name2)
    print(event_body)
    bucket = event_body["Bucket_Name"]
    name = event_body['File_name']
    print(name)
    # print(city_name3)
    #review = urllib.parse.unquote_plus(event['Records'][0]['body']['File_Name'], encoding='utf-8')
    # print(review)
    #logger.debug('Received event: {}'.format(event))

    file = {
        'ID': 3,
        'City_Name': bucket,
        'Review': name
    }

    table = dynamodb.Table('Cities')
    table.put_item(Item=file)

    # for record in event['Records']:
    #    print(record)

    return 0
