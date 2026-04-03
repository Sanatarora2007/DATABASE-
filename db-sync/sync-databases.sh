#!/bin/bash
# Syncs WhatsApp, Calendar, and Reminders SQLite databases to DATABASE- repo
# Runs every 5 minutes via launchd
# Databases are stored on a separate 'db-sync' branch to avoid bloating main

set -e

REPO_DIR="$HOME/DATABASE-"
SYNC_DIR="$REPO_DIR/db-sync/snapshots"

# Source database paths
WHATSAPP_DB="$HOME/Library/Group Containers/group.net.whatsapp.WhatsApp.shared/ChatStorage.sqlite"
CALENDAR_DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
REMINDERS_DB="$HOME/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-A5FBE7B2-70BC-4FA4-BA7A-C5376D78F941.sqlite"

mkdir -p "$SYNC_DIR"

cd "$REPO_DIR"

# Switch to db-sync branch (create if needed)
git checkout db-sync 2>/dev/null || git checkout -b db-sync

# Copy databases using sqlite3 backup (safe — no locking issues)
if [ -f "$WHATSAPP_DB" ]; then
    sqlite3 "$WHATSAPP_DB" ".backup '$SYNC_DIR/ChatStorage.sqlite'" 2>/dev/null || \
    cp "$WHATSAPP_DB" "$SYNC_DIR/ChatStorage.sqlite"
    echo "$(date): WhatsApp synced"
fi

if [ -f "$CALENDAR_DB" ]; then
    sqlite3 "$CALENDAR_DB" ".backup '$SYNC_DIR/Calendar.sqlitedb'" 2>/dev/null || \
    cp "$CALENDAR_DB" "$SYNC_DIR/Calendar.sqlitedb"
    echo "$(date): Calendar synced"
fi

if [ -f "$REMINDERS_DB" ]; then
    sqlite3 "$REMINDERS_DB" ".backup '$SYNC_DIR/Reminders.sqlite'" 2>/dev/null || \
    cp "$REMINDERS_DB" "$SYNC_DIR/Reminders.sqlite"
    echo "$(date): Reminders synced"
fi

# Commit and push
git add db-sync/snapshots/
if git diff --cached --quiet; then
    echo "$(date): No changes to sync"
else
    git commit -m "DB sync $(date '+%Y-%m-%d %H:%M')"
    git push origin db-sync --force
    echo "$(date): Pushed to db-sync branch"
fi

# Switch back to master
git checkout master
