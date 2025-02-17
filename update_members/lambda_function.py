import json
import boto3
import http.client
from bng_latlon import bng_to_latlon
from decimal import *
from boto3.dynamodb.conditions import Key

ssm = boto3.client('ssm')
r = ssm.get_parameter(Name='/OS/API_KEY')
key = r['Parameter']['Value']

keymap = {
  'GDPR': 'GDPR',
  'Interest Areas': 'interests', 
  'Member Number': 'membership',
  'Payment Method': 'payment', 
  'Trailer': 'smallboats',
}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def update(row):
    primary_key = ['id','membership']
    item = {keymap.get(k, k.lower().replace(' ', '_').replace(':', '')):v for (k,v) in row.items()}
    print(item)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('members')
    r = table.query(KeyConditionExpression=Key("membership").eq(item['membership']))
    print(r)
    a = [kv for kv in item.items() if kv[0] not in primary_key]
    keys = [kv[0] for kv in a]
    vals = [kv[1] for kv in a]
    return table.update_item(
        Key={ 'id':item['id'], 'membership':item['membership'] },
        UpdateExpression=f"SET {','.join([f'#f{i}=:var{i}' for i, k in enumerate(keys)])}",
        ExpressionAttributeNames={f'#f{i}':k for i,k in enumerate(keys)},
        ExpressionAttributeValues={f':var{i}':v for i,v in enumerate(vals)},
        ReturnValues="UPDATED_NEW"
    )

def location(item):
    host = 'api.os.uk'
    conn = http.client.HTTPSConnection(host)
    place = item['Postcode'].replace(' ', '')
    conn.request("GET", f"/search/names/v1/find?query={place}&maxresults=1", headers={"Host": host, 'key': key})
    r1 = conn.getresponse()
    if r1.status == 200:
        data = json.loads(r1.read())
        entry = data['results'][0]['GAZETTEER_ENTRY']
        return bng_to_latlon(entry['GEOMETRY_X'], entry['GEOMETRY_Y'])
    else:
        print(r1.status, r1.reason)
        return 0, 0

def lambda_handler(event, context):
    if 'body' in event:
        response = update(json.loads(event['body'])['detail'])
    elif 'Records' in event:
        for record in event['Records']:
            message = json.loads(record['Sns']['Message'])
            detail = json.loads(message['Detail'])
            before = detail['before']
            after = detail['after']
            change = {k:v for (k,v) in after.items() if v != before[k]}
            change['ID'] = after['ID']
            change['Member Number'] = after['Member Number']
            if after['Country'] in ['United Kingdom', 'Eire'] and after['Status'] != 'Left OGA':
                lat, lng = location(after)
                change['lat'] = Decimal(str(round(float(lat), 5)))
                change['lng'] = Decimal(str(round(float(lng), 5)))
            response = update(change)
    else:
        response = 'ERROR'
    return {
        'statusCode': 200,
        'body': json.dumps(response, cls=DecimalEncoder)
    }
