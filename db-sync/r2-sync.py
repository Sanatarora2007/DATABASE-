#!/opt/homebrew/bin/python3
"""Uploads WhatsApp, Calendar, and Reminders SQLite databases to Cloudflare R2.
Triggered by fswatch on database file changes. Uses sqlite3 .backup for safe copies.
Compresses with gzip before upload. Only uploads the changed database if path is passed."""

import sqlite3 as _sqlite3
import urllib.parse
import tempfile
import gzip
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

# Database sources (Calendar excluded — Google Calendar MCP is primary)
DATABASES = {
    "ChatStorage.sqlite": os.path.expanduser(
        "~/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite"
    ),
    "Reminders.sqlite": os.path.expanduser(
        "~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-A5FBE7B2-70BC-4FA4-BA7A-C5376D78F941.sqlite"
    ),
}

def which_db_changed(changed_path):
    """Return the subset of DATABASES that match the changed file path."""
    if not changed_path:
        return DATABASES  # no hint — upload all
    for name, src in DATABASES.items():
        if src in changed_path or changed_path.startswith(os.path.dirname(src)):
            return {name: src}
    return DATABASES  # unknown path — upload all

def backup_and_upload(changed_path=None):
    print(f"{time.strftime('%H:%M:%S')} [dbsync] importing boto3", flush=True)
    import boto3
    print(f"{time.strftime('%H:%M:%S')} [dbsync] boto3 imported", flush=True)

    from botocore.config import Config
    access_key, secret_key = load_credentials()
    print(f"{time.strftime('%H:%M:%S')} [dbsync] credentials loaded, creating s3 client", flush=True)
    s3 = boto3.client("s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
        config=Config(connect_timeout=10, read_timeout=60, retries={"max_attempts": 2}),
    )

    print(f"{time.strftime('%H:%M:%S')} [dbsync] s3 client ready", flush=True)
    targets = which_db_changed(changed_path)

    for name, src_path in targets.items():
        if not os.path.exists(src_path):
            continue

        tmp = os.path.join(tempfile.gettempdir(), f"dbsync-{name}")
        tmp_gz = tmp + ".gz"
        print(f"{time.strftime('%H:%M:%S')} [dbsync] backing up {name}", flush=True)
        try:
            src_uri = "file:" + urllib.parse.quote(src_path) + "?mode=ro"
            src_con = _sqlite3.connect(src_uri, uri=True, timeout=10)
            dst_con = _sqlite3.connect(tmp)
            src_con.backup(dst_con)
            src_con.close()
            dst_con.close()
        except Exception as backup_err:
            print(f"{time.strftime('%H:%M:%S')} [dbsync] backup error for {name}: {backup_err}", flush=True)
            continue

        if not os.path.exists(tmp):
            continue

        raw_mb = os.path.getsize(tmp) / (1024 * 1024)
        print(f"{time.strftime('%H:%M:%S')} [dbsync] backup done {name} ({raw_mb:.1f}MB), compressing", flush=True)

        # Compress
        with open(tmp, "rb") as f_in, gzip.open(tmp_gz, "wb", compresslevel=3) as f_out:
            f_out.write(f_in.read())
        os.remove(tmp)

        gz_mb = os.path.getsize(tmp_gz) / (1024 * 1024)
        print(f"{time.strftime('%H:%M:%S')} [dbsync] uploading {name}.gz ({gz_mb:.1f}MB)", flush=True)
        s3.upload_file(tmp_gz, BUCKET, name + ".gz")
        os.remove(tmp_gz)

        print(f"{time.strftime('%H:%M:%S')} ✓ {name} ({raw_mb:.1f}MB → {gz_mb:.1f}MB gz)", flush=True)

if __name__ == "__main__":
    changed_path = sys.argv[1] if len(sys.argv) > 1 else None
    print(f"{time.strftime('%H:%M:%S')} [dbsync] starting, changed_path={changed_path}", flush=True)
    try:
        backup_and_upload(changed_path)
    except Exception as e:
        print(f"{time.strftime('%H:%M:%S')} [dbsync] ERROR: {e}", flush=True)
        raise
