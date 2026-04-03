#!/usr/bin/env python3
"""Uploads WhatsApp, Calendar, and Reminders SQLite databases to Cloudflare R2.
Triggered by fswatch on database file changes. Uses sqlite3 .backup for safe copies."""

import subprocess
import tempfile
import os
import sys
import time

# R2 config
ENDPOINT = "https://87fc573113247ec5fc93a6cc77401204.r2.cloudflarestorage.com"
BUCKET = "sanat-db-sync"

# Read keys from ~/.r2-credentials (not in git)
def load_credentials():
    creds_file = os.path.expanduser("~/.r2-credentials")
    creds = {}
    with open(creds_file) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                creds[k.strip()] = v.strip()
    return creds["access_key"], creds["secret_key"]

# Database sources
DATABASES = {
    "ChatStorage.sqlite": os.path.expanduser(
        "~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite"
    ),
    "Calendar.sqlitedb": os.path.expanduser(
        "~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
    ),
    "Reminders.sqlite": os.path.expanduser(
        "~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-A5FBE7B2-70BC-4FA4-BA7A-C5376D78F941.sqlite"
    ),
}

def backup_and_upload():
    import boto3

    access_key, secret_key = load_credentials()
    s3 = boto3.client("s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
    )

    for name, src_path in DATABASES.items():
        if not os.path.exists(src_path):
            continue

        # Safe backup to temp file
        tmp = os.path.join(tempfile.gettempdir(), f"dbsync-{name}")
        try:
            subprocess.run(
                ["sqlite3", src_path, f".backup '{tmp}'"],
                capture_output=True, timeout=30
            )
        except Exception:
            # Fallback: direct copy
            subprocess.run(["cp", src_path, tmp], capture_output=True)

        if os.path.exists(tmp):
            s3.upload_file(tmp, BUCKET, name)
            size_mb = os.path.getsize(tmp) / (1024 * 1024)
            print(f"{time.strftime('%H:%M:%S')} ✓ {name} ({size_mb:.1f}MB)")
            os.remove(tmp)

if __name__ == "__main__":
    backup_and_upload()
