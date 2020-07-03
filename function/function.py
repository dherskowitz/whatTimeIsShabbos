import os
import urllib3
import json
from botocore.exceptions import ClientError

ip_info_base_url = 'https://ipinfo.io/'
ip_info_token = os.environ['ipinfo_token']


def get_location_from_ip(ip_address):
    http = urllib3.PoolManager()
    
    ip_info_api_url = f"{ip_info_base_url}{ip_address}?token={ip_info_token}"
    ip_response = http.request('GET', ip_info_api_url)
    ip_data = json.loads(ip_response.data.decode('utf-8'))
    if 'error' in ip_data:
       data = {
            'location': "31.779456, 35.224255",
            'tz': "Asia/Jerusalem",
            'city': "Jerusalem",
            'region': "Jerusalem",
            'country': "IL",
            'status': "ip_error"
        }
    else:
        data = {
            'location': ip_data['loc'],
            'tz': ip_data['timezone'],
            'city': ip_data['city'],
            'region': ip_data['region'],
            'country': ip_data['country'],
            'status': "ip_found"
        }
    return data


def get_zmanim_from_location(event, context):
    print(event, context)
    data = {}
    http = urllib3.PoolManager()
    
    try:
        if event['httpMethod'] == 'GET':
            client_ip = event['headers']['X-Forwarded-For']
            if ',' in client_ip:
                client_ip = client_ip.split(',')[0]
            ip_data = get_location_from_ip(client_ip)
            location_split = ip_data['location'].split(',')
            lat = location_split[0]
            lng = location_split[1]
            tz = ip_data["tz"]
            time_before_lighting = '40' if ip_data['city'] == 'Jerusalem' else '18'
        else: 
            data = json.loads(event['body'])
            lat = data['location']['lat']
            lng = data['location']['lng']
            tz_url = f"http://api.timezonedb.com/v2.1/get-time-zone?format=json&by=position&lat={lat}&lng={lng}&key={os.environ['timezonedb']}"
            get_tz = http.request('GET', tz_url)
            tz_data = json.loads(get_tz.data.decode('utf-8'))
            tz = tz_data['zoneName']
            time_before_lighting = '40' if data['city'] == 'Jerusalem' else '18'
            ip_data = {
                'tz': tz,
                'city': data['city'],
                'region': data['region'],
                'country': data['country'],
                'status': "user_location"
            }
        
        url = f'https://www.hebcal.com/shabbat/?cfg=json&m=42&leyning=off&a=on&b={time_before_lighting}&geo=pos&latitude={lat}&longitude={lng}&tzid={tz}'
        print(url)
        zm = http.request('GET', url)
        data['zman_data'] = json.loads(zm.data.decode('utf-8'))
        data['ip_data'] = ip_data
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {'status': 'error', 'error': e.response['Error']['Message']}
    # print(data)
    return {
        'statusCode': 200,
        'headers': { 'Content-Type': 'application/json' },
        'body': json.dumps(data)
    }
