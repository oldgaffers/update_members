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
    if after['Country'] in ['United Kingdom', 'Eire']:
        lat, lng = location(after)
        change['lat'] = Decimal(str(round(float(lat), 5)))
        change['lng'] = Decimal(str(round(float(lng), 5)))]
    return change

def detail_handler(message):
    type = message['DetailType']
    detail = json.loads(message['Detail'])
    # print('detail', json.dumps(detail))
    if type == 'added':
        return update(detail)
    elif type == 'updated':
        before = detail['before']
        after = detail['after']
    if after['Status'] not in ['Deceased', 'Left OGA']:
        change = calculate_change(before, after)
        return update(change)

def lambda_handler(event, context):
    # print(json.dumps(event))
    if 'body' in event:
        response = detail_handler(event['body'])
    elif 'Records' in event:
        for record in event['Records']:
            if 'Sns' in record:
                message = json.loads(record['Sns']['Message'])
                return detail_handler(message)
            else:
                response = 'ERROR'
    else:
        response = 'ERROR'
    return {
        'statusCode': 200,
        'body': json.dumps(response, cls=DecimalEncoder)
    }
