#!/bin/bash
# Downloads latest SQLite databases from Cloudflare R2 to ~/synced-db/
# Run this from any cloud environment (Codespaces, remote, etc.)

python3 - <<'EOF'
import subprocess, os, gzip, shutil
subprocess.run(["pip3", "install", "boto3", "--break-system-packages", "-q"], capture_output=True)
import boto3
os.makedirs(os.path.expanduser("~/synced-db"), exist_ok=True)
s3 = boto3.client("s3",
    endpoint_url="https://87fc573113247ec5fc93a6cc77401204.r2.cloudflarestorage.com",
    aws_access_key_id="b6e345139d3cde2c83e6914c8ac6ac8d",
    aws_secret_access_key="7de8c327382dda91f30f6b3973028f800b207744bdf2b06b1088f777dbd40a8a",
    region_name="auto"
)
files = ["ChatStorage.sqlite", "Calendar.sqlitedb", "Reminders.sqlite", "Gmail.sqlite"]
for f in files:
    dest = os.path.expanduser(f"~/synced-db/{f}")
    gz_key = f + ".gz"
    gz_dest = dest + ".gz"
    # Try compressed version first (current upload format)
    try:
        s3.download_file("sanat-db-sync", gz_key, gz_dest)
        with gzip.open(gz_dest, "rb") as f_in, open(dest, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(gz_dest)
        print(f"✓ {f} (from .gz)")
    except Exception:
        # Fall back to uncompressed
        try:
            s3.download_file("sanat-db-sync", f, dest)
            print(f"✓ {f} (uncompressed)")
        except Exception as e:
            print(f"✗ {f}: {e}")
print("Done — databases refreshed.")
EOF
