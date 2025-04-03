import json
from decimal import *
from ddb import update
from geo import location

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def calculate_change(before, after):
    change = {k:v for (k,v) in after.items() if v != before.get(k, '')}
    change['ID'] = after['ID']
    change['Member Number'] = after['Member Number']
    if after['Country'] in ['United Kingdom', 'Eire'] and after['Status'] != 'Left OGA':
        lat, lng = location(after)
        change['lat'] = Decimal(str(round(float(lat), 5)))
        change['lng'] = Decimal(str(round(float(lng), 5)))

def lambda_handler(event, context):
    if 'body' in event:
        response = update(json.loads(event['body'])['detail'])
    elif 'Records' in event:
        for record in event['Records']:
            message = json.loads(record['Sns']['Message'])
            detail = json.loads(message['Detail'])
            before = detail['before']
            after = detail['after']
            change = calculate_change(before, after)
            response = update(change)
    else:
        response = 'ERROR'
    return {
        'statusCode': 200,
        'body': json.dumps(response, cls=DecimalEncoder)
    }
