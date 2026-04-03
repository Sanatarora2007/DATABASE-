#!/bin/bash
set -e

echo "=== Setting up Claude Code ==="

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Create .claude directory structure
mkdir -p ~/.claude/projects

# Symlink skills
ln -sf "$(pwd)/.claude/skills" ~/.claude/skills

# Symlink plugins
ln -sf "$(pwd)/.claude/plugins" ~/.claude/plugins

# Symlink settings
ln -sf "$(pwd)/.claude/settings.json" ~/.claude/settings.json

# Symlink MCP configs
ln -sf "$(pwd)/.claude/.mcp.json" ~/.claude/.mcp.json
ln -sf "$(pwd)/mcp.json" ~/.claude/mcp.json

# Copy CLAUDE.md to home (global)
cp "$(pwd)/CLAUDE.md" ~/CLAUDE.md

# Symlink memory to project directory
PROJ_DIR=~/.claude/projects/-home-codespace-DATABASE-
mkdir -p "$PROJ_DIR"
ln -sf "$(pwd)/memory" "$PROJ_DIR/memory"

echo ""
echo "=== Pulling synced SQLite databases ==="

# Find the repo directory (varies by Codespace setup)
REPO_DIR="$(pwd)"

mkdir -p ~/synced-db

# Create refresh script that auto-detects repo path
cat > ~/refresh-db.sh << REFRESH
#!/bin/bash
cd "$REPO_DIR" 2>/dev/null || cd ~/DATABASE- 2>/dev/null || cd /workspaces/DATABASE- 2>/dev/null || { echo "✗ Can't find repo"; exit 1; }
git fetch origin db-sync 2>/dev/null
git show origin/db-sync:db-sync/snapshots/ChatStorage.sqlite > ~/synced-db/ChatStorage.sqlite 2>/dev/null
git show origin/db-sync:db-sync/snapshots/Calendar.sqlitedb > ~/synced-db/Calendar.sqlitedb 2>/dev/null
git show origin/db-sync:db-sync/snapshots/Reminders.sqlite > ~/synced-db/Reminders.sqlite 2>/dev/null
echo "✓ Databases refreshed at \$(date)"
REFRESH
chmod +x ~/refresh-db.sh

# Initial pull
bash ~/refresh-db.sh

# Auto-refresh every 60 seconds via cron
(crontab -l 2>/dev/null; echo "* * * * * bash ~/refresh-db.sh >> /tmp/db-refresh.log 2>&1") | sort -u | crontab -
# Start cron daemon if not running
sudo service cron start 2>/dev/null || true

echo "✓ Auto-refresh cron installed (every 60 seconds)"

echo ""
echo "=== Claude Code Setup Complete ==="
echo "Skills:  $(ls .claude/skills | wc -l) skills linked"
echo "Memory:  $(ls memory | wc -l) memory files linked"
echo "Plugins: linked"
echo "MCPs:    linked"
echo "DBs:     ~/synced-db/ (WhatsApp, Calendar, Reminders)"
echo ""
echo "Run 'claude' to start Claude Code"
echo "Run '~/refresh-db.sh' to pull latest database snapshots"
