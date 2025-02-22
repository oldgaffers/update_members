import json
import http.client
from bng_latlon.bng_to_latlon import OSGB36toWGS84
import boto3

ssm = boto3.client('ssm')
r = ssm.get_parameter(Name='/OS/API_KEY')
key = r['Parameter']['Value']

def location(item):
    host = 'api.os.uk'
    conn = http.client.HTTPSConnection(host)
    place = item['Postcode'].replace(' ', '')
    conn.request("GET", f"/search/names/v1/find?query={place}&maxresults=1", headers={"Host": host, 'key': key})
    r1 = conn.getresponse()
    if r1.status == 200:
        data = json.loads(r1.read())
        entry = data['results'][0]['GAZETTEER_ENTRY']
        return OSGB36toWGS84(entry['GEOMETRY_X'], entry['GEOMETRY_Y'])
    else:
        print(r1.status, r1.reason)
        return 0, 0
