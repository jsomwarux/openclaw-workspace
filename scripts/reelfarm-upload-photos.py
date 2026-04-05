import boto3
import os
from botocore.exceptions import NoCredentialsError

# Auto-load global.env if env vars not set
def _load_global_env():
    env_path = os.path.expanduser("~/.config/env/global.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())
_load_global_env()

# Cloudflare R2 Credentials (from env or global.env)
R2_ACCESS_KEY = os.environ.get('R2_ACCESS_KEY', '368494f1f6cf5b6749e3f7e5bf35c106')
R2_SECRET_KEY = os.environ.get('R2_SECRET_KEY', 'd8b719aa5c0c36dff1af4c384e636164f64062b067d8c08c41cccb57864aa579')
R2_BUCKET = os.environ.get('R2_BUCKET', 'vibe-marketing-photos')

# Create a session with the R2 service
session = boto3.session.Session()

# Create a client using R2 (s3 compatible)
client = session.client(
    's3',
    region_name='auto',
    endpoint_url=os.environ.get('R2_ENDPOINT', 'https://7148196b25e764e7753e4c7fbcdaaa5b.r2.cloudflarestorage.com'),
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY
)

# Function to upload photos to Cloudflare R2

def upload_photo(file_path):
    try:
        file_name = os.path.basename(file_path)
        client.upload_file(file_path, R2_BUCKET, file_name)
        print(f'Successfully uploaded {file_name} to R2 bucket')
    except NoCredentialsError:
        print('Credentials not available')
    except Exception as e:
        print(f'Error uploading {file_name}: {e}')