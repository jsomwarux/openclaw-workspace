#!/usr/bin/env python3
"""
Generate an image using Nano Banana 2 (google/gemini-3.1-flash-image-preview) via OpenRouter.
Usage: python3 nb2-generate.py --prompt "..." --output path/to/output.png
Requires: OPENROUTER_API_KEY env var set
"""
import sys
import json
import base64
import os
import argparse

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests', '-q'])
    import requests


def main():
    parser = argparse.ArgumentParser(description='Generate image via NB2 (Gemini flash image)')
    parser.add_argument('--prompt', required=True, help='Image generation prompt')
    parser.add_argument('--output', required=True, help='Output file path (.png)')
    parser.add_argument('--thinking', action='store_true', default=False,
                        help='Enable thinking mode (only for complex spatial reasoning)')
    args = parser.parse_args()

    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        # Fallback: read from OpenClaw auth-profiles.json
        try:
            profiles_path = os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json')
            with open(profiles_path) as f:
                profiles = json.load(f).get('profiles', {})
            api_key = profiles.get('openrouter:default', {}).get('token', '')
        except Exception:
            pass
    if not api_key:
        print('ERROR: OPENROUTER_API_KEY not set — add to ~/.config/env/global.env or auth-profiles.json', file=sys.stderr)
        sys.exit(1)

    payload = {
        'model': 'google/gemini-3.1-flash-image-preview',
        'messages': [{'role': 'user', 'content': args.prompt}],
    }
    if not args.thinking:
        payload['thinking'] = False

    try:
        r = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://jtsomwaru.com',
                'X-Title': 'Eve Vibe Marketing'
            },
            json=payload,
            timeout=60
        )
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'ERROR: API call failed: {e}', file=sys.stderr)
        sys.exit(1)

    data = r.json()

    # Extract image from response
    # OpenRouter NB2 returns images in message.images[] array (not in content)
    try:
        message = data['choices'][0]['message']
    except (KeyError, IndexError) as e:
        print(f'ERROR: Unexpected response structure: {e}', file=sys.stderr)
        print(json.dumps(data, indent=2)[:500], file=sys.stderr)
        sys.exit(1)

    image_found = False

    # Primary path: message.images[] array (OpenRouter NB2 format)
    images = message.get('images', [])
    for img in images:
        if isinstance(img, dict):
            url = img.get('image_url', {}).get('url', '') or img.get('url', '')
            if url.startswith('data:'):
                img_data = url.split(',', 1)[1]
                os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
                with open(args.output, 'wb') as f:
                    f.write(base64.b64decode(img_data))
                print(f'✅ Saved: {args.output}')
                image_found = True
                break
            elif url.startswith('http'):
                import urllib.request
                os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
                urllib.request.urlretrieve(url, args.output)
                print(f'✅ Saved (from URL): {args.output}')
                image_found = True
                break

    # Fallback: content field (list of parts or raw data URI)
    if not image_found:
        content = message.get('content')
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get('type') == 'image_url':
                    url = part['image_url']['url']
                    if url.startswith('data:'):
                        img_data = url.split(',', 1)[1]
                        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
                        with open(args.output, 'wb') as f:
                            f.write(base64.b64decode(img_data))
                        print(f'✅ Saved: {args.output}')
                        image_found = True
                        break
        elif isinstance(content, str) and content.startswith('data:'):
            img_data = content.split(',', 1)[1]
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, 'wb') as f:
                f.write(base64.b64decode(img_data))
            print(f'✅ Saved: {args.output}')
            image_found = True

    if not image_found:
        print('ERROR: No image data found in response', file=sys.stderr)
        print(json.dumps(data, indent=2)[:1000], file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
