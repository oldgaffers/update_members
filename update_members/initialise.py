import json
import boto3

s3 = boto3.client('s3')

def json_from_object(bucket, key):
    r = s3.get_object(Bucket=bucket, Key=key)
    text = r["Body"].read().decode('utf-8')
    return json.loads(text)

def initialise_from_s3():
   return json_from_object('boatregister', 'gold/latest.json')