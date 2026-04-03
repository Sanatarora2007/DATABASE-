#!/bin/bash
# Watches WhatsApp, Calendar, and Reminders SQLite files for changes
# Triggers sync 10 seconds after the last change (debounce)
# Run as a background daemon via launchd

SYNC_SCRIPT="$HOME/DATABASE-/db-sync/r2-sync.py"
LOG_FILE="/tmp/dbsync.log"

# Database directories to watch
WHATSAPP_DIR="$HOME/Library/Group Containers/group.net.whatsapp.WhatsApp.shared"
CALENDAR_DIR="$HOME/Library/Group Containers/group.com.apple.calendar"
REMINDERS_DIR="$HOME/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores"

echo "$(date): DB watcher started (R2 mode)" >> "$LOG_FILE"

# fswatch with 10-second debounce (--latency)
# Only triggers after 10 seconds of no changes — batches rapid writes
fswatch \
    --latency 10 \
    --recursive \
    --include '\.sqlite$' \
    --include '\.sqlite-wal$' \
    --include '\.sqlitedb$' \
    --include '\.sqlitedb-wal$' \
    --exclude '.*' \
    "$WHATSAPP_DIR" \
    "$CALENDAR_DIR" \
    "$REMINDERS_DIR" \
    | while read -r changed_file; do
        echo "$(date): Change detected in $changed_file" >> "$LOG_FILE"
        python3 "$SYNC_SCRIPT" >> "$LOG_FILE" 2>&1
    done
