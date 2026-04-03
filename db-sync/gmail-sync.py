#!/usr/bin/env python3
"""Fetches recent Gmail via IMAP, saves to SQLite, uploads to R2.
Runs on Mac triggered by fswatch or cron."""

import imaplib
import email
import email.utils
import sqlite3
import os
import time
import json
from email.header import decode_header

# Gmail IMAP config
GMAIL_USER = "sanatarora2007@gmail.com"
GMAIL_PASS = "zbom borr qxfx kpvm"
IMAP_HOST = "imap.gmail.com"

# Local SQLite path
DB_PATH = os.path.expanduser("~/synced-db/Gmail.sqlite")

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.execute("""CREATE TABLE IF NOT EXISTS emails (
        message_id TEXT PRIMARY KEY,
        sender TEXT,
        sender_email TEXT,
        subject TEXT,
        date TEXT,
        date_timestamp INTEGER,
        body TEXT,
        is_read INTEGER DEFAULT 0,
        labels TEXT,
        snippet TEXT
    )""")
    db.execute("CREATE INDEX IF NOT EXISTS idx_date ON emails(date_timestamp DESC)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_sender ON emails(sender_email)")
    db.commit()
    return db

def decode_str(s):
    if s is None:
        return ""
    decoded = decode_header(s)
    parts = []
    for part, charset in decoded:
        if isinstance(part, bytes):
            parts.append(part.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(part)
    return " ".join(parts)

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    return part.get_payload(decode=True).decode(errors="replace")
                except:
                    return ""
            elif part.get_content_type() == "text/html":
                try:
                    return part.get_payload(decode=True).decode(errors="replace")
                except:
                    return ""
    else:
        try:
            return msg.get_payload(decode=True).decode(errors="replace")
        except:
            return ""
    return ""

def fetch_emails():
    db = init_db()

    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(GMAIL_USER, GMAIL_PASS)
    mail.select("INBOX")

    # Fetch emails from last 7 days
    import datetime
    since = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'(SINCE {since})')

    if status != "OK":
        print("Failed to search")
        return

    msg_ids = messages[0].split()
    print(f"Found {len(msg_ids)} emails from last 7 days")

    count = 0
    for mid in msg_ids[-100:]:  # Last 100 max
        status, data = mail.fetch(mid, "(RFC822)")
        if status != "OK":
            continue

        msg = email.message_from_bytes(data[0][1])

        message_id = msg.get("Message-ID", f"unknown-{mid}")
        sender_raw = decode_str(msg.get("From", ""))
        subject = decode_str(msg.get("Subject", ""))
        date_str = msg.get("Date", "")

        # Parse sender
        sender_name, sender_email = email.utils.parseaddr(sender_raw)
        if not sender_name:
            sender_name = sender_email

        # Parse date to timestamp
        try:
            date_tuple = email.utils.parsedate_tz(date_str)
            timestamp = int(email.utils.mktime_tz(date_tuple)) if date_tuple else 0
        except:
            timestamp = 0

        body = get_body(msg)
        snippet = body[:500] if body else ""

        try:
            db.execute("""INSERT OR REPLACE INTO emails
                (message_id, sender, sender_email, subject, date, date_timestamp, body, snippet)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (message_id, sender_name, sender_email, subject, date_str, timestamp, body, snippet))
            count += 1
        except Exception as e:
            print(f"Error: {e}")

    db.commit()
    db.close()
    mail.logout()
    print(f"Synced {count} emails to {DB_PATH}")

def upload_to_r2():
    import boto3

    creds_file = os.path.expanduser("~/.r2-credentials")
    creds = {}
    with open(creds_file) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                creds[k.strip()] = v.strip()

    s3 = boto3.client("s3",
        endpoint_url="https://87fc573113247ec5fc93a6cc77401204.r2.cloudflarestorage.com",
        aws_access_key_id=creds["access_key"],
        aws_secret_access_key=creds["secret_key"],
        region_name="auto")

    s3.upload_file(DB_PATH, "sanat-db-sync", "Gmail.sqlite")
    size_mb = os.path.getsize(DB_PATH) / (1024 * 1024)
    print(f"Uploaded Gmail.sqlite ({size_mb:.1f}MB) to R2")

if __name__ == "__main__":
    fetch_emails()
    upload_to_r2()
