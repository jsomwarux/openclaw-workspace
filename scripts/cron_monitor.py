import time
import os
import subprocess

CRON_JOBS = [
    'eve-job-market-daily-005',
    'Daily News Hook',
    'job-application-tracker',
    'zoom-resume-cover-letter-builder',
    'nash-satoshi-image-retriever',
    'crypto-analysis',
    'weekly-review'
]

def check_cron_status(job_name):
    try:
        result = subprocess.run(['cron', 'list'], stdout=subprocess.PIPE, text=True)
        return job_name in result.stdout
    except Exception as e:
        print(f"Error checking cron status for {job_name}: {e}")
        return False

while True:
    for job in CRON_JOBS:
        if not check_cron_status(job):
            print(f"⚠️ {job} is currently not running!")
    time.sleep(60)  # Check every minute