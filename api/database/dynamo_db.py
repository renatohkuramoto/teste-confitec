import boto3
from config import get_database

# Configurações do AWS
client = boto3.client(
    'dynamodb',
    aws_access_key_id=get_database()['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=get_database()['AWS_SECRET_ACCESS_KEY'],
    region_name=get_database()['REGION_NAME'],
)

resource = boto3.resource(
    'dynamodb',
    aws_access_key_id=get_database()['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=get_database()['AWS_SECRET_ACCESS_KEY'],
    region_name=get_database()['REGION_NAME'],
)
