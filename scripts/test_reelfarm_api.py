import os
import sys

import requests


def get_api_key():
    api_key = os.getenv("REELFARM_API_KEY")
    if not api_key:
        print("ERROR: REELFARM_API_KEY is not set", file=sys.stderr)
        sys.exit(1)
    return api_key


if __name__ == '__main__':
    api_key = get_api_key()
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    response = requests.get('https://reel.farm/api/v1/videos', headers=headers)
    print(f'Response Code: {response.status_code}')
    print(response.json())
