import requests
import os

def get_api_key():
    return '368494f1f6cf5b6749e3f7e5bf35c106'

if __name__ == '__main__':
    api_key = get_api_key()
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    response = requests.get('https://reel.farm/api/v1/videos', headers=headers)
    print(f'Response Code: {response.status_code}')
    print(response.json())