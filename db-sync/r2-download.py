#!/usr/bin/env python3
"""Downloads WhatsApp, Calendar, and Reminders SQLite databases from Cloudflare R2.
Used by Codespaces to get the latest synced data."""

import os
import sys
import time

# R2 config
ENDPOINT = "https://87fc573113247ec5fc93a6cc77401204.r2.cloudflarestorage.com"
BUCKET = "sanat-db-sync"

# Read keys from ~/.r2-credentials or environment
def load_credentials():
    # Try credentials file first
    creds_file = os.path.expanduser("~/.r2-credentials")
    if os.path.exists(creds_file):
        creds = {}
        with open(creds_file) as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    creds[k.strip()] = v.strip()
        return creds["access_key"], creds["secret_key"]

    # Fall back to environment variables
    return os.environ["R2_ACCESS_KEY"], os.environ["R2_SECRET_KEY"]

DATABASES = ["ChatStorage.sqlite", "Calendar.sqlitedb", "Reminders.sqlite"]
DEST_DIR = os.path.expanduser("~/synced-db")

def download():
    import boto3

    access_key, secret_key = load_credentials()
    s3 = boto3.client("s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )

    os.makedirs(DEST_DIR, exist_ok=True)

    for name in DATABASES:
        dest = os.path.join(DEST_DIR, name)
        try:
            s3.download_file(BUCKET, name, dest)
            size_mb = os.path.getsize(dest) / (1024 * 1024)
            print(f"✓ {name} ({size_mb:.1f}MB)")
        except Exception as e:
            print(f"✗ {name}: {e}")

    print(f"Refreshed at {time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    download()
