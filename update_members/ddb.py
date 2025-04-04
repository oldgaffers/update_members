import boto3
from boto3.dynamodb.conditions import Key

keymap = {
  'GDPR': 'GDPR',
  'Interest Areas': 'interests', 
  'Member Number': 'membership',
  'Payment Method': 'payment', 
  'Trailer': 'smallboats',
}

def update(row):
    primary_key = ['id','membership']
    item = {keymap.get(k, k.lower().replace(' ', '_').replace(':', '')):v for (k,v) in row.items()}
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('members')
    r = table.query(KeyConditionExpression=Key("membership").eq(item['membership']))
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